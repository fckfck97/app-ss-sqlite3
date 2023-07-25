from django.views import View
from django.contrib.auth.mixins import  LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages 
from django.core.exceptions import ValidationError
from .forms import VotersForm
from .models import Voter
from django.utils import timezone

class HomeView(View):
    template_name ='base.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
class VoterListView(LoginRequiredMixin,ListView):
    model = Voter
    template_name = "voters_list.html"
    context_object_name = "voters" 
    
    def get_queryset(self):
        return Voter.objects.filter(coordinator=self.request.user)

class VotersFormView(LoginRequiredMixin, View):
    template_name = 'voters.html'

    def get(self, request, *args, **kwargs):
        form = VotersForm()
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = VotersForm(request.POST, request.FILES)
        
        if form.is_valid():
            nuip = form.cleaned_data.get('nuip')
            fullName = form.cleaned_data.get('fullName')
            quarter = form.cleaned_data.get('quarter')
            votingPoint = form.cleaned_data.get('votingPoint')
            numberPhone = form.cleaned_data.get('numberPhone')
            email = form.cleaned_data.get('email')
            
            voter = Voter(
                nuip=nuip,
                fullName=fullName,
                quarter=quarter,
                votingPoint=votingPoint,
                numberPhone=numberPhone,
                email=email,
                coordinator=request.user,
            )
            voter.save()

            messages.success(request, 'Votante Registrado con éxito')
            return redirect('voter:voter-list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    if "already exists" in error:
                        error = "Ya existe un Votante registrado con esa Cedula."
                    messages.error(request, f"{error}")

        
        return render(request, self.template_name, {'form': form})
    
class VotersUpdateView(LoginRequiredMixin, View):
    template_name="votersEdit.html"
    form_class=VotersForm

    def get(self, request, *args, **kwargs):
        voter = Voter.objects.get(pk=kwargs['pk'])
        form = self.form_class(instance=voter)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        voter = Voter.objects.get(pk=kwargs['pk'])
        form = self.form_class(request.POST, request.FILES, instance=voter)

        if 'voter_edits' in request.session and request.session['voter_edits_date'] == timezone.now().date().isoformat():
            if request.session['voter_edits'] >= 3:
                messages.error(request, 'Has llegado al límite de ediciones diarias.')
                return redirect('voter:voter-list')
        else:
            request.session['voter_edits'] = 0
            request.session['voter_edits_date'] = timezone.now().date().isoformat()

        if form.is_valid():
            form.save()

            request.session['voter_edits'] += 1 

            messages.success(request, 'Votante actualizado con éxito')
            return redirect('voter:voter-list')

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    if "already exists" in error:
                        error = "Ya existe un Votante registrado con esa Cedula."
                    messages.error(request, f"{error}")

        return render(request, self.template_name, {'form': form})