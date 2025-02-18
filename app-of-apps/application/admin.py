from django.contrib import admin
from application.models import Application, Role, AppPermission, ApplicationUser


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'API_KEY', 'created_ts', 'updated_ts', 'deleted_ts')
    readonly_fields = ('API_KEY', 'created_ts', 'updated_ts', 'deleted_ts')
    search_fields = ('name',)
    ordering = ('-created_ts',)
    fieldsets = (
        (None, {'fields': ('name', 'description')}),
        ('Timestamps', {'fields': ('created_ts', 'updated_ts', 'deleted_ts'), 'classes': ('collapse',)}),
        ('API Key', {'fields': ('API_KEY',), 'classes': ('collapse',)}),
    )


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'application', 'created_ts', 'updated_ts', 'deleted_ts')
    search_fields = ('name', 'application__name')
    list_filter = ('application',)
    ordering = ('-created_ts',)
    readonly_fields = ('created_ts', 'updated_ts', 'deleted_ts')
    fieldsets = (
        (None, {'fields': ('name', 'application', 'description')}),
        ('Timestamps', {'fields': ('created_ts', 'updated_ts', 'deleted_ts'), 'classes': ('collapse',)}),
    )


@admin.register(AppPermission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'application', 'created_ts', 'updated_ts', 'deleted_ts')
    search_fields = ('name', 'application__name')
    list_filter = ('application',)
    ordering = ('-created_ts',)
    readonly_fields = ('created_ts', 'updated_ts', 'deleted_ts')
    fieldsets = (
        (None, {'fields': ('name', 'application', 'description')}),
        ('Timestamps', {'fields': ('created_ts', 'updated_ts', 'deleted_ts'), 'classes': ('collapse',)}),
    )


@admin.register(ApplicationUser)
class ApplicationUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'application', 'role', 'created_ts', 'updated_ts', 'deleted_ts')
    search_fields = ('user__username', 'application__name', 'role__name')
    list_filter = ('application', 'role', 'created_ts')
    ordering = ('-created_ts',)
    readonly_fields = ('created_ts', 'updated_ts', 'deleted_ts')
    fieldsets = (
        (None, {'fields': ('user', 'application', 'role')}),
        ('Timestamps', {'fields': ('created_ts', 'deleted_ts'), 'classes': ('collapse',)}),
    )
