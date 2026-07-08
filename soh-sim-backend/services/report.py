"""
报告服务层
封装技术报告 / BOM 报告的 PDF 构建、Plotly 图表构建，
以及从数据库回填报告数据的逻辑。
供 routes/report.py 调用，保持路由层只负责 HTTP 协议与租户校验。
"""

import io
import json
import os
from datetime import datetime

from database import BatteryPCSConfig, Project, Simulation, Survey

# ==================== 字体与样式配置 ====================

_FONT_NAME = "Helvetica"
_FONT_NAME_BOLD = "Helvetica-Bold"
_font_registered = False


def register_chinese_font():
    """注册中文字体（仅需执行一次）"""
    global _FONT_NAME, _FONT_NAME_BOLD, _font_registered
    if _font_registered:
        return
    try:
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont

        font_paths = []
        win_font_dir = os.path.join(
            os.environ.get("WINDIR", "C:\\Windows"), "Fonts"
        )
        for fname in [
            "msyh.ttc",
            "msyhbd.ttc",
            "simhei.ttf",
            "simsun.ttc",
        ]:
            font_paths.append(
                (os.path.join(win_font_dir, fname), fname)
            )
        linux_paths = [
            "/usr/share/fonts/truetype/noto/"
            "NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/opentype/noto/"
            "NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/wqy/"
            "wqy-microhei.ttc",
        ]
        for p in linux_paths:
            font_paths.append((p, os.path.basename(p)))
        project_font_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            "fonts",
        )
        for fname in [
            "NotoSansSC-Regular.ttf",
            "SourceHanSansSC-Regular.ttf",
        ]:
            font_paths.append(
                (os.path.join(project_font_dir, fname), fname)
            )

        for path, name in font_paths:
            if os.path.exists(path):
                try:
                    pdfmetrics.registerFont(
                        TTFont("Chinese", path)
                    )
                    bold_path = (
                        path.replace("Regular", "Bold")
                        .replace("msyh.ttc", "msyhbd.ttc")
                    )
                    if os.path.exists(bold_path):
                        pdfmetrics.registerFont(
                            TTFont("ChineseBold", bold_path)
                        )
                        _FONT_NAME_BOLD = "ChineseBold"
                    else:
                        _FONT_NAME_BOLD = "Chinese"
                    _FONT_NAME = "Chinese"
                    _font_registered = True
                    return
                except Exception:
                    continue
        _font_registered = True
    except ImportError:
        _font_registered = True


def _build_styles():
    """构建 PDF 样式表"""
    from reportlab.lib.colors import HexColor
    from reportlab.lib.styles import (
        ParagraphStyle,
        getSampleStyleSheet,
    )

    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="CNTitle",
            fontName=_FONT_NAME_BOLD,
            fontSize=20,
            leading=28,
            spaceAfter=20,
            alignment=1,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CNSubTitle",
            fontName=_FONT_NAME,
            fontSize=12,
            leading=18,
            spaceAfter=6,
            textColor=HexColor("#666666"),
            alignment=1,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CNHeading",
            fontName=_FONT_NAME_BOLD,
            fontSize=14,
            leading=20,
            spaceBefore=16,
            spaceAfter=8,
            textColor=HexColor("#1a56db"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="CNBody",
            fontName=_FONT_NAME,
            fontSize=10,
            leading=16,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CNSmall",
            fontName=_FONT_NAME,
            fontSize=8,
            leading=12,
            textColor=HexColor("#888888"),
        )
    )
    return styles


def _draw_header(canvas, doc, project_name, report_type):
    canvas.saveState()
    from reportlab.lib.units import mm

    canvas.setFont(_FONT_NAME, 8)
    canvas.setFillColor("#999999")
    canvas.drawString(
        20 * mm, doc.height + 12 * mm, project_name
    )
    canvas.drawRightString(
        doc.width + 20 * mm,
        doc.height + 12 * mm,
        (
            "Technical Report"
            if report_type == "technical"
            else "Bill of Materials"
        ),
    )
    canvas.setStrokeColor("#dddddd")
    canvas.line(
        20 * mm,
        doc.height + 10 * mm,
        doc.width + 20 * mm,
        doc.height + 10 * mm,
    )
    canvas.restoreState()


def _draw_footer(canvas, doc):
    canvas.saveState()
    from reportlab.lib.units import mm

    canvas.setFont(_FONT_NAME, 8)
    canvas.setFillColor("#999999")
    canvas.drawCentredString(
        doc.width / 2 + 20 * mm,
        10 * mm,
        f"- {canvas.getPageNumber()} -",
    )
    canvas.restoreState()


def build_technical_report(data):
    """构建技术报告 PDF"""
    from reportlab.lib import colors
    from reportlab.lib.colors import HexColor
    from reportlab.lib.units import mm
    from reportlab.platypus import (
        PageBreak,
        Paragraph,
        SimpleDocTemplate,
        Spacer,
        Table,
        TableStyle,
    )

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=(210 * mm, 297 * mm),
        topMargin=25 * mm,
        bottomMargin=20 * mm,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
    )
    styles = _build_styles()
    project_name = data.get(
        "project_name", "BESS SOH Simulation"
    )
    story = []
    story.append(Spacer(1, 60 * mm))
    story.append(Paragraph("BESS SOH", styles["CNTitle"]))
    story.append(Paragraph(project_name, styles["CNTitle"]))
    story.append(Spacer(1, 10 * mm))
    story.append(
        Paragraph(
            'Report Date: '
            + datetime.now().strftime("%Y-%m-%d %H:%M"),
            styles["CNSubTitle"],
        )
    )
    story.append(PageBreak())

    story.append(
        Paragraph("1. Project Overview", styles["CNHeading"])
    )
    overview_data = [
        ["Project Name", project_name],
        ["Location", data.get("location", "-")],
        ["Total MW", str(data.get("total_mw", "-"))],
        ["Total MWh", str(data.get("total_mwh", "-"))],
        [
            "Duration",
            f"{data.get('duration', '-')} h",
        ],
        [
            "Cycles/Day",
            str(data.get("cycles_per_day", "-")),
        ],
        [
            "Report Time",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ],
    ]
    overview_table = Table(
        overview_data, colWidths=[60 * mm, 100 * mm]
    )
    overview_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), _FONT_NAME),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    HexColor("#f0f4ff"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (0, -1),
                    HexColor("#1a56db"),
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    HexColor("#dddddd"),
                ),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(overview_table)
    story.append(Spacer(1, 10 * mm))

    story.append(
        Paragraph(
            "2. System Configuration", styles["CNHeading"]
        )
    )
    params = data.get("params", {})
    param_rows = [
        ["Parameter", "Value", "Unit"],
        [
            "Rated Energy",
            str(params.get("ratedEnergy", "-")),
            "MWh",
        ],
        [
            "Container Qty",
            str(params.get("initContainerQty", "-")),
            "units",
        ],
        [
            "PCS Qty",
            str(params.get("initPcsQty", "-")),
            "units",
        ],
        [
            "Duration",
            str(params.get("duration", "-")),
            "h",
        ],
        [
            "Cycles/Day",
            str(params.get("cyclesPerDay", "-")),
            "cycles",
        ],
        [
            "AC Efficiency",
            f"{params.get('acEfficiency', '-')}",
            "%",
        ],
        [
            "BESS Aux Run",
            str(params.get("bessAuxRun", "-")),
            "kW",
        ],
        [
            "BESS Aux Standby",
            str(params.get("bessAuxStandby", "-")),
            "kW",
        ],
        [
            "PCS Aux Run",
            str(params.get("pcsAuxRun", "-")),
            "kW",
        ],
        [
            "PCS Aux Standby",
            str(params.get("pcsAuxStandby", "-")),
            "kW",
        ],
        [
            "Required Energy",
            str(params.get("requiredEnergy", "-")),
            "MWh",
        ],
    ]
    param_table = Table(
        param_rows,
        colWidths=[55 * mm, 50 * mm, 35 * mm],
    )
    param_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), _FONT_NAME),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    HexColor("#1a56db"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    _FONT_NAME_BOLD,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    HexColor("#dddddd"),
                ),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.white, HexColor("#f8faff")],
                ),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    story.append(param_table)
    story.append(Spacer(1, 10 * mm))

    story.append(
        Paragraph(
            "3. 25-Year Capacity Degradation Table",
            styles["CNHeading"],
        )
    )
    results = data.get("results", {})
    soh = data.get("soh", [])
    rte = data.get("rte", [])
    N = 26
    matrix_header = [
        "Yr",
        "SOH%",
        "RTE%",
        "Gross\nMWh",
        "Aux\nMWh",
        "Usable\nMWh",
        "Aug\nMWh",
        "Total\nMWh",
        "Aug\nQty",
        "OK",
    ]
    matrix_rows = [matrix_header]
    init_gross = results.get("initGross", [0] * N)
    init_aux = results.get("initAux", [0] * N)
    init_ac = results.get("initAcUsable", [0] * N)
    aug_gross = results.get("augGross", [0] * N)
    aug_ac = results.get("augAcUsable", [0] * N)
    total_ac = results.get("totalAcUsable", [0] * N)
    aug_qty = results.get("augAccumQty", [0] * N)
    meets_req = results.get("meetsReq", [False] * N)
    for i in range(N):
        row = [
            str(i),
            (
                f"{soh[i]*100:.1f}"
                if i < len(soh) and soh[i] is not None
                else "-"
            ),
            (
                f"{rte[i]*100:.1f}"
                if i < len(rte) and rte[i] is not None
                else "-"
            ),
            (
                f"{init_gross[i]:.2f}"
                if i < len(init_gross)
                else "0"
            ),
            (
                f"{init_aux[i]:.2f}"
                if i < len(init_aux)
                else "0"
            ),
            (
                f"{init_ac[i]:.2f}"
                if i < len(init_ac)
                else "0"
            ),
            (
                f"{aug_ac[i]:.2f}"
                if i < len(aug_ac)
                else "0"
            ),
            (
                f"{total_ac[i]:.2f}"
                if i < len(total_ac)
                else "0"
            ),
            (
                f"{int(aug_qty[i])}"
                if i < len(aug_qty)
                else "0"
            ),
            (
                "Y"
                if i < len(meets_req) and meets_req[i]
                else "N"
            ),
        ]
        matrix_rows.append(row)
    col_w = [
        12 * mm,
        14 * mm,
        14 * mm,
        16 * mm,
        14 * mm,
        16 * mm,
        16 * mm,
        16 * mm,
        12 * mm,
        10 * mm,
    ]
    matrix_table = Table(
        matrix_rows, colWidths=col_w, repeatRows=1
    )
    matrix_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), _FONT_NAME),
                ("FONTSIZE", (0, 0), (-1, -1), 7),
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    HexColor("#1a56db"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    _FONT_NAME_BOLD,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.3,
                    HexColor("#cccccc"),
                ),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.white, HexColor("#f8faff")],
                ),
                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER",
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                (
                    "TEXTCOLOR",
                    (-1, 1),
                    (-1, -1),
                    HexColor("#dc2626"),
                ),
            ]
        )
    )
    story.append(matrix_table)
    story.append(Spacer(1, 10 * mm))

    story.append(
        Paragraph("4. Conclusion", styles["CNHeading"])
    )
    fail_years = [
        i
        for i in range(N)
        if i < len(meets_req) and not meets_req[i]
    ]
    conclusion = (
        'Years not meeting requirement: '
        + ", ".join(map(str, fail_years))
        + ". Augmentation recommended."
        if fail_years
        else (
            "All 25 years meet the required energy target."
        )
    )
    story.append(Paragraph(conclusion, styles["CNBody"]))

    doc.build(
        story,
        onFirstPage=lambda c, d: (
            _draw_header(
                c, d, project_name, "technical"
            ),
            _draw_footer(c, d),
        ),
        onLaterPages=lambda c, d: (
            _draw_header(
                c, d, project_name, "technical"
            ),
            _draw_footer(c, d),
        ),
    )
    buf.seek(0)
    return buf


