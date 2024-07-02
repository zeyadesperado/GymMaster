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
    list_display = [
        'id', 'email', 'name', 'is_active', 'is_staff', 'is_superuser', 'gender', 'age',
        'weight', 'height', 'phone', 'bmi_interpretation', 'activity_level', 'caloric_needs'
    ]
    list_filter = [
        'is_active', 'is_staff', 'is_superuser', 'gender', 'activity_level'
    ]
    search_fields = ['email', 'name', 'phone']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name', 'gender', 'age', 'phone', 'picture')}),
        (_('Physical Info'), {
            'fields': (
                'weight', 'height', 'body_fat_percentage', 'muscle_mass', 'bone_density',
                'waist_circumference', 'hip_circumference'
            )
        }),
        (_('Health Info'), {
            'fields': ('bmi_interpretation', 'activity_level', 'caloric_needs')
        }),
        (_('Payment Info'), {'fields': ('payment_start_date', 'payment_end_date')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important Dates'), {'fields': ('last_login', )}),
    )
    readonly_fields = ['last_login', 'bmi_interpretation', 'caloric_needs']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2', 'name', 'gender', 'age', 'phone', 'picture',
                'weight', 'height', 'body_fat_percentage', 'muscle_mass', 'bone_density',
                'waist_circumference', 'hip_circumference', 'activity_level', 'is_active',
                'is_staff', 'is_superuser', 'groups', 'user_permissions'
            ),
        }),
    )
    
    
class RecipeAdmin(admin.ModelAdmin):
    """Define the admin pages for recipes."""
    list_display = ['id', 'title', 'user', 'time_minutes', 'calories', 'price']
    list_filter = ['user', 'tags']
    search_fields = ['title']

class TagAdmin(admin.ModelAdmin):
    """Define the admin pages for tags."""
    list_display = ['id', 'name', 'user']
    search_fields = ['name']

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
    list_display = ['id', 'user', 'duration', 'price', 'created_at' ,'user_id']
    list_filter = ['user']
    search_fields = ['user__id']

class CoachAdmin(admin.ModelAdmin):
    """Define the admin pages for coaches."""
    list_display = ['id', 'name', 'price_per_month']
    search_fields = ['name']


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Recipe,RecipeAdmin)
admin.site.register(models.Tag,TagAdmin)
admin.site.register(models.Ingredient,IngredientAdmin)
admin.site.register(models.Payment,PaymentAdmin)
admin.site.register(models.Coach,CoachAdmin)
admin.site.register(models.Supplement,SupplementAdmin)