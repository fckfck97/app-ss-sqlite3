from .models import Voter
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db import models
from .models import Voter, UserParent

def reportVoter(request):
    context = {}
    if request.user.is_authenticated: # Aseguramos que el usuario está autenticado
        try:
            voters = Voter.objects.filter(coordinator=request.user)
            context = {
                'enc': voters,
                'quantity': len(voters)
            }
            return render(request, "reporte/reporte.html", context)
        except Exception as e:  
                print(e)
    else:
        messages.error(request, 'Debes iniciar sesión para ver este recurso.')
    messages.error(request,'Factura NO Disponible Actualmente.')
    return redirect("voter:voter-list")

def reportUserParent(request):
    context = {}
    if request.user.is_authenticated: 
        try:
            parent = UserParent.objects.get(user=request.user)
            children_reports = []
            parent_voters = Voter.objects.filter(coordinator=parent.user)
            voters_count = parent_voters.count()

            for child in parent.children.all():
                voters = Voter.objects.filter(coordinator=child.user)
                voters_count += voters.count()
                children_reports.append({
                    'child': child,
                    'voters': voters,
                    'voters_count': voters.count()
                })

            context = {
                'parent': parent,
                'parent_voters': parent_voters,
                'voters_count': voters_count,
                'children_reports': children_reports,
            }

            return render(request, "reporte/report-child.html", context)
        except Exception as e:  
            print(e)
    else:
        messages.error(request, 'Debes iniciar sesión para ver este recurso.')
    messages.error(request, 'Reporte NO Disponible Actualmente.')
    return redirect("home")

def reportByVotingPoint(request):
    context = {}
    if request.user.is_authenticated:
        try:
            voters = Voter.objects.values('votingPoint__name').annotate(count=models.Count('votingPoint')).order_by('-count')
            total_voters = voters.aggregate(count_totals=models.Sum('count'))['count_totals']
            context = {
                'votingPoints': voters,
                'total_voters': total_voters,
            }
            return render(request, "reporte/reporte_votingPoint.html", context)
        except Exception as e:  
            print(e)
    else:
        messages.error(request, 'Debes iniciar sesión para ver este recurso.')
    messages.error(request,'Reporte NO Disponible Actualmente.')
    return redirect("voter:voter-list")

def reportByQuarter(request):
    context = {}
    if request.user.is_authenticated:
        try:
            # Se agrupa los votantes respecto al campo quarter y se cuenta cuántos hay en cada uno
            voters = Voter.objects.values('quarter').annotate(count=models.Count('quarter')).order_by('-count')
            # Se cuenta el total de votantes
            total_voters = Voter.objects.count()
            context = {
                'quarters': voters,
                'total_voters': total_voters,
            }
            return render(request, "reporte/reporte_quarter.html", context)
        except Exception as e:  
            print(e)    
    else:
        messages.error(request, 'Debes iniciar sesión para ver este recurso.')

    messages.error(request,'Reporte NO Disponible Actualmente.')
    return redirect("voter:voter-list")