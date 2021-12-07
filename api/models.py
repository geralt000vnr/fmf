from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Stations(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500, null=False, blank=False)
    vendor = models.ForeignKey(User, related_name='vendor', null=False, on_delete=models.CASCADE)
    timing = models.TextField(null=False, blank=False)
    address = models.TextField(null=False, blank=False)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    cng_available = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
