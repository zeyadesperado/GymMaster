from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

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
    MALE = 'M'
    FEMALE = 'F'

    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female')
    ]

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)

    # Basic attributes
    age = models.PositiveIntegerField(blank=True, null=True)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    picture = models.ImageField(upload_to='pictures/', null=True, blank=True)

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
    caloric_needs = models.FloatField(null=True, blank=True,)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    @property
    def bmi(self):
        if self.height and self.weight:
            height_in_meters = self.height / 100
            return self.weight / (height_in_meters ** 2)
        return None

    def save(self, *args, **kwargs):
        self.set_bmi_interpretation()
        self.daily_caloric_needs()
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

    def daily_caloric_needs(self):
        if self.weight and self.height and self.age and self.gender:
            if self.gender == self.MALE:
                # Mifflin-St Jeor Equation for men
                bmr = 10 * self.weight + 6.25 * self.height - 5 * self.age + 5
            else:
                # Mifflin-St Jeor Equation for women
                bmr = 10 * self.weight + 6.25 * self.height - 5 * self.age - 161
            
            # Assuming a sedentary activity level (can be adjusted)
            self.caloric_needs = bmr * 1.2 
                

class Recipe(models.Model):
    """Recipe object."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField(null=True, blank=True)
    calories = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField('Tag')
    ingredients = models.ManyToManyField('Ingredient')
    picture = models.ImageField(upload_to='recipes/', null=True, blank=True)

    def __str__(self):
        return self.title

class Tag(models.Model):
    """Tag for filtering recipes."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    """Ingredients for recipe."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Supplement(models.Model):
    """Supplement object."""
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    calories = models.IntegerField()
    picture = models.ImageField(upload_to='supplement/', null=True, blank=True)

    def __str__(self):
        return self.name




class Payment(models.Model):
    """Payment object."""

    duration = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.duration} - month'

class Coach(models.Model):
    """Coach object."""
    name = models.CharField(max_length=255)
    bio = models.TextField()
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    picture = models.ImageField(upload_to='coach/', null=True, blank=True)
    certificate = models.ImageField(upload_to='coach/certificate/', null=True, blank=True)

    def __str__(self):
        return self.name


