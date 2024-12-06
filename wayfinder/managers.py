from django.contrib.auth.models import UserManager

class CustomUserManager(UserManager):
    def _create_user(self, name, email, password, **extra_fields):
        """
        Create and save a user with the given name, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set') # Raise an error if the email is not provided
        email = self.normalize_email(email) # Normalize the email
        user = self.model(email=email, name=name, **extra_fields) # Create the user object with the given email and name
        user.set_password(password) # Set the user's password
        user.save(using=self._db) # Save the user object
        return user
    
    def create_user(self, name=None, email=None, password=None, **extra_fields):
        """
        Create and save a regular user with the given name, email, and password.
        """
        extra_fields.setdefault('is_staff', False) # Set the is_staff field to False by default
        extra_fields.setdefault('is_superuser', False) # Set the is_superuser field to False by default
        return self._create_user(name, email, password, **extra_fields) # Call the _create_user method
    
    def create_superuser(self, name=None, email=None, password=None, **extra_fields):
        """
        Create and save a superuser with the given name, email, and password.
        """
        extra_fields.setdefault('is_staff', True) # Set the is_staff field to True by default
        extra_fields.setdefault('is_superuser', True) # Set the is_superuser field to True by default
        return self._create_user(name, email, password, **extra_fields) # Call the _create_user method
