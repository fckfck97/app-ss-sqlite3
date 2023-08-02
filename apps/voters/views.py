from django.contrib import messages 
from django.contrib.auth.mixins import  LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView
from django.utils import timezone
from .forms import VotersForm
from .models import Voter,SharedToken
from .serializers import VoterSerializer, ConsultSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, exceptions, generics
from rest_framework.authentication import BaseAuthentication
from django.utils import timezone
import json
class SharedTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return None
        try:
            SharedToken.objects.get(key=token)
        except SharedToken.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such token')

        return (None, None)

class ConsultAPIView(APIView):
    authentication_classes = [SharedTokenAuthentication]
    def get_new_nuip(self):
        new_nuip_object = Voter.objects.filter(checkout=False).first()
        if new_nuip_object:
            return new_nuip_object.nuip
        else:
            return 'Ya no hay NUIP para verificar'
    def post(self, request, *args):
        nuip = request.data.get('nuip')
        current_department = request.data.get('department')
        current_municipality = request.data.get('municipality')
        if not nuip:
            return Response({
                'success': True,
                'new_nuip': self.get_new_nuip()
            }, status=status.HTTP_200_OK)
        try:
            voter = Voter.objects.get(nuip=nuip)
        except Voter.DoesNotExist:
            return Response({'error': 'Votante no registrado en la base de datos SS'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ConsultSerializer(data=request.data)
        if serializer.is_valid():
            official_consultation = serializer.save()
            if voter.voting_point.department != current_department or voter.voting_point.municipality != current_municipality:
                voter.checkout_confirmation = False
            else:
                if not voter.checkout_confirmation:
                    voter.checkout_confirmation = True
            if voter.checkout:
                return Response({'error': 'El votante ya esta validado'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                voter.official_consultation = official_consultation
                voter.checkout = True
                voter.update_at = timezone.now()
                voter.save()
                return Response({
                    'success': True,
                    'new_nuip': self.get_new_nuip()
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VoterListCreate(generics.ListCreateAPIView):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer
    
class CreateUpdateMixin(LoginRequiredMixin, View):
    def process_form(self, request, form, instance=None):
        if form.is_valid():
            form.instance.coordinator = request.user
            if instance:
                form.instance.id = instance.id
            form.save()
            messages.success(request, f'Votante {"actualizado" if instance else "registrado"} con éxito')
            return redirect('voter:voter-list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    if "already exists" in error:
                        error = "Ya existe un Votante registrado con esa Cedula."
                    messages.error(request, f"{error}")
        
        return render(request, self.template_name, {'form': form})

class HomeView(View):
    template_name ='home.html'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('voter:dashboard')
        return render(request, self.template_name)

class DashboardView(LoginRequiredMixin,View):
    template_name ='dash.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
class VoterListView(LoginRequiredMixin, ListView):
    model = Voter
    context_object_name = 'voters'
    template_name = 'voters_list.html'
    paginate_by = 5

    def get_queryset(self):
        return Voter.objects.filter(coordinator=self.request.user)

class VotersFormView(CreateUpdateMixin):
    template_name = 'voters.html'
    form_class = VotersForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            parent_voter = form.save(commit=False) 
            parent_voter.coordinator = request.user 
            parent_voter.save()  
            child_voters_data_str = request.POST.get('child_voters_data', '[]')
            print(child_voters_data_str)
            if child_voters_data_str:
                child_voters_data = json.loads(child_voters_data_str)
            else:
                child_voters_data = []
            print(child_voters_data)
            for child_data in child_voters_data:
                Voter.objects.create(
                    parent_voter=parent_voter,
                    document_type=child_data.get('document_type', 'CC'),
                    nuip=child_data.get('nuip'),
                    full_name=child_data.get('full_name'),
                    coordinator=request.user,
                )
        return self.process_form(request, form)
    
class VotersUpdateView(CreateUpdateMixin):
    template_name="votersEdit.html"
    form_class=VotersForm

    def get(self, request, *args, **kwargs):
        voter = Voter.objects.get(pk=kwargs['pk'])
        form = self.form_class(instance=voter)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        voter = Voter.objects.get(pk=kwargs['pk'])
        form = self.form_class(request.POST, request.FILES, instance=voter)
        if 'voter_edits' not in request.session or request.session['voter_edits_date'] != timezone.now().date().isoformat():
            request.session['voter_edits'] = 0
            request.session['voter_edits_date'] = timezone.now().date().isoformat()

        if request.session['voter_edits'] < 3:
            voter.update_add = timezone.now()  
            voter.save()
            return self.process_form(request, form, instance=voter)

        messages.error(request, 'Has llegado al límite de ediciones diarias.')
        return redirect('voter:voter-list')