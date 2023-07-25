from django.db import models
from django.contrib.auth.models import User

class VotingPoint(models.Model):
    name = models.CharField(max_length=200)
    longitude = models.DecimalField(max_digits=9, decimal_places=6) 
    latitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.name
    
class Voter(models.Model):
    nuip = models.CharField(max_length=11, unique=True)
    fullName = models.CharField(max_length=100)
    quarter = models.CharField(max_length=50)
    numberPhone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    votingPoint = models.ForeignKey(VotingPoint,on_delete=models.CASCADE)
    
    coordinator = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.fullName