"""
EPC模块服务层
包含: 系统架构、电网合规、安全消防、IPP财务、合规矩阵、
      热管理、SCADA/EMS、高压接入、投标文档
"""

import json
import math


# ===================== 系统架构设计 =====================


def design_architecture_service(data):
    """自动设计系统架构"""
    total_power_mw = float(data.get("total_power_mw", 100))
    total_energy_mwh = float(data.get("total_energy_mwh", 200))
    duration_hours = total_energy_mwh / total_power_mw if total_power_mw > 0 else 2
    arch_type = data.get("architecture_type", "central")
    coupling = data.get("coupling_type", "AC")

    cell_v = float(data.get("cell_voltage", 3.2))
    cell_ah = float(data.get("cell_capacity", 280))
    cell_energy_kwh = cell_v * cell_ah / 1000

    pcs_power_mw = float(data.get("pcs_power_mw", 3.45))
    pcs_max_dc_v = float(data.get("pcs_max_dc_voltage", 1500))

    pcs_count = math.ceil(total_power_mw / pcs_power_mw)
    dc_bus_voltage = min(pcs_max_dc_v * 0.9, 1500)
    cell_series = int(dc_bus_voltage / cell_v)
    module_series = 24 if cell_series >= 24 else 12
    modules_per_rack = cell_series // module_series
    pack_energy_kwh = module_series * cell_v * cell_ah / 1000
    rack_energy_kwh = pack_energy_kwh * modules_per_rack
    rack_power_kw = rack_energy_kwh / duration_hours if duration_hours > 0 else 0
    racks_per_cluster = max(1, math.ceil(pcs_power_mw * 1000 / rack_power_kw / 4)) if rack_power_kw > 0 else 1
    cluster_energy_mwh = rack_energy_kwh * racks_per_cluster / 1000
    racks_per_container = min(racks_per_cluster, 8)
    containers_per_pcs = max(1, math.ceil(racks_per_cluster / racks_per_container))
    container_energy_mwh = rack_energy_kwh * racks_per_container / 1000
    total_containers = pcs_count * containers_per_pcs
    containers_per_section = containers_per_pcs
    sections = (
        max(1, math.ceil(total_energy_mwh / (container_energy_mwh * containers_per_section)))
        if container_energy_mwh > 0
        else 1
    )
    recommended_stages = max(2, min(4, sections // 4)) if sections > 1 else 1
    power_per_stage = total_power_mw / recommended_stages
    energy_per_stage = total_energy_mwh / recommended_stages

    stages = []
    for i in range(recommended_stages):
        stages.append({
            "stage": i + 1,
            "power_mw": round(power_per_stage, 1),
            "energy_mwh": round(energy_per_stage, 1),
            "sections": max(1, sections // recommended_stages),
            "estimated_date": f"2027-Q{(i*2)+1}",
        })

    dc_breaker_count = pcs_count * racks_per_cluster
    dc_fuse_count = total_containers * racks_per_container

    topology = {
        "levels": [
            {"name": "电芯", "count": cell_series, "unit": "串联"},
            {"name": "模组", "count": module_series, "unit": "串/模组"},
            {"name": "电池包", "count": modules_per_rack, "unit": "包/机架"},
            {"name": "机架", "count": racks_per_cluster, "unit": "架/簇"},
            {"name": "集装箱", "count": racks_per_container, "unit": "架/箱"},
            {"name": "PCS", "count": containers_per_pcs, "unit": "箱/PCS"},
            {"name": "分段", "count": sections, "unit": "总段数"},
            {"name": "PCS总数", "count": pcs_count, "unit": "台"},
        ],
        "total_cells": cell_series * modules_per_rack * racks_per_cluster * racks_per_container * containers_per_pcs * pcs_count,
        "total_containers": total_containers,
        "total_racks": total_containers * racks_per_container,
    }

    return {
        "total_power_mw": total_power_mw,
        "total_energy_mwh": total_energy_mwh,
        "duration_hours": round(duration_hours, 2),
        "architecture_type": arch_type,
        "coupling_type": coupling,
        "cell_to_module": cell_series,
        "module_to_pack": module_series,
        "pack_to_rack": modules_per_rack,
        "rack_to_cluster": racks_per_cluster,
        "cluster_to_container": racks_per_container,
        "container_to_section": containers_per_pcs,
        "section_to_stage": sections,
        "stage_count": recommended_stages,
        "stages": stages,
        "pcs_count": pcs_count,
        "pcs_power_mw": pcs_power_mw,
        "pcs_topology": "distributed" if arch_type == "string" else "centralized",
        "dc_bus_voltage": round(dc_bus_voltage, 0),
        "dc_breaker_count": dc_breaker_count,
        "dc_fuse_count": dc_fuse_count,
        "topology_data": topology,
        "rack_energy_kwh": round(rack_energy_kwh, 2),
        "container_energy_mwh": round(container_energy_mwh, 2),
        "total_containers": total_containers,
    }


