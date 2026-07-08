# ===================== SCADA/EMS =====================


def design_scada_ems_service(data):
    """SCADA/EMS设计"""
    container_count = int(data.get("container_count", 20))
    pcs_count = int(data.get("pcs_count", 10))

    points_per_container = 200
    points_per_pcs = 50
    total_points = container_count * points_per_container + pcs_count * points_per_pcs + 500

    ems_functions = [
        "peak_shaving",
        "arbitrage",
        "frequency_regulation",
        "voltage_support",
        "renewable_smoothing",
        "black_start",
    ]

    return {
        "scada_architecture": data.get("scada_architecture", "hierarchical"),
        "communication_protocol": data.get("communication_protocol", "IEC_61850"),
        "network_topology": "ring",
        "redundancy_level": "dual",
        "total_data_points": total_points,
        "analog_points": int(total_points * 0.4),
        "digital_points": int(total_points * 0.5),
        "control_points": int(total_points * 0.1),
        "ems_functions": ems_functions,
        "dispatch_strategy": data.get("dispatch_strategy", "peak_shaving"),
        "forecasting_type": "load_and_pv_forecast",
        "firewall_config": "分层防火墙架构",
        "encryption_type": "AES-256",
        "nerc_cip_compliant": True,
        "iec_62443_compliant": True,
        "architecture_diagram": {
            "layers": [
                "站控层",
                "通信层",
                "间隔层",
                "过程层",
            ],
            "protocols": {
                "站控层": "IEC 61850 MMS",
                "间隔层": "IEC 61850 GOOSE",
                "过程层": "SV",
            },
        },
    }
