from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Leaves(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    leave_reason = models.CharField(max_length=25)
    leave_type = models.CharField(max_length=10)
    leave_from_date = models.DateField(default=timezone.now)
    leave_to_date = models.DateField(default=timezone.now)
    applied_leaves = models.FloatField(default=0)
    choices= (('pending','pending'),('approved','approved'),('rejected','rejected'),('cancelled','cancelled'))
    status = models.CharField(max_length=10, choices=choices)

    def __str__(self):
        return self.user


class Attendence(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    in_time = models.TimeField(null=True)
    out_time = models.TimeField(null=True)
    working_hour = models.TextField(max_length=20,null=True)
    punch_in = models.BooleanField(default=False)

    def __str__(self):
        return self.user