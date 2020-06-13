from django.db import models

from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class UserDetails(models.Model):
    name = models.CharField(max_length=250, null=False)
    phone = PhoneNumberField(null=False, blank=False)
    email_field = models.EmailField(max_length=254, unique=True)
    # This is okay for simplicity for now but other-ways we should be encoding or using a salt to save passwords
    password = models.CharField(max_length=254)


class SocialLoginDetails(models.Model):
    user = models.ForeignKey('users.UserDetails', null=True, on_delete=models.SET_NULL)
    provider_social = models.CharField(max_length=250, default="", unique=True)
    meta = models.CharField(max_length=250, null=True)
