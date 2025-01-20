from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.


class PageView(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Page view count: {self.count}"

class Hobby(models.Model):
    name = models.CharField(max_length=100)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.name
    
class CustomUser(AbstractUser):
    friends = models.ManyToManyField('self', blank=True, symmetrical=True)
    # Inherited fields: username, email, password, first_name, last_name, etc.
    email = models.EmailField(unique=True)  # Enforce unique email addresses
    date_of_birth = models.DateField(null=True, blank=True)  # Optional field
    hobbies = models.ManyToManyField('Hobby', blank=True, related_name='users')  # Many-to-many with Hobby

    def __str__(self):
        return self.username
class FriendRequest(models.Model):
    # Define status choices
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]

    # ForeignKey fields to represent users sending and receiving the requests
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_requests', on_delete=models.CASCADE)
    
    # A status field to track the state of the request
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    # Timestamp of when the request was created
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevent duplicate requests between the same users
        unique_together = ('from_user', 'to_user')  

    def __str__(self):
        return f"{self.from_user} -> {self.to_user} ({self.status})"
    
class Thread (models.Model):
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='threads')
    content 
    created_at = models.DateTimeField(auto_now_add=True)