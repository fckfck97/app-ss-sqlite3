from django.urls import path
from .views import HomeView, VotersFormView, VotersUpdateView, VoterListView
from .reporte import reportVoter
app_name = 'apps.voters'


urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('voters/', VoterListView.as_view(), name='voter-list'),
    path('voter',VotersFormView.as_view(), name='voter'),
    path('voter/<pk>/edit',VotersUpdateView.as_view(), name='voter-edit'),
    
    path('voter/report',reportVoter, name="report-voter"),
]