def build_bom_report(data):
    """构建设备清单 BOM PDF"""
    from reportlab.lib import colors
    from reportlab.lib.colors import HexColor
    from reportlab.lib.units import mm
    from reportlab.platypus import (
        PageBreak,
        Paragraph,
        SimpleDocTemplate,
        Spacer,
        Table,
        TableStyle,
    )

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=(210 * mm, 297 * mm),
        topMargin=25 * mm,
        bottomMargin=20 * mm,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
    )
    styles = _build_styles()
    project_name = data.get(
        "project_name", "BESS SOH Simulation"
    )
    story = []
    story.append(Spacer(1, 60 * mm))
    story.append(
        Paragraph("Bill of Materials", styles["CNTitle"])
    )
    story.append(Paragraph(project_name, styles["CNTitle"]))
    story.append(Spacer(1, 10 * mm))
    story.append(
        Paragraph(
            'Report Date: '
            + datetime.now().strftime("%Y-%m-%d %H:%M"),
            styles["CNSubTitle"],
        )
    )
    story.append(PageBreak())

    def _table(title, rows):
        story.append(
            Paragraph(title, styles["CNHeading"])
        )
        if not rows:
            story.append(
                Paragraph(
                    "No data available.", styles["CNBody"]
                )
            )
        else:
            t = Table(
                rows, colWidths=[60 * mm, 100 * mm]
            )
            t.setStyle(
                TableStyle(
                    [
                        (
                            "FONTNAME",
                            (0, 0),
                            (-1, -1),
                            _FONT_NAME,
                        ),
                        (
                            "FONTSIZE",
                            (0, 0),
                            (-1, -1),
                            10,
                        ),
                        (
                            "BACKGROUND",
                            (0, 0),
                            (0, -1),
                            HexColor("#f0f4ff"),
                        ),
                        (
                            "TEXTCOLOR",
                            (0, 0),
                            (0, -1),
                            HexColor("#1a56db"),
                        ),
                        (
                            "GRID",
                            (0, 0),
                            (-1, -1),
                            0.5,
                            HexColor("#dddddd"),
                        ),
                        (
                            "TOPPADDING",
                            (0, 0),
                            (-1, -1),
                            4,
                        ),
                        (
                            "BOTTOMPADDING",
                            (0, 0),
                            (-1, -1),
                            4,
                        ),
                    ]
                )
            )
            story.append(t)
        story.append(Spacer(1, 10 * mm))

    _table(
        "1. Cell Selection",
        [
            ["Parameter", "Value"],
            [
                "Manufacturer",
                data.get("cell", {}).get(
                    "manufacturer", "-"
                ),
            ],
            [
                "Model",
                data.get("cell", {}).get("model", "-"),
            ],
            [
                "Capacity (Ah)",
                str(
                    data.get("cell", {}).get(
                        "capacity", "-"
                    )
                ),
            ],
            [
                "Nominal Voltage (V)",
                str(
                    data.get("cell", {}).get(
                        "nominalVoltage", "-"
                    )
                ),
            ],
            [
                "Energy per Cell (Wh)",
                str(
                    data.get("cell", {}).get("energy", "-")
                ),
            ],
            [
                "Cycle Life",
                str(
                    data.get("cell", {}).get(
                        "cycleLife", "-"
                    )
                ),
            ],
            [
                "Chemistry",
                data.get("cell", {}).get(
                    "chemistry", "LFP"
                ),
            ],
        ]
        if data.get("cell")
        else None,
    )
    _table(
        "2. Container Selection",
        [
            ["Parameter", "Value"],
            [
                "Manufacturer",
                data.get("container", {}).get(
                    "manufacturer", "-"
                ),
            ],
            [
                "Model",
                data.get("container", {}).get(
                    "model", "-"
                ),
            ],
            [
                "Rated Energy (MWh)",
                str(
                    data.get("container", {}).get(
                        "ratedEnergy", "-"
                    )
                ),
            ],
            [
                "Rated Power (MW)",
                str(
                    data.get("container", {}).get(
                        "ratedPower", "-"
                    )
                ),
            ],
            [
                "Cooling Type",
                data.get("container", {}).get(
                    "coolingType", "-"
                ),
            ],
        ]
        if data.get("container")
        else None,
    )
    _table(
        "3. PCS Selection",
        [
            ["Parameter", "Value"],
            [
                "Manufacturer",
                data.get("pcs", {}).get(
                    "manufacturer", "-"
                ),
            ],
            [
                "Model",
                data.get("pcs", {}).get("model", "-"),
            ],
            [
                "Rated Power (MW)",
                str(
                    data.get("pcs", {}).get(
                        "ratedPower", "-"
                    )
                ),
            ],
            [
                "Efficiency (%)",
                str(
                    data.get("pcs", {}).get(
                        "efficiency", "-"
                    )
                ),
            ],
            [
                "Topology",
                data.get("pcs", {}).get(
                    "topology", "-"
                ),
            ],
        ]
        if data.get("pcs")
        else None,
    )

    story.append(
        Paragraph(
            "4. Quantity Summary", styles["CNHeading"]
        )
    )
    params = data.get("params", {})
    summary_rows = [
        ["Item", "Quantity", "Unit"],
        [
            "Container (Initial)",
            str(params.get("initContainerQty", "-")),
            "units",
        ],
        [
            "PCS (Initial)",
            str(params.get("initPcsQty", "-")),
            "units",
        ],
    ]
    aug_qty_list = data.get("results", {}).get(
        "augAccumQty", []
    )
    if aug_qty_list:
        total_aug = int(max(aug_qty_list))
        summary_rows.append(
            [
                "Container (Augmentation)",
                str(total_aug),
                "units",
            ]
        )
        summary_rows.append(
            [
                "Container (Total)",
                str(
                    params.get("initContainerQty", 0)
                    + total_aug
                ),
                "units",
            ]
        )
    summary_table = Table(
        summary_rows,
        colWidths=[70 * mm, 40 * mm, 30 * mm],
    )
    summary_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), _FONT_NAME),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    HexColor("#1a56db"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    _FONT_NAME_BOLD,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    HexColor("#dddddd"),
                ),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.white, HexColor("#f8faff")],
                ),
                (
                    "ALIGN",
                    (1, 0),
                    (-1, -1),
                    "CENTER",
                ),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(summary_table)

    doc.build(
        story,
        onFirstPage=lambda c, d: (
            _draw_header(c, d, project_name, "bom"),
            _draw_footer(c, d),
        ),
        onLaterPages=lambda c, d: (
            _draw_header(c, d, project_name, "bom"),
            _draw_footer(c, d),
        ),
    )
    buf.seek(0)
    return buf


