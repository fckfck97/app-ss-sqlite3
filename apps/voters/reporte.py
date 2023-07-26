from .models import Voter
from django.contrib import messages
from django.shortcuts import render, redirect

from .models import Voter

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