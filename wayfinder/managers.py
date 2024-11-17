from django.contrib.auth.models import UserManager

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
