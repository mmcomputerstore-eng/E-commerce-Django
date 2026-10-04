from django.contrib import admin
from userauth.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_vendor', 'is_staff', 'is_superuser']
    list_editable = ['is_vendor']
    list_filter = ['is_vendor', 'is_staff', 'is_superuser']
    search_fields = ['username', 'email']

admin.site.register(User, UserAdmin)
