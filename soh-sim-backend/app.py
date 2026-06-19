import math
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

N = 26


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
