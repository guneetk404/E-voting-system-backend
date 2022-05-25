from django.db import models
from accounts.models import CustomUser

# Create your models here.

class Contestant(models.Model):
    contestno = models.ForeignKey('Contest', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    contestantid = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='images/')
    status = models.BooleanField(default=False)
    party = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Voter(models.Model):
    User = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    Mobile = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100, blank=True)
    Name = models.CharField(max_length=100)
    FatherName = models.CharField(max_length=100)
    Gender = models.CharField(max_length=20)
    Address = models.TextField()
    City = models.CharField(max_length=50)
    State = models.CharField(max_length=50)
    Pincode = models.CharField(max_length=20)
    Aadhaar = models.CharField(max_length=12)
    Photo = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return self.Name


class Contest(models.Model):
    contestno = models.CharField(max_length=100)
    electiontype = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    result= models.BooleanField(default=False)

    def __str__(self):
        return self.contestno


class Vote(models.Model):
    Voter = models.ForeignKey('Voter', on_delete=models.CASCADE)
    Contestant = models.ForeignKey('Contestant', on_delete=models.CASCADE)
    Contest = models.ForeignKey('Contest', on_delete=models.CASCADE)
    Points = models.IntegerField(default=0)
