from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'student_number', 'lecturer_number', 'registrar_number']
    search_fields = ['username', 'email']

admin.site.register(User, UserAdmin)
