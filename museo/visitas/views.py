from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from .forms import VisitaForm, SalidaForm
from .models import Visita
import datetime
# Create your views here.

class Home(View):
    def get(self,request):
        return render(request, 'index.html', {})

class Entrada(View):
    def get(self,request):
        form = VisitaForm()
        context = {'form':form}
        return render(request, 'entrada.html', context)
    
    def post(self, request):
        form = VisitaForm(request.POST)
        if form.is_valid():
            entrada = form.save(commit=False)
            visitas = Visita.objects.filter(timestamp_in__gte=datetime.date.today(), timestamp_out=None)
            if visitas:
                print("Ya está dentro")
            else:
                print("Pase por favor")
                entrada.save()
            return redirect('index')
        else:
            context = {'form': form}
            return render(request, 'entrada.html', context)

class Salida(View):
    def get(self,request):
        form = SalidaForm()
        context = {'form':form}
        return render(request, 'salida.html', context)
    
    def post(self, request):
        form = SalidaForm(request.POST)
        if form.is_valid():
            #form.save()
            salida = form.save(commit=False)
            visitas = Visita.objects.filter(email=salida.email,timestamp_out=None, timestamp_in__gte=datetime.date.today())
            if visitas:
                #print(f"Si hay registros: {visitas}")
                visita = Visita.objects.get(pk=visitas[0].id)
                visita.timestamp_out = datetime.datetime.now()
                visita.comment = salida.comment
                visita.save()
            else:
                print("NO HAY REGISTROS!")
            return redirect('index')
        else:
            context = {'form': form}
            return render(request, 'salida.html', context)