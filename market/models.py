from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

CONDITION_CHOICES = [
    ('New', 'New'),
    ('Like New', 'Like New'),
    ('Used', 'Used'),
    ('Fair', 'Fair'),
]

class CustomUser(AbstractUser):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class Listing(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    photo = models.ImageField(upload_to='listing_photos/')
    status = models.CharField(max_length=20, default='Available')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} (${self.price})"
    