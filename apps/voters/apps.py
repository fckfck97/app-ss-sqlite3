from django.apps import AppConfig
from .archivos.quarters import load_quarters
from .archivos.votingpoint import load_point

class VotersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.voters'

    def ready(self):
        from .archivos import signal
        
        self.check_and_load_quarters()
        self.check_and_load_points()

    def check_and_load_quarters(self):
        from .models import Quarters
        if not Quarters.objects.exists():
            load_quarters()

    def check_and_load_points(self):
        from .models import VotingPoint
        if not VotingPoint.objects.exists():
            load_point()