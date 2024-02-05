"""
Django admin customization
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from core import models


class SellerAdmin(UserAdmin):
    """Define the admin pages for sellers."""
    ordering = ['id']
    list_display = ['email', 'name', 'about']
    fieldsets = (
        (None, {'fields': ('email', 'name', 'password', 'about')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser'
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'name',
                'about',
                'password1',
                'password2',
                'is_active',
                'is_staff',
                'is_superuser'
            )
        }),
    )


admin.site.register(models.Seller, SellerAdmin)
admin.site.register(models.CreditRequest)
admin.site.register(models.ChargeRequest)