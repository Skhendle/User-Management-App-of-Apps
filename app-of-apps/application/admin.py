from django.contrib import admin
from application.models import Application


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


admin.site.register(Application, ApplicationAdmin)


# Register your models here.
