from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.TextField(max_length=50)
    leaves = models.FloatField(default=12)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    