from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static
from django.contrib.auth.models import AbstractUser

class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
class RegisterCheck(models.Model):
    email = models.EmailField(unique=True, blank=True, null=True)
    time = models.TimeField(blank=True, null=True, auto_now_add=True)
    code = models.IntegerField(blank=True, null=True)
    password = models.CharField(max_length=150, blank=True, null=True)
    count = models.IntegerField(default=0)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)

class Follow(models.Model):
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    is_following = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.following.name} -> {self.follower.name}'

class Avatar(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='images_set')
    image = models.ImageField(upload_to='avatar/')
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.title}"





