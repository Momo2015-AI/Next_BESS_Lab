"""统一 API 响应格式工具

提供标准化的成功/失败/分页响应，确保所有端点返回一致的结构：
{
    "success": true/false,
    "data": ...,
    "error": null/"错误信息",
    "message": "操作描述"
}
"""

from flask import jsonify


def success_response(data=None, message="操作成功", status_code=200):
    """成功响应

    Args:
        data: 响应数据
        message: 提示消息
        status_code: HTTP 状态码

    Returns:
        (flask.Response, int)
    """
    return (
        jsonify({"success": True, "data": data, "error": None, "message": message}),
        status_code,
    )


def error_response(error, message=None, status_code=400):
    """失败响应

    Args:
        error: 错误描述
        message: 额外提示（可选）
        status_code: HTTP 状态码

    Returns:
        (flask.Response, int)
    """
    return (
        jsonify({"success": False, "data": None, "error": error, "message": message or error}),
        status_code,
    )


def paginated_response(items, page, page_size, total, message="查询成功"):
    """分页响应

    Args:
        items: 当前页数据列表
        page: 当前页码（从 1 开始）
        page_size: 每页数量
        total: 总记录数
        message: 提示消息

    Returns:
        (flask.Response, int)
    """
    total_pages = (total + page_size - 1) // page_size if page_size > 0 else 0
    return (
        jsonify(
            {
                "success": True,
                "data": items,
                "error": None,
                "message": message,
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "total": total,
                    "total_pages": total_pages,
                },
            }
        ),
        200,
    )
