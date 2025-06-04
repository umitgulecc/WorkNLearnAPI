from app.models.user import User


def is_admin(user: User) -> bool:
    return user.role and user.role.name == "admin"

def is_manager(user: User) -> bool:
    return user.role and user.role.name == "manager"

def is_employee(user: User) -> bool:
    return user.role and user.role.name == "employee"

def has_access_to_user(viewer: User, target: User) -> bool:
    """
    viewer → current_user
    target → erişilmek istenen kullanıcı
    """
    if viewer.id == target.id:
        return True
    if is_admin(viewer):
        return True
    if is_manager(viewer) and viewer.department_id == target.department_id:
        return True
    return False
