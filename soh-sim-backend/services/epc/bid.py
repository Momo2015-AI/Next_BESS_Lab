# ===================== 投标文档 =====================


BID_DOCUMENT_TEMPLATES = {
    "technical_proposal": {
        "name": "技术方案",
        "chapters": [
            {
                "num": "1",
                "title": "项目概述",
                "sections": [
                    {
                        "num": "1.1",
                        "title": "项目背景",
                        "source": "survey",
                    },
                    {
                        "num": "1.2",
                        "title": "系统规模",
                        "source": "survey",
                    },
                    {
                        "num": "1.3",
                        "title": "合规概述",
                        "source": "compliance_matrix",
                    },
                ],
            },
            {
                "num": "2",
                "title": "系统架构设计",
                "sections": [
                    {
                        "num": "2.1",
                        "title": "整体架构",
                        "source": "system_architecture",
                    },
                    {
                        "num": "2.2",
                        "title": "分期建设方案",
                        "source": "system_architecture",
                    },
                ],
            },
            {
                "num": "3",
                "title": "电池系统设计",
                "sections": [
                    {
                        "num": "3.1",
                        "title": "电芯选型",
                        "source": "dc_design",
                    },
                    {
                        "num": "3.2",
                        "title": "SOH/RTE性能保证",
                        "source": "simulation",
                    },
                ],
            },
            {
                "num": "4",
                "title": "PCS与电力系统",
                "sections": [
                    {
                        "num": "4.1",
                        "title": "PCS选型",
                        "source": "ac_design",
                    },
                    {
                        "num": "4.2",
                        "title": "高压接入设计",
                        "source": "hv_interconnection",
                    },
                    {
                        "num": "4.3",
                        "title": "电网合规",
                        "source": "grid_compliance",
                    },
                ],
            },
            {
                "num": "5",
                "title": "安全与消防设计",
                "sections": [
                    {
                        "num": "5.1",
                        "title": "火灾分区",
                        "source": "safety_design",
                    },
                    {
                        "num": "5.2",
                        "title": "热失控防护",
                        "source": "safety_design",
                    },
                ],
            },
            {
                "num": "6",
                "title": "热管理系统",
                "sections": [
                    {
                        "num": "6.1",
                        "title": "冷却方案",
                        "source": "thermal_management",
                    },
                ],
            },
            {
                "num": "7",
                "title": "SCADA与EMS",
                "sections": [
                    {
                        "num": "7.1",
                        "title": "系统架构",
                        "source": "scada_ems",
                    },
                ],
            },
            {
                "num": "8",
                "title": "性能保证",
                "sections": [
                    {
                        "num": "8.1",
                        "title": "SOH衰减曲线",
                        "source": "simulation",
                    },
                    {
                        "num": "8.2",
                        "title": "可用率保证",
                        "source": "ipp_financial",
                    },
                ],
            },
            {
                "num": "9",
                "title": "财务方案",
                "sections": [
                    {
                        "num": "9.1",
                        "title": "投资概算",
                        "source": "ipp_financial",
                    },
                    {
                        "num": "9.2",
                        "title": "LCOE分析",
                        "source": "ipp_financial",
                    },
                ],
            },
            {
                "num": "10",
                "title": "合规矩阵",
                "sections": [
                    {
                        "num": "10.1",
                        "title": "RFP条款逐项回应",
                        "source": "compliance_matrix",
                    },
                ],
            },
        ],
    }
}


def _generate_section_content(section_template, data):
    """根据数据源生成章节内容"""
    source = section_template["source"]
    if not data:
        return f"（待{source}模块数据填充）"

    if source == "survey":
        return (
            "项目名称: "
            + data.get("project_name", "N/A")
            + "\n"
            + "项目规模: "
            + data.get("total_mw", "N/A")
            + "MW / "
            + data.get("total_mwh", "N/A")
            + "MWh\n"
            + "储能时长: "
            + data.get("duration", "N/A")
            + "小时\n"
            + "项目位置: "
            + data.get("location", "N/A")
        )
    elif source == "system_architecture":
        return (
            "系统架构类型: "
            + data.get("architecture_type", "N/A")
            + "\n"
            + "PCS数量: "
            + data.get("pcs_count", "N/A")
            + "台\n"
            + "DC母线电压: "
            + data.get("dc_bus_voltage", "N/A")
            + "V\n"
            + "分期建设: "
            + data.get("stage_count", "N/A")
            + "期"
        )
    elif source == "simulation":
        return (
            "初始SOH: "
            + data.get("init_soh", "N/A")
            + "%\n"
            + "初始RTE: "
            + data.get("init_rte", "N/A")
            + "%\n"
            + "第10年SOH: "
            + data.get("soh_year10", "N/A")
            + "%"
        )
    elif source == "grid_compliance":
        return (
            "合规标准: "
            + data.get("grid_standard", "N/A")
            + "\n"
            + "LVRT: "
            + ("通过" if data.get("lvrt_pass") else "未通过")
            + "\n"
            + "HVRT: "
            + ("通过" if data.get("hvrt_pass") else "未通过")
            + "\n"
            + "总体合规: "
            + ("通过" if data.get("overall_pass") else "未通过")
        )
    elif source == "safety_design":
        return (
            "火灾分区: "
            + data.get("zone_count", "N/A")
            + "个\n"
            + "热失控温度: "
            + data.get("thermal_runaway_temp_c", "N/A")
            + "°C\n"
            + "UL 9540A: "
            + ("通过" if data.get("ul_9540a_pass") else "未通过")
        )
    elif source == "ipp_financial":
        return (
            "NPV: $"
            + data.get("npv_usd", "N/A")
            + "\n"
            + "IRR: "
            + data.get("irr", "N/A")
            + "%\n"
            + "LCOE: $"
            + data.get("lcoe_usd_kwh", "N/A")
            + "/kWh\n"
            + "回收期: "
            + data.get("payback_years", "N/A")
            + "年"
        )
    elif source == "thermal_management":
        return (
            "冷却方式: "
            + data.get("cooling_type", "N/A")
            + "\n"
            + "制冷容量: "
            + data.get("hvac_capacity_kw", "N/A")
            + "kW\n"
            + "目标温度: "
            + data.get("target_cell_temp_c", "N/A")
            + "°C"
        )
    elif source == "scada_ems":
        return (
            "架构: "
            + data.get("scada_architecture", "N/A")
            + "\n"
            + "通信协议: "
            + data.get("communication_protocol", "N/A")
            + "\n"
            + "数据点: "
            + data.get("total_data_points", "N/A")
        )
    elif source == "hv_interconnection":
        return (
            "并网点电压: "
            + data.get("poc_voltage_kv", "N/A")
            + "kV\n"
            + "变压器: "
            + data.get("transformer_count", "N/A")
            + "×"
            + data.get("transformer_capacity_mva", "N/A")
            + "MVA\n"
            + "变比: "
            + data.get("transformer_ratio", "N/A")
        )
    elif source == "compliance_matrix":
        return (
            "总条款: "
            + data.get("total_items", "N/A")
            + "\n"
            + "合规: "
            + data.get("compliant_count", "N/A")
            + "\n"
            + "不合规: "
            + data.get("non_compliant_count", "N/A")
            + "\n"
            + "部分合规: "
            + data.get("partial_count", "N/A")
        )
    else:
        return f"（待{source}模块数据填充）"


def generate_bid_document_service(data):
    """生成投标文档"""
    template_code = data.get("template", "technical_proposal")
    template = BID_DOCUMENT_TEMPLATES.get(template_code)
    if not template:
        return None, "模板不存在"

    project_data = data.get("project_data", {})

    chapters = []
    for ch_template in template["chapters"]:
        chapter = {
            "num": ch_template["num"],
            "title": ch_template["title"],
            "sections": [],
        }
        for sec_template in ch_template["sections"]:
            source = sec_template["source"]
            src_data = project_data.get(source, {})
            content = _generate_section_content(sec_template, src_data)
            chapter["sections"].append(
                {
                    "num": sec_template["num"],
                    "title": sec_template["title"],
                    "content": content,
                    "data_source": source,
                }
            )
        chapters.append(chapter)

    sources = list(set(s["source"] for ch in template["chapters"] for s in ch["sections"]))

    return {
        "chapters": chapters,
        "sources": sources,
        "template_name": template["name"],
        "template_code": template_code,
    }, None
