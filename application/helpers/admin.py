from application.models import UserModel


def create_superadmin():
    """Check if super admin exists in database or create as necessary"""
    super_admin = UserModel.find_by_username("admin")

    if not super_admin:
        # create superadmin with default creds
        new_admin = UserModel("admin", "admin", "admin@admin.com", True)
        new_admin.save()
