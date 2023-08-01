from django.urls import path
from .views import HomeView, VotersFormView, VotersUpdateView, VoterListView, VoterListCreate, ConsultAPIView, DashboardView
from .reporte import reportVoter, reportUserParent, reportByQuarter, reportByVotingPoint
app_name = 'apps.voters'


urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('voters/', VoterListView.as_view(), name='voter-list'),
    path('voter',VotersFormView.as_view(), name='voter'),
    path('voter/<pk>/edit',VotersUpdateView.as_view(), name='voter-edit'),
    
    path('api/v1/voters/', VoterListCreate.as_view(), name='voters_list_create'),
    path('api/v1/consult/', ConsultAPIView.as_view()),
    path('report',reportVoter, name="report-voter"),
    path('report/parent',reportUserParent, name="report-parent"),
    path('report/quarter', reportByQuarter, name='report-quarter'),
    path('report/votingPoint', reportByVotingPoint, name='report-votingPoint'),
]
