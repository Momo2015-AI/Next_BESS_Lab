"""EPC 路由共享辅助函数"""

from database import Project, db


def check_project_access(project_id, user):
    """验证用户有权访问该项目（tenant_id 隔离）"""
    if not user:
        return False
    proj = Project.query.get(project_id) if project_id else None
    if not proj:
        return False
    if getattr(user, "role", None) == "admin":
        return True
    return getattr(proj, "tenant_id", None) == getattr(user, "tenant_id", None)


def get_or_404(model, item_id):
    obj = db.session.get(model, item_id)
    return obj if obj else None
