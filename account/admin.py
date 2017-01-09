from django.contrib import admin

from account.models import Account


class UserAdmin(admin.ModelAdmin):
    list_display = [
        'email', 'first_name', 'last_name', 'auth_via'
    ]

    class Meta:
        model = Account


admin.site.register(Account, UserAdmin)
