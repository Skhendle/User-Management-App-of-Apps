from django.db import models
from django.contrib.auth.models import User, Group, Permission

from django.core.exceptions import PermissionDenied

import uuid


class BaseModel(models.Model):
    """
    Abstract base model that includes:
    - JSONField for dynamic data storage
    - Timestamp fields for tracking creation, updates, and soft deletion
    """
    data = models.JSONField(default=dict)  # JSON column
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)
    deleted_ts = models.DateTimeField(null=True, blank=True)  # Soft delete field

    class Meta:
        abstract = True  # Ensures this model is not created as a table


def generate_api_key():
    return uuid.uuid4().hex  # Generates a new unique API key every time

class Application(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="applications"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    API_KEY = models.CharField(
        max_length=255,
        unique=True,
        default=generate_api_key,  # Call the function instead of setting a fixed value
        editable=False
    )

    def __str__(self):
        return f"{self.name} - {self.user.username}"

    def save(self, *args, **kwargs):
        """ Ensure only users with the correct role can create applications """
        if not self.user.groups.filter(name="developer").exists():
            raise PermissionDenied("User does not have permission to create applications.")
        super().save(*args, **kwargs)



class Role(BaseModel):
    """
    Defines roles that belong to a specific application.
    """
    application = models.ForeignKey(
        Application, 
        on_delete=models.CASCADE, 
        related_name="roles"
    )
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    # FIX: Add ManyToMany relationship with Permission
    permissions = models.ManyToManyField('AppPermission', related_name="roles")

    class Meta:
        unique_together = ('application', 'name')

    def __str__(self):
        return f"{self.name} ({self.application.name})"

    def save(self, *args, **kwargs):
        """ Ensure only users with the correct role can create applications """
        if not self.application.user.groups.filter(name="developer").exists():
            raise PermissionDenied("User does not have permission to create applications.")
        super().save(*args, **kwargs)


class AppPermission(BaseModel):
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="permissions"
    )
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('application', 'name')

    def __str__(self):
        return f"{self.name} ({self.application.name})"

    def save(self, *args, **kwargs):
        """ Ensure only users with the correct role can create applications """
        if not self.application.user.groups.filter(name="developer").exists():
            raise PermissionDenied("User does not have permission to create applications.")
        super().save(*args, **kwargs)


class ApplicationUser(BaseModel):
    """
    Links users to applications and assigns them a role that belongs to that application.
    """
    application = models.ForeignKey(
        Application, 
        on_delete=models.CASCADE, 
        related_name="app_users"
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="app_memberships"
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT,  # Prevent deletion of a role if assigned
        related_name="role_users"
    )

    class Meta:
        unique_together = ('application', 'user')  # Prevent duplicate user-application pair

    def __str__(self):
        return f"{self.user.username} - {self.application.name} ({self.role.name})"
