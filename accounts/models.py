from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.timezone import now

# User Roles
class UserRoles(models.TextChoices):
    SUPERADMIN = "superadmin", "Super Admin"
    DOCTOR = "doctor", "Doctor"
    PATIENT = "patient", "Patient"

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, name, password=None):
        """Create a regular user"""
        if not email:
            raise ValueError("The Email field is required")
        if not username:
            raise ValueError("The Username field is required")
        if not name:
            raise ValueError("The  Name field is required")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, name, password=None):
        """Create a superadmin user"""
        user = self.create_user(email, username, name, password)
        user.is_staff = True
        user.is_superuser = True
        user.role = UserRoles.SUPERADMIN
        user.save(using=self._db)
        return user

# Custom User Model
class Accounts(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=50)
    
    address = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=UserRoles.choices, default=UserRoles.PATIENT)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=now)
    last_login = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']

    def __str__(self):
        return f"{self.username} ({self.role})"

    def set_password(self, raw_password):
        """Use Django's built-in password hashing"""
        super().set_password(raw_password)
        self.save()


