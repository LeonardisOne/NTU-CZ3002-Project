from django.db import models

# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length = 128)
    password = models.CharField(max_length = 32)
    last_name = models.CharField(max_length = 128)
