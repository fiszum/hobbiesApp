from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Hobby, Thread
# Register your models here.


# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Add fields to display in the admin list view
    list_display = ['username', 'email', 'date_of_birth', 'is_staff']

    # Add fields to the 'change' form in admin
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_of_birth', 'hobbies')}),
    )



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Hobby)
admin.sitr.register(Thread)