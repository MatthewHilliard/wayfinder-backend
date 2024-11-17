from django.db import models
import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.db import models

class CustomUserManager(UserManager):
    def _create_user(self, name, email, password, **extra_fields):
        """
        Create and save a user with the given name, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        # Normalize the email
        email = self.normalize_email(email)
        # Create the user
        user = self.model(email=email, name=name, **extra_fields)
        # Set the user's password
        user.set_password(password)
        # Save the user
        user.save(using=self._db)
        return user
    
    def create_user(self, name=None, email=None, password=None, **extra_fields):
        """
        Create and save a regular user with the given name, email, and password.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(name, email, password, **extra_fields)
    
    def create_superuser(self, name=None, email=None, password=None, **extra_fields):
        """
        Create and save a superuser with the given name, email, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(name, email, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    # Location here
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name',]

    def __str__(self):
        return self.email