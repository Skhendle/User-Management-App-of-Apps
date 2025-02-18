from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from application.models import Application, Role, AppPermission, ApplicationUser


class Command(BaseCommand):
    help = "Populates the database with initial test data"

    def handle(self, *args, **kwargs):
        self.stdout.write("📌 Populating database...")

        # Create Users
        normal_user, admin_user, developer_user = self.create_users()

        # Create Developer Group and Assign Permissions
        developer_group = self.create_group_with_permissions("developer", [Application, Role, AppPermission, ApplicationUser])
        developer_user.groups.add(developer_group)

        # Create Application
        app = self.create_application(developer_user)

        # Create Permissions
        create_perm, view_perm = self.create_permissions(app)

        # Create Roles and Assign Permissions
        admin_role, viewer_role = self.create_roles(app, create_perm, view_perm)

        # Assign Users to Roles
        self.assign_users_to_roles(app, normal_user, admin_user, developer_user, admin_role, viewer_role)

        self.stdout.write(self.style.SUCCESS("✅ Database population completed!"))

    def create_users(self):
        """Create and return test users."""
        normal_user = User.objects.create_user(username="normal", email="normal@example.com", password="normalpass")
        admin_user = User.objects.create_superuser(username="admin", email="admin@example.com", password="adminpass")
        developer_user = User.objects.create_user(username="developer", email="developer@example.com", password="devpass")
        return normal_user, admin_user, developer_user

    def create_group_with_permissions(self, group_name, models):
        """Create a group and assign CRUD permissions on the given models."""
        group, _ = Group.objects.get_or_create(name=group_name)
        for model in models:
            content_type = ContentType.objects.get_for_model(model)
            permissions = Permission.objects.filter(content_type=content_type)
            group.permissions.add(*permissions)
        return group

    def create_application(self, user):
        """Create an application assigned to a user."""
        return Application.objects.create(user=user, name="FinanceApp", description="Manage financial data")

    def create_permissions(self, app):
        """Create and return custom application permissions."""
        create_perm = AppPermission.objects.create(
            application=app, name="Can Create Financial Reports", description="Allowed to add financial data"
        )
        view_perm = AppPermission.objects.create(
            application=app, name="Can View Financial Reports", description="Allowed to view financial data"
        )
        return create_perm, view_perm

    def create_roles(self, app, create_perm, view_perm):
        """Create roles and assign permissions."""
        admin_role = Role.objects.create(application=app, name="Admin", description="Full access to the application")
        viewer_role = Role.objects.create(application=app, name="Viewer", description="Can view financial data")

        # Assign Permissions
        admin_role.permissions.add(create_perm, view_perm)
        viewer_role.permissions.add(view_perm)

        return admin_role, viewer_role

    def assign_users_to_roles(self, app, normal_user, admin_user, developer_user, admin_role, viewer_role):
        """Assign users to their respective roles."""
        ApplicationUser.objects.create(application=app, user=normal_user, role=viewer_role)
        ApplicationUser.objects.create(application=app, user=admin_user, role=admin_role)
        ApplicationUser.objects.create(application=app, user=developer_user, role=viewer_role)
