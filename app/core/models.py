"""
Database models.
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    # Basic attributes
    age = models.PositiveIntegerField(blank=True, null=True)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    
    # Additional body composition attributes
    body_fat_percentage = models.FloatField(null=True, blank=True)
    muscle_mass = models.FloatField(null=True, blank=True)
    bone_density = models.FloatField(null=True, blank=True)
    waist_circumference = models.FloatField(null=True, blank=True)
    hip_circumference = models.FloatField(null=True, blank=True)
    
    # BMI interpretation choices
    UNDERWEIGHT = 'Underweight'
    NORMAL_WEIGHT = 'Normal weight'
    OVERWEIGHT = 'Overweight'
    OBESITY = 'Obesity'
    
    BMI_CHOICES = [
        (UNDERWEIGHT, 'Underweight'),
        (NORMAL_WEIGHT, 'Normal weight'),
        (OVERWEIGHT, 'Overweight'),
        (OBESITY, 'Obesity')
    ]
    
    bmi_interpretation = models.CharField(
        max_length=15,
        choices=BMI_CHOICES,
        blank=True,
        null=True
    )
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    
    @property
    def bmi(self):
        if self.height and self.weight:
            height_in_meters = self.height / 100
            return self.weight / (height_in_meters ** 2)
        return None
    
    def save(self, *args, **kwargs):
        self.set_bmi_interpretation()
        super().save(*args, **kwargs)
    
    def set_bmi_interpretation(self):
        bmi_value = self.bmi
        if bmi_value is None:
            self.bmi_interpretation = None
        elif bmi_value < 18.5:
            self.bmi_interpretation = self.UNDERWEIGHT
        elif 18.5 <= bmi_value < 24.9:
            self.bmi_interpretation = self.NORMAL_WEIGHT
        elif 25 <= bmi_value < 29.9:
            self.bmi_interpretation = self.OVERWEIGHT
        else:
            self.bmi_interpretation = self.OBESITY

class Recipe(models.Model):
    """Recipe object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField(null=True, blank=True)
    calories = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField('Tag')
    ingredients = models.ManyToManyField('Ingredient')

    def __str__(self):
        return self.title


class Tag(models.Model):
    """Tag for filtering recipes."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredients for recipe."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
