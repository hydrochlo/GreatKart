from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

# Register your models here.
# admin.site.register(Account)

# Way->1 to make any field read only
# @admin.register(Account)
# class AccountAdmin(admin.ModelAdmin):
#     readonly_fields = ("password","is_admin")

class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'is_active', 'date_joined')
    list_display_links = ('email', 'first_name', 'last_name', 'username',) # this will make the provided fields links to visit.
    
    
    filter_horizontal = ()
    list_filter = ('is_active',)
    # fieldsets = ()
    add_fieldsets = ()

admin.site.register(Account, AccountAdmin)
