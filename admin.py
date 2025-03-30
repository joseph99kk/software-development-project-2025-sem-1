from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Department, Issue, Category, Registration, Activity

# Custom User Admin
@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', )
    list_filter = ('name',)

# Issue Admin
@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'department', 'user', 'status', 'priority', 'category', 'created_by', 'assigned_to', 'affected_course', 'affected_student', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'department__name', 'user__username', 'status', 'priority', 'category__name', 'created_by__username', 'assigned_to__username', 'affected_course', 'affected_student')
    list_filter = ('status', 'priority', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    readonly_fields = ('Issue_id',)

# Activity Admin
@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('issue', 'user', 'action', 'details', 'timestamp')
    search_fields = ('issue__title', 'user__username', 'action', 'details')
    list_filter = ('action', 'timestamp')
    date_hierarchy = 'timestamp'

# Registration Admin
@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username', 'user__email')
    date_hierarchy = 'created_at'