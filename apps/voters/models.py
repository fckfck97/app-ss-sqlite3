from django.db import models
from django.contrib.auth.models import User
from import_export import resources

class VotingPoint(models.Model):
    name = models.CharField(max_length=200)
    longitude = models.DecimalField(max_digits=9, decimal_places=6) 
    latitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        self.name = self.name.upper()
        return self.name


DOCUMENT_TYPES = [
    ('CC','CEDULA DE CIUDADANIA'),
    ('CE','CEDULA DE EXTRANJERIA'),
]

class Voter(models.Model):
    document_type = models.CharField(max_length=2, choices=DOCUMENT_TYPES, default='CC')
    nuip = models.CharField(max_length=11, unique=True)
    full_name = models.CharField(max_length=100)
    quarter = models.CharField(max_length=50)
    address = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateField(auto_now=True,blank=True)
    voting_point = models.ForeignKey(VotingPoint, on_delete=models.CASCADE, related_name='voters')  
    coordinator = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.full_name = self.full_name.upper()
        self.quarter = self.quarter.upper()
        self.address = self.address.upper()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name

class UserParent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='children')

    def __str__(self):
        return self.user.username
