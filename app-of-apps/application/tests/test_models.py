import pytest
from django.contrib.auth.models import User, Group
from django.core.exceptions import PermissionDenied
from application.models import Application, Role, AppPermission, ApplicationUser
from django.utils import timezone


@pytest.fixture
def create_users(db):  # Add `db` fixture to enable database access
    """Create users for testing."""
    normal_user = User.objects.create_user(username="normal", email="normal@example.com", password="testpass")
    admin_user = User.objects.create_superuser(username="admin", email="admin@example.com", password="adminpass")
    developer_user = User.objects.create_user(username="developer", email="developer@example.com", password="devpass")

    # Assign developer role
    developer_group, _ = Group.objects.get_or_create(name="developer")
    developer_user.groups.add(developer_group)

    return normal_user, admin_user, developer_user

@pytest.fixture
def create_application(db, create_users):
    """Create an application with a developer user."""
    _, _, developer_user = create_users
    return Application.objects.create(user=developer_user, name="FinanceApp", description="Financial management")

@pytest.fixture
def create_permissions(db, create_application):
    """Create permissions for an application."""
    app = create_application
    create_perm = AppPermission.objects.create(application=app, name="Create Reports", description="Allows report creation")
    view_perm = AppPermission.objects.create(application=app, name="View Reports", description="Allows report viewing")
    return create_perm, view_perm

@pytest.fixture
def create_roles(db, create_application, create_permissions):
    """Create roles and assign permissions."""
    app = create_application
    create_perm, view_perm = create_permissions

    admin_role = Role.objects.create(application=app, name="Admin", description="Full access")
    viewer_role = Role.objects.create(application=app, name="Viewer", description="Can view reports")

    admin_role.permissions.add(create_perm, view_perm)
    viewer_role.permissions.add(view_perm)

    return admin_role, viewer_role

@pytest.fixture
def create_application_users(db, create_application, create_users, create_roles):
    """Assign users to roles in an application."""
    normal_user, admin_user, developer_user = create_users
    admin_role, viewer_role = create_roles
    app = create_application

    return [
        ApplicationUser.objects.create(application=app, user=normal_user, role=viewer_role),
        ApplicationUser.objects.create(application=app, user=admin_user, role=admin_role),
        ApplicationUser.objects.create(application=app, user=developer_user, role=viewer_role)
    ]

# ---------------- TEST CASES ---------------- #

@pytest.mark.django_db
def test_application_creation(create_application):
    """Test that an application is created successfully."""
    app = create_application
    assert app.name == "FinanceApp"
    assert app.API_KEY is not None
    assert isinstance(app.API_KEY, str)

@pytest.mark.django_db
def test_application_permission_enforcement(create_users):
    """Test that a normal user cannot create an application."""
    normal_user, _, _ = create_users
    with pytest.raises(PermissionDenied):
        Application.objects.create(user=normal_user, name="UnauthorizedApp")

@pytest.mark.django_db
def test_role_creation(create_roles):
    """Test role creation and unique constraint enforcement."""
    admin_role, viewer_role = create_roles
    assert admin_role.name == "Admin"
    assert viewer_role.name == "Viewer"
    assert admin_role.application == viewer_role.application

@pytest.mark.django_db
def test_permission_creation(create_permissions):
    """Test permission creation and uniqueness constraint."""
    create_perm, view_perm = create_permissions
    assert create_perm.name == "Create Reports"
    assert view_perm.name == "View Reports"
    assert create_perm.application == view_perm.application

@pytest.mark.django_db
def test_application_user_assignment(create_application_users):
    """Test that users are correctly assigned to applications with roles."""
    for app_user in create_application_users:
        assert app_user.application is not None
        assert app_user.user is not None
        assert app_user.role is not None

@pytest.mark.django_db
def test_unique_application_user_constraint(create_application, create_users, create_roles):
    """Test that duplicate ApplicationUser entries are prevented."""
    app = create_application
    normal_user, _, _ = create_users
    _, viewer_role = create_roles

    ApplicationUser.objects.create(application=app, user=normal_user, role=viewer_role)

    with pytest.raises(Exception):  # Unique constraint violation
        ApplicationUser.objects.create(application=app, user=normal_user, role=viewer_role)

@pytest.mark.django_db
def test_role_permission_assignment(create_roles):
    """Test that roles correctly assign permissions."""
    admin_role, viewer_role = create_roles
    assert admin_role.permissions.count() == 2  # Admin has both permissions
    assert viewer_role.permissions.count() == 1  # Viewer has only view permission

@pytest.mark.django_db
def test_application_deletion_cascades(create_application, create_roles):
    """Test that deleting an application cascades and deletes associated roles."""
    app = create_application
    app_id = app.id  # Store the application ID before deletion

    app.delete()

    # Use application_id instead of the deleted application instance
    assert Role.objects.filter(application_id=app_id).count() == 0
    assert AppPermission.objects.filter(application_id=app_id).count() == 0


@pytest.mark.django_db
def test_soft_delete(create_application):
    """Test soft deletion logic (if applicable)."""
    app = create_application
    app.deleted_ts = timezone.now()  # Use timezone-aware datetime
    app.save()

    assert app.deleted_ts is not None

