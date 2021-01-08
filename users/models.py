from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Books(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.IntegerField()
