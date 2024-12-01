from django.db import models
from django.conf import settings
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager

'''Location model for the application'''
class Location(models.Model):
    location_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    country = models.ForeignKey('cities_light.Country', on_delete=models.SET_NULL, null=True)
    region = models.ForeignKey('cities_light.Region', on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey('cities_light.City', on_delete=models.SET_NULL, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        if self.city is not None:
            return f"{self.city.name}, {self.city.region.name if self.city.region else 'Unknown Region'}, {self.city.country.name if self.city.country else 'Unknown Country'}"
        elif self.region is not None:
            return f"{self.region.name}, {self.region.country.name if self.region.country else 'Unknown Country'}"
        elif self.country is not None:
            return f"{self.country.name}"
        else:
            return "Unknown Location"

'''User model for the a pplication'''
class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    country = models.ForeignKey('cities_light.Country', on_delete=models.SET_NULL, null=True, blank=True) 
    city = models.ForeignKey('cities_light.City', on_delete=models.SET_NULL, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name',]

    def __str__(self):
        return self.email

'''Experience model for the application'''
class Experience(models.Model):
    experience_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='experiences')
    creator = models.ForeignKey('User', on_delete=models.CASCADE, related_name='created_experiences')
    average_rating = models.FloatField(default=0.0)
    number_of_ratings = models.PositiveIntegerField(default=0)
    date_posted = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', related_name='experiences')
    image = models.ImageField(upload_to='experience_images/', blank=True, null=True)
    price = models.CharField(
        max_length=10,
        choices=[
            ('free', 'Free'),
            ('cheap', 'Cheap'),
            ('moderate', 'Moderate'),
            ('expensive', 'Expensive'),
        ],
        blank=True,
        null=True
    )
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title

'''Tip model for the application'''
class Tip(models.Model):
    tip_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    country = models.ForeignKey('cities_light.Country', on_delete=models.SET_NULL, null=True, blank=True) 
    city = models.ForeignKey('cities_light.City', on_delete=models.SET_NULL, null=True, blank=True)
    creator = models.ForeignKey('User', on_delete=models.CASCADE, related_name='created_tips')
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

'''Wishlist model for the application'''
class Wishlist(models.Model):
    wishlist_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='wishlists')
    title = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.user.name}"

'''WishlistItem model for the application'''
class WishlistItem(models.Model):
    wishlist_item_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wishlist = models.ForeignKey('Wishlist', on_delete=models.CASCADE, related_name='items')
    experience = models.ForeignKey('Experience', on_delete=models.CASCADE, related_name='wishlist_items')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.experience.title} in {self.wishlist.title}"

'''Rating model for the application'''
class Rating(models.Model):
    rating_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='ratings')
    experience = models.ForeignKey('Experience', on_delete=models.CASCADE, related_name='ratings')
    comment = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    rating_value = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return f"Rating by {self.user.name} on {self.experience.title}"

'''Tag model for the application'''
class Tag(models.Model):
    tag_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