def supplement_technical_data(data, current_user):
    """从数据库补充技术报告数据（项目概况、仿真结果）。
    租户隔离由调用方校验。
    """
    project_id = data.get("project_id")
    simulation_id = data.get("simulation_id")
    if project_id:
        project = Project.query.get(project_id)
        if project:
            data.setdefault(
                "project_name", project.name
            )
            survey = Survey.query.filter_by(
                project_id=project_id
            ).first()
            if survey:
                data.setdefault(
                    "location", survey.location or "-"
                )
                data.setdefault(
                    "total_mw", survey.total_mw or "-"
                )
                data.setdefault(
                    "total_mwh",
                    survey.total_mwh or "-",
                )
                data.setdefault(
                    "duration", survey.duration or "-"
                )
                data.setdefault(
                    "cycles_per_day",
                    survey.cycles_per_day or "-",
                )
        if simulation_id:
            simulation = Simulation.query.get(
                simulation_id
            )
            if simulation and simulation.results:
                sim_results = json.loads(
                    simulation.results
                )
                data.setdefault(
                    "results",
                    sim_results.get("results", {}),
                )
                data.setdefault(
                    "params",
                    sim_results.get("params", {}),
                )
                data.setdefault(
                    "soh", sim_results.get("soh", [])
                )
                data.setdefault(
                    "rte", sim_results.get("rte", [])
                )
    return data


def supplement_bom_data(data, current_user):
    """从数据库补充 BOM 报告数据
    （项目概况、电池/PCS 选型配置）。
    """
    project_id = data.get("project_id")
    if project_id:
        project = Project.query.get(project_id)
        if project:
            data.setdefault(
                "project_name", project.name
            )
        bp_config = BatteryPCSConfig.query.filter_by(
            project_id=project_id
        ).first()
        if bp_config:
            data.setdefault(
                "cell",
                (
                    json.loads(bp_config.cell_config)
                    if bp_config.cell_config
                    else {}
                ),
            )
            data.setdefault(
                "container",
                (
                    json.loads(
                        bp_config.container_config
                    )
                    if bp_config.container_config
                    else {}
                ),
            )
            data.setdefault(
                "pcs",
                (
                    json.loads(bp_config.pcs_config)
                    if bp_config.pcs_config
                    else {}
                ),
            )
    return data


def supplement_chart_data(data):
    """从数据库补充图表数据（仿真结果）。"""
    project_id = data.get("project_id")
    simulation_id = data.get("simulation_id")
    if project_id and simulation_id:
        simulation = Simulation.query.get(
            simulation_id
        )
        if simulation and simulation.results:
            sim_results = json.loads(
                simulation.results
            )
            data.setdefault(
                "results",
                sim_results.get("results", {}),
            )
            data.setdefault(
                "params", sim_results.get("params", {})
            )
            data.setdefault(
                "soh", sim_results.get("soh", [])
            )
            data.setdefault(
                "rte", sim_results.get("rte", [])
            )
    return data


try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False


def _plotly_layout_defaults(title, x_title="", y_title=""):
    return dict(
        title=title,
        xaxis=dict(
            title=x_title,
            gridcolor="#e5e7eb",
            zerolinecolor="#9ca3af",
        ),
        yaxis=dict(
            title=y_title,
            gridcolor="#e5e7eb",
            zerolinecolor="#9ca3af",
        ),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font=dict(
            family="Microsoft YaHei, Arial, sans-serif",
            size=12,
            color="#1f2937",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        margin=dict(l=60, r=30, t=80, b=60),
    )


def _build_soh_rte_curve_chart(data):
    soh = data.get("soh", [])
    rte = data.get("rte", [])
    n = max(len(soh), len(rte))
    if n == 0:
        return None
    years = list(range(n))
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=years,
            y=[
                s * 100 if s is not None else None
                for s in soh
            ],
            name="SOH",
            mode="lines+markers",
            line=dict(color="#1a56db", width=2.5),
            marker=dict(size=6),
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=years,
            y=[
                r * 100 if r is not None else None
                for r in rte
            ],
            name="RTE",
            mode="lines+markers",
            line=dict(
                color="#dc2626", width=2.5, dash="dot"
            ),
            marker=dict(size=6),
        ),
        secondary_y=True,
    )
    fig.update_layout(
        **_plotly_layout_defaults(
            "25 年 SOH/RTE 衰减曲线", "运行年数", ""
        )
    )
    fig.update_yaxes(
        title_text="SOH (%)",
        secondary_y=False,
        range=[60, 105],
    )
    fig.update_yaxes(
        title_text="RTE (%)",
        secondary_y=True,
        range=[85, 100],
    )
    return fig


def _build_capacity_matrix_heatmap(data):
    results = data.get("results", {})
    total_ac = results.get("totalAcUsable", [])
    required = data.get("params", {}).get("requiredEnergy")
    if not total_ac:
        return None
    years = list(range(len(total_ac)))
    z = [[v] for v in total_ac]
    fig = go.Figure(
        data=go.Heatmap(
            z=z,
            x=["可用容量 (MWh)"],
            y=years,
            colorscale="RdYlGn",
            colorbar=dict(title="MWh"),
            text=[[f"{v:.1f}"] for v in total_ac],
            texttemplate="%{text}",
            hovertemplate=(
                "Year %{y}<br>"
                "Capacity %{z:.2f} MWh<extra></extra>"
            ),
        )
    )
    if required:
        fig.add_hline(
            y=required,
            line_dash="dash",
            line_color="#1f2937",
            annotation_text=f"要求 {required} MWh",
            annotation_position="top right",
        )
    fig.update_layout(
        **_plotly_layout_defaults(
            "25 年容量矩阵热力图", "", "运行年数"
        )
    )
    return fig


def _build_grid_compliance_chart(data):
    lvrt = data.get("lvrt_curve", {})
    hvrt = data.get("hvrt_curve", {})
    if not lvrt and not hvrt:
        return None
    fig = go.Figure()
    if lvrt:
        fig.add_trace(
            go.Scatter(
                x=lvrt.get("voltage", []),
                y=lvrt.get("time", []),
                name="LVRT",
                fill="tozeroy",
                line=dict(color="#1a56db", width=2.5),
            )
        )
    if hvrt:
        fig.add_trace(
            go.Scatter(
                x=hvrt.get("voltage", []),
                y=hvrt.get("time", []),
                name="HVRT",
                fill="tozeroy",
                line=dict(color="#dc2626", width=2.5),
            )
        )
    fig.update_layout(
        **_plotly_layout_defaults(
            "电网合规 LVRT/HVRT 曲线", "电压 (pu)", "时间 (s)"
        )
    )
    return fig


def _build_ipp_cashflow_chart(data):
    cashflow = data.get("cashflow_data", [])
    if not cashflow:
        return None
    years = [
        c.get("year", i) for i, c in enumerate(cashflow)
    ]
    cum_npv = []
    acc = 0
    for c in cashflow:
        acc += c.get("net_cashflow", 0)
        cum_npv.append(acc)
    fig = go.Figure(
        go.Waterfall(
            x=years,
            y=[
                c.get("net_cashflow", 0)
                for c in cashflow
            ],
            name="年度净现金流",
            measure=[
                c.get("measure", "relative")
                for c in cashflow
            ],
            decreasing=dict(
                marker=dict(color="#dc2626")
            ),
            increasing=dict(
                marker=dict(color="#16a34a")
            ),
            totals=dict(marker=dict(color="#1a56db")),
            connector=dict(
                line=dict(color="#9ca3af", width=1)
            ),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=years,
            y=cum_npv,
            name="累计现金流",
            line=dict(
                color="#f59e0b", width=2, dash="dot"
            ),
            mode="lines+markers",
        )
    )
    fig.update_layout(
        **_plotly_layout_defaults(
            "IPP 25 年现金流瀑布图",
            "运行年数",
            "现金流 (USD)",
        )
    )
    return fig


CHART_BUILDERS = {
    "soh_rte_curve": _build_soh_rte_curve_chart,
    "capacity_matrix": _build_capacity_matrix_heatmap,
    "grid_compliance": _build_grid_compliance_chart,
    "ipp_cashflow": _build_ipp_cashflow_chart,
}
