from django.db import models

# Create your models here.

class User(models.Model):
    ROLE_CHOICES = [
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
    ]
    user_id = models.BigIntegerField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
