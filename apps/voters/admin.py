from django.contrib import admin
from .models import Voter, VotingPoint
# Register your models here.
admin.site.register(Voter)
admin.site.register(VotingPoint)