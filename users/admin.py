from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User, PatientProfile, DoctorProfile, DoctorApplication

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active')
    list_filter = ('is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'address', 'phone_number', 'role', 'nid')
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'nid', 'is_staff', 'is_active')
        }),
    )

    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)

admin.site.register(PatientProfile)
admin.site.register(DoctorProfile)
admin.site.register(DoctorApplication)