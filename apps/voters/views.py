from django.contrib import messages 
from django.contrib.auth.mixins import  LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView
from django.utils import timezone
from .forms import VotersForm
from .models import Voter
from rest_framework import generics
from .serializers import VoterSerializer

import csv
from .models import Quarters  # Asegurate que esta ruta al modelo sea correcta

def load_data_from_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Omitimos la primera fila si contiene los encabezados
        for row in reader:
            # Asegúrate de que la fila no está vacía antes de intentar acceder a los elementos
            if row:
                obj, created = Quarters.objects.get_or_create(
                    name=row[2].strip() if len(row) > 1 else "",  # Asumimos que 'name' es la segunda columna
                    commune=row[3].strip() if len(row) > 2 else ""  # Asumimos que 'commune' es la tercera columna
                )

class VoterListCreate(generics.ListCreateAPIView):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer
    
class CreateUpdateMixin():
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

class VotersFormView(LoginRequiredMixin, View, CreateUpdateMixin):
    template_name = 'voters.html'
    form_class = VotersForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        return self.process_form(request, form)

class VotersUpdateView(LoginRequiredMixin, View, CreateUpdateMixin):
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
            return self.process_form(request, form, instance=voter)

        messages.error(request, 'Has llegado al límite de ediciones diarias.')
        return redirect('voter:voter-list')  