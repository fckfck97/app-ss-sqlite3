from django.contrib import admin
from .models import Voter, VotingPoint, UserParent, Quarters, OfficialConsultation, SharedToken
# Register your models here.
admin.site.register(Voter)
admin.site.register(VotingPoint)
admin.site.register(UserParent)
admin.site.register(Quarters)
admin.site.register(OfficialConsultation)
admin.site.register(SharedToken)