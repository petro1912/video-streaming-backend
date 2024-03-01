from django.contrib import admin
from app_auth.models import Account
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('id', 'email', 'fullname', 'date_joined', 'is_admin', 'is_active')
    search_fields = ('email', 'fullname')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    ordering = ('id','email',)
    fieldsets = (
        (None)
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'fullname', 'password1', 'password2'),
        }),
    )

admin.site.register(Account,AccountAdmin)
