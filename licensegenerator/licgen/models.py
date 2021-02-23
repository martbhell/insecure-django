from django.db import models

from django.contrib.auth.models import User

# Create your models here.

# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
# TODO: Define signals to create/update Profile  ?
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    social_security = models.CharField(max_length=13, unique=True)
    num_licenses = models.IntegerField(default=10)
    admin = models.BooleanField(default=False)

class License(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    licenseid = models.CharField(max_length=32, unique=True)
    mac_address = models.CharField(max_length=18)
    created_at = models.DateTimeField('creation date', auto_now_add=True)
    # TODO: autoadd now + 1y ? Or do this in code?
    expire_at = models.DateTimeField('expiration date')
