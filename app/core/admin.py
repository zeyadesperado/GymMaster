"""
Django admin customization
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['id','email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('important_dates'), {'fields': ('last_login',)})
    )
    readonly_fields = ['last_login', ]
    add_fieldsets = (
        [None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }],
    )

class RecipeAdmin(admin.ModelAdmin):
    """Define the admin pages for recipes."""
    list_display = ['id', 'title', 'user', 'time_minutes', 'calories', 'price']
    list_filter = ['user', 'tags']
    search_fields = ['title', 'user__email']

class TagAdmin(admin.ModelAdmin):
    """Define the admin pages for tags."""
    list_display = ['id', 'name', 'user']
    search_fields = ['name', 'user__email']

class IngredientAdmin(admin.ModelAdmin):
    """Define the admin pages for ingredients."""
    list_display = ['id', 'name', 'user']
    search_fields = ['name', 'user__email']

class SupplementAdmin(admin.ModelAdmin):
    """Define the admin pages for supplements."""
    list_display = ['id', 'name', 'price', 'calories']
    search_fields = ['name']

class PaymentAdmin(admin.ModelAdmin):
    """Define the admin pages for payments."""
    list_display = ['id', 'user', 'duration', 'price', 'created_at']
    list_filter = ['user']
    search_fields = ['user__email', 'user__id']

class CoachAdmin(admin.ModelAdmin):
    """Define the admin pages for coaches."""
    list_display = ['id', 'name', 'price_per_month']
    search_fields = ['name']


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Recipe)
admin.site.register(models.Tag)
admin.site.register(models.Ingredient)
admin.site.register(models.Payment)
admin.site.register(models.Coach)
admin.site.register(models.Supplement)