from django.db import models
from django.contrib.auth.models import User


class VotingPoint(models.Model):
    name = models.CharField(max_length=200)
    longitude = models.DecimalField(max_digits=9, decimal_places=6) 
    latitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.name


DOCUMENT_TYPES = [
    ('CC','CEDULA DE CIUDADANIA'),
    ('CE','CEDULA DE EXTRANJERIA'),
]


class Voter(models.Model):
    typeDocument = models.CharField(max_length=2, choices=DOCUMENT_TYPES, default='CC')
    nuip = models.CharField(max_length=11, unique=True)
    fullName = models.CharField(max_length=100)
    quarter = models.CharField(max_length=50)
    address = models.CharField(max_length=100, blank=True, null=True)
    numberPhone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateField(auto_now=True,blank=True)
    votingPoint = models.ForeignKey(VotingPoint, on_delete=models.CASCADE, related_name='voters')  
    coordinator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.fullName
    
class UserParent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='children')

    def __str__(self):
        return self.user.username
