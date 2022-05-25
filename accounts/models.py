from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from accounts.managers import CustomUserManager
from django.contrib.auth.models import PermissionsMixin
# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(_('email address'),max_length=254, unique=True)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30)
    Mobile = models.CharField(max_length=13,blank=True)
    Aadhaar = models.CharField(max_length=12,blank=True)
    is_blo = models.BooleanField(default=False)
    is_voter = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
    
class OtpModel(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)

class TempimageHolder(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
    Photo = models.ImageField(upload_to='tempimages/')