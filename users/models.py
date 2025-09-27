from django.contrib.auth.models import AbstractUser
from django.db import models
from lawyer.models import LawCategory

# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = (
    ('client', 'Client'),
    ('lawyer', 'Lawyer')
    )
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    categories = models.ManyToManyField(LawCategory, blank=True)


    def __str__(self):
        return f"{self.username} ({self.role})"
