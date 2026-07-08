# ===================== 合规矩阵 =====================


COMPLIANCE_TEMPLATES = {
    "UAE_DEWA_VII_BESS": {
        "name": "UAE DEWA VII BESS RFP",
        "sections": [
            {
                "section": "1.0",
                "title": "通用要求",
                "requirements": [
                    {
                        "id": "1.1",
                        "text": "系统容量: 1400MW/8400MWh",
                        "category": "系统规模",
                    },
                    {
                        "id": "1.2",
                        "text": "储能时长: 6小时",
                        "category": "系统规模",
                    },
                    {
                        "id": "1.3",
                        "text": "IPP模式运营",
                        "category": "商业模式",
                    },
                    {
                        "id": "1.4",
                        "text": "2027-2029分阶段投运",
                        "category": "项目进度",
                    },
                ],
            },
            {
                "section": "2.0",
                "title": "电池系统",
                "requirements": [
                    {
                        "id": "2.1",
                        "text": "电池化学体系: LFP",
                        "category": "电池系统",
                    },
                    {
                        "id": "2.2",
                        "text": "循环寿命≥6000次@80%DoD",
                        "category": "电池系统",
                    },
                    {
                        "id": "2.3",
                        "text": "系统RTE≥90%",
                        "category": "性能保证",
                    },
                    {
                        "id": "2.4",
                        "text": "10年SOH≥70%",
                        "category": "性能保证",
                    },
                    {
                        "id": "2.5",
                        "text": "液冷热管理",
                        "category": "热管理",
                    },
                    {
                        "id": "2.6",
                        "text": "IP55防护等级",
                        "category": "环境防护",
                    },
                ],
            },
            {
                "section": "3.0",
                "title": "电网合规",
                "requirements": [
                    {
                        "id": "3.1",
                        "text": "符合UAE.S 5010-1标准",
                        "category": "电网合规",
                    },
                    {
                        "id": "3.2",
                        "text": "LVRT: 20%电压保持150ms",
                        "category": "电网合规",
                    },
                    {
                        "id": "3.3",
                        "text": "HVRT: 120%电压保持2s",
                        "category": "电网合规",
                    },
                    {
                        "id": "3.4",
                        "text": "频率响应: 49.5-50.5Hz",
                        "category": "电网合规",
                    },
                    {
                        "id": "3.5",
                        "text": "功率因数: 0.95滞后~0.95超前",
                        "category": "电网合规",
                    },
                    {
                        "id": "3.6",
                        "text": "THD≤5%",
                        "category": "电能质量",
                    },
                    {
                        "id": "3.7",
                        "text": "防孤岛保护≤2s",
                        "category": "安全保护",
                    },
                    {
                        "id": "3.8",
                        "text": "IEC 61850通信协议",
                        "category": "通信",
                    },
                ],
            },
            {
                "section": "4.0",
                "title": "安全与消防",
                "requirements": [
                    {
                        "id": "4.1",
                        "text": "UL 9540A认证",
                        "category": "安全认证",
                    },
                    {
                        "id": "4.2",
                        "text": "NFPA 855合规",
                        "category": "消防安全",
                    },
                    {
                        "id": "4.3",
                        "text": "可燃气体检测系统",
                        "category": "消防安全",
                    },
                    {
                        "id": "4.4",
                        "text": "火灾分区设计",
                        "category": "消防安全",
                    },
                    {
                        "id": "4.5",
                        "text": "热失控防护",
                        "category": "安全防护",
                    },
                    {
                        "id": "4.6",
                        "text": "IEC 62619认证",
                        "category": "安全认证",
                    },
                ],
            },
            {
                "section": "5.0",
                "title": "PCS与电力系统",
                "requirements": [
                    {
                        "id": "5.1",
                        "text": "Grid-forming逆变器",
                        "category": "PCS",
                    },
                    {
                        "id": "5.2",
                        "text": "合成惯量支持",
                        "category": "PCS",
                    },
                    {
                        "id": "5.3",
                        "text": "一次调频响应≤0.2s",
                        "category": "PCS",
                    },
                    {
                        "id": "5.4",
                        "text": "UL 1741 SB认证",
                        "category": "PCS认证",
                    },
                ],
            },
            {
                "section": "6.0",
                "title": "SCADA与EMS",
                "requirements": [
                    {
                        "id": "6.1",
                        "text": "SCADA系统集成",
                        "category": "SCADA",
                    },
                    {
                        "id": "6.2",
                        "text": "EMS能量调度",
                        "category": "EMS",
                    },
                    {
                        "id": "6.3",
                        "text": "远程监控与控制",
                        "category": "SCADA",
                    },
                    {
                        "id": "6.4",
                        "text": "网络安全: NERC-CIP",
                        "category": "网络安全",
                    },
                ],
            },
            {
                "section": "7.0",
                "title": "环境要求",
                "requirements": [
                    {
                        "id": "7.1",
                        "text": "高温运行: ≥45°C",
                        "category": "环境",
                    },
                    {
                        "id": "7.2",
                        "text": "沙尘防护: IP55+",
                        "category": "环境",
                    },
                    {
                        "id": "7.3",
                        "text": "噪声: ≤75dB@1m",
                        "category": "环境",
                    },
                    {
                        "id": "7.4",
                        "text": "电池回收计划",
                        "category": "环境",
                    },
                ],
            },
        ],
    }
}


def _auto_match_requirement(req, project_data):
    """自动匹配RFP条款"""
    text = req["text"]
    if "LVRT" in text:
        gc = project_data.get("grid_compliance", {})
        return (
            (
                "compliant",
                "系统支持LVRT功能",
            )
            if gc.get("lvrt_pass")
            else (
                (
                    "partial",
                    "系统支持LVRT功能",
                )
                if gc
                else ("N/A", "待电网合规分析")
            )
        )
    if "HVRT" in text:
        gc = project_data.get("grid_compliance", {})
        return (
            (
                "compliant",
                "系统支持HVRT功能",
            )
            if gc.get("hvrt_pass")
            else (
                (
                    "partial",
                    "系统支持HVRT功能",
                )
                if gc
                else ("N/A", "待电网合规分析")
            )
        )
    if "RTE" in text and "≥" in text:
        sim = project_data.get("simulation", {})
        rte = sim.get("rte_initial", 0)
        return (
            (
                "compliant",
                f"系统初始RTE = {rte}%",
            )
            if rte >= 90
            else (
                "partial",
                f"系统RTE = {rte}%，需优化",
            )
        )
    if "SOH" in text and "10年" in text:
        sim = project_data.get("simulation", {})
        return ("compliant", "第10年SOH满足要求") if sim.get("soh_year10", 0) >= 70 else ("partial", "需仿真验证")
    if "UL 9540" in text:
        safety = project_data.get("safety_design", {})
        return ("compliant", "已通过UL 9540A测试") if safety.get("ul_9540a_pass") else ("partial", "需提供测试报告")
    if "NFPA 855" in text:
        safety = project_data.get("safety_design", {})
        return ("compliant", "符合NFPA 855要求") if safety.get("nfpa_855_pass") else ("partial", "需安全设计分析")
    return ("N/A", "待人工确认")


def generate_compliance_matrix_service(data):
    """生成合规矩阵"""
    template_code = data.get("template", "UAE_DEWA_VII_BESS")
    template = COMPLIANCE_TEMPLATES.get(template_code)
    if not template:
        return None, "模板不存在"

    project_data = data.get("project_data", {})
    matrix = []

    for section in template["sections"]:
        for req in section["requirements"]:
            status, response = _auto_match_requirement(req, project_data)
            matrix.append(
                {
                    "section": req["id"],
                    "requirement": req["text"],
                    "category": req["category"],
                    "compliance_status": status,
                    "response": response,
                    "evidence": "",
                    "reference_doc": "",
                    "verified": False,
                }
            )

    compliant = sum(1 for m in matrix if m["compliance_status"] == "compliant")
    non_compliant = sum(1 for m in matrix if m["compliance_status"] == "non_compliant")
    partial = sum(1 for m in matrix if m["compliance_status"] == "partial")

    return {
        "matrix": matrix,
        "total": len(matrix),
        "compliant": compliant,
        "non_compliant": non_compliant,
        "partial": partial,
        "template_name": template["name"],
        "template_code": template_code,
    }, None
