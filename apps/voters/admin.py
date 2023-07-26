from django.contrib import admin
from .models import Voter, VotingPoint, UserParent
# Register your models here.
admin.site.register(Voter)
admin.site.register(VotingPoint)
admin.site.register(UserParent)
