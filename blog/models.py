from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator, MinLengthValidator

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, validators=[MinLengthValidator(1)])
    body = models.CharField(max_length=255, validators=[MinLengthValidator(1)])
    def __str__(self):
        return self.title
