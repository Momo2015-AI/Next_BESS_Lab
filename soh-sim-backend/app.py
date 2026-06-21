import math
import os
import re
import csv
import io
import tempfile
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from database import db, init_db, Survey, Project
from routes.survey import survey_bp
from routes.export import export_bp
from routes.auth import auth_bp

app = Flask(__name__)
CORS(app)

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(os.path.abspath(__file__)), 'soh_sim.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# JWT Secret Key (生产环境请使用环境变量)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'soh-sim-secret-key-change-in-production')

# 初始化数据库
init_db(app)

# 注册路由
app.register_blueprint(survey_bp)
app.register_blueprint(export_bp)
app.register_blueprint(auth_bp)

N = 26
UPLOAD_DIR = os.path.join(tempfile.gettempdir(), "soh_uploads")


def calculate(params, soh, rte, dod, aug_qty):
    rated_energy = params.get("ratedEnergy", 5)
    init_container_qty = params.get("initContainerQty", 62)
    init_pcs_qty = params.get("initPcsQty", 1)
    duration = params.get("duration", 2)
    cycles_per_day = params.get("cyclesPerDay", 1)
    ac_efficiency = params.get("acEfficiency", 97.03) / 100
    bess_aux_run = params.get("bessAuxRun", 18.124)
    bess_aux_standby = params.get("bessAuxStandby", 3.5)
    pcs_aux_run = params.get("pcsAuxRun", 6.5)
    pcs_aux_standby = params.get("pcsAuxStandby", 1.0)
    required_energy = params.get("requiredEnergy", 240)

    run_hours = duration * cycles_per_day
    standby_hours = max(0, 24 - run_hours)

    daily_container_aux_per_unit = (bess_aux_run * run_hours + bess_aux_standby * standby_hours) / 1000
    daily_pcs_aux_per_unit = (pcs_aux_run * run_hours + pcs_aux_standby * standby_hours) / 1000
    cycle_container_aux_per_unit = daily_container_aux_per_unit / cycles_per_day
    cycle_pcs_aux_per_unit = daily_pcs_aux_per_unit / cycles_per_day

    init_gross = [0.0] * N
    init_aux = [0.0] * N
    init_ac_usable = [0.0] * N
    aug_gross = [0.0] * N
    aug_aux = [0.0] * N
    aug_ac_usable = [0.0] * N
    aug_accum_qty = [0.0] * N
    total_ac_usable = [0.0] * N
    meets_req = [False] * N

    accum = 0
    for i in range(N):
        accum += int(aug_qty[i]) if i < len(aug_qty) else 0
        aug_accum_qty[i] = accum

        c_dod = (float(dod[i]) if i < len(dod) else (float(dod[-1]) if dod else 100)) / 100
        c_rte = float(rte[i]) if i < len(rte) else (float(rte[-1]) if rte else 0)
        c_soh = float(soh[i]) if i < len(soh) else (float(soh[-1]) if soh else 0)

        init_gross[i] = rated_energy * init_container_qty * c_dod * c_rte * c_soh * ac_efficiency
        init_aux[i] = init_container_qty * cycle_container_aux_per_unit + init_pcs_qty * cycle_pcs_aux_per_unit
        init_ac_usable[i] = max(0, init_gross[i] - init_aux[i])

        total_aug_ac = 0.0
        total_aug_aux = 0.0
        for k in range(i + 1):
            qty_k = int(aug_qty[k]) if k < len(aug_qty) else 0
            if qty_k > 0:
                age = i - k
                asset_soh = float(soh[min(age, N - 1)])
                asset_gross = rated_energy * qty_k * c_dod * c_rte * asset_soh * ac_efficiency
                asset_aux = qty_k * cycle_container_aux_per_unit
                total_aug_ac += max(0, asset_gross - asset_aux)
                total_aug_aux += asset_aux

        aug_gross[i] = total_aug_ac + total_aug_aux
        aug_aux[i] = total_aug_aux
        aug_ac_usable[i] = total_aug_ac
        total_ac_usable[i] = init_ac_usable[i] + total_aug_ac
        meets_req[i] = total_ac_usable[i] >= required_energy

    return {
        "initGross": init_gross,
        "initAux": init_aux,
        "initAcUsable": init_ac_usable,
        "augGross": aug_gross,
        "augAux": aug_aux,
        "augAcUsable": aug_ac_usable,
        "augAccumQty": aug_accum_qty,
        "totalAcUsable": total_ac_usable,
        "meetsReq": meets_req,
    }


@app.route("/api/soh/calculate", methods=["POST"])
def soh_calculate():
    data = request.get_json()
    if not data:
        return jsonify({"error": "invalid request body"}), 400

    params = data.get("params", {})
    soh = data.get("soh", [])
    rte = data.get("rte", [])
    dod = data.get("dod", [])
    aug_qty = data.get("augQty", [])

    try:
        results = calculate(params, soh, rte, dod, aug_qty)
        return jsonify({"results": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/soh/calculate-multi", methods=["POST"])
def soh_calculate_multi():
    data = request.get_json()
    if not data:
        return jsonify({"error": "invalid request body"}), 400

    scenarios = data.get("scenarios", [])
    all_results = []
    for scenario in scenarios:
        params = scenario.get("params", {})
        soh = scenario.get("soh", [])
        rte = scenario.get("rte", [])
        dod = scenario.get("dod", [])
        aug_qty = scenario.get("augQty", [])
        try:
            results = calculate(params, soh, rte, dod, aug_qty)
            all_results.append(results)
        except Exception as e:
            all_results.append({"error": str(e)})

    return jsonify({"results": all_results})


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/api/upload/extract", methods=["POST"])
def upload_extract():
    if "file" not in request.files:
        return jsonify({"error": "no file uploaded"}), 400

    f = request.files["file"]
    if f.filename == "":
        return jsonify({"error": "empty filename"}), 400

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    ext = os.path.splitext(f.filename)[1].lower()
    text = ""

    try:
        if ext == ".csv":
            stream = io.StringIO(f.read().decode("utf-8", errors="replace"))
            reader = csv.reader(stream)
            rows = list(reader)
            text = "\n".join([" | ".join(r) for r in rows[:200]])
        elif ext in (".xlsx", ".xls"):
            try:
                import openpyxl
                wb = openpyxl.load_workbook(io.BytesIO(f.read()), data_only=True)
                ws = wb.active
                rows_list = []
                for row in ws.iter_rows(values_only=True):
                    rows_list.append(" | ".join([str(c) if c is not None else "" for c in row]))
                text = "\n".join(rows_list[:200])
            except ImportError:
                text = "xlsx_parsing_unavailable"
        elif ext == ".txt":
            text = f.read().decode("utf-8", errors="replace")[:5000]
        elif ext == ".json":
            import json
            data = json.loads(f.read().decode("utf-8", errors="replace"))
            text = json.dumps(data, indent=2, ensure_ascii=False)
        elif ext == ".pdf":
            text = f.read().decode("latin-1", errors="replace")[:5000]
            text = "".join(c for c in text if c.isprintable() or c in "\n\r\t")
        else:
            raw = f.read()[:5000]
            text = raw.decode("utf-8", errors="replace")
    except Exception as e:
        return jsonify({"error": f"file read failed: {str(e)}"}), 400

    if not text or len(text) < 5:
        return jsonify({"extracted": {}, "fieldsExtracted": 0})

    extracted = extract_parameters(text)
    return jsonify({"extracted": extracted, "rawPreview": text[:1000]})


def extract_parameters(text):
    patterns = [
        (r"(?:project|项目)\s*(?:name|名称|名称)\s*[:：=]?\s*([^\n\r]{2,80})", "project_name"),
        (r"(?:location|地点|位置)\s*[:：=]?\s*([^\n\r]{2,50})", "location"),
        (r"(?:total|总|额定).*(?:power|功率|MW)\s*[:：=]?\s*(\d+\.?\d*)", "total_mw"),
        (r"(?:total|总|额定).*(?:energy|能量|MWh|容量)\s*[:：=]?\s*(\d+\.?\d*)", "total_mwh"),
        (r"(?:duration|时长|充放电).*(?:hour|小时|h)\s*[:：=]?\s*(\d+\.?\d*)", "duration_h"),
        (r"(?:cycle|循环).*(?:day|天|日).*[:：=]?\s*(\d+\.?\d*)", "cycles_per_day"),
        (r"(?:altitude|海拔|elevation)\s*[:：=]?\s*(\d+\.?\d*)", "altitude_m"),
        (r"(?:max.*temp|最高.*温|极端.*高温)\s*[:：=]?\s*(\d+\.?\d*)", "temp_max_c"),
        (r"(?:min.*temp|最低.*温|极端.*低温)\s*[:：=]?\s*(-?\d+\.?\d*)", "temp_min_c"),
        (r"(?:avg.*temp|平均.*温)\s*[:：=]?\s*(\d+\.?\d*)", "temp_avg_c"),
        (r"(?:humidity|湿度|RH)\s*[:：=]?\s*(\d+\.?\d*)", "humidity_pct"),
        (r"(?:grid.*voltage|并网.*电压|电压等级)\s*[:：=]?\s*(\d+\.?\d*\s*kV)", "grid_voltage_kv"),
        (r"(?:frequency|频率|Hz)\s*[:：=]?\s*(\d+\.?\d*\s*Hz)", "grid_freq_hz"),
        (r"(?:RTE|round.?trip|充放电效率).*(?:target|目标|年).*[:：=]?\s*(\d+\.?\d*)", "rte_target_pct"),
        (r"(?:SOH|健康状态).*(?:year.?1|1年|第一年).*[:：=]?\s*(\d+\.?\d*)", "soh_year1_pct"),
        (r"(?:SOH|健康状态).*(?:year.?25|25年).*[:：=]?\s*(\d+\.?\d*)", "soh_year25_pct"),
        (r"(?:calendar.*life|日历.*寿命|设计.*寿命).*[:：=]?\s*(\d+\.?\d*)", "calendar_life_y"),
        (r"(?:cycle.*life|循环.*寿命).*[:：=]?\s*(\d+\.?\d*)", "cycle_life"),
        (r"(?:aux|辅助|自耗).*(?:consumption|功耗|电耗).*[:：=]?\s*(\d+\.?\d*)", "aux_consumption_pct"),
        (r"(?:response.*time|响应.*时间).*[:：=]?\s*(\d+\.?\d*)", "response_time_ms"),
        (r"(?:DC.*voltage|直流.*电压|DC.*范围).*[:：=]?\s*(\d+\s*[-~]\s*\d+\s*V)", "dc_voltage_range"),
        (r"(?:AC.*voltage|交流.*电压).*[:：=]?\s*(\d+\.?\d*\s*V)", "ac_voltage_v"),
        (r"(?:THD|谐波).*[:：=]?\s*(\d+\.?\d*)\s*%?", "thdi_pct"),
        (r"(?:availability|可用率|可用).*[:：=]?\s*(\d+\.?\d*)\s*%?", "availability_target_pct"),
    ]

    extracted = {}
    for pattern, key in patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            val = m.group(1).strip()
            try:
                val = float(re.sub(r"[^\d.\-]", "", val))
            except ValueError:
                pass
            extracted[key] = val

    return extracted


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)