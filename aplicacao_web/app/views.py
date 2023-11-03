from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.shortcuts import HttpResponseRedirect
from django.http import JsonResponse
from .models import DadosTemperaturaUmidade

def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})
   
def home(request): 
    if request.user.is_authenticated:
        return redirect('/profile')
    else:
        return render(request, 'home.html')
   
  
def signin(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/profile') #profile
        else:
            msg = 'Error Login'
            form = AuthenticationForm(request.POST)
            return render(request, 'login.html', {'form': form, 'msg': msg})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})
  
def profile(request):
    # Adicione a lógica para buscar os dados do histórico de temperatura e umidade
    historico = DadosTemperaturaUmidade.objects.all()  # Substitua pela consulta correta

    context = {
        'historico': historico,
    }

    return render(request, 'profile.html', context)
   
def signout(request):
    logout(request)
    return redirect('/')

def get_temperature(request):
    # Simule a obtenção da temperatura de uma API externa
    temperatura_atual = DadosTemperaturaUmidade.objects.latest('timestamp').temperatura

    data = {
        'temperatura': temperatura_atual,
    }
    return JsonResponse(data)

def get_humidity(request):
    umidade_atual = DadosTemperaturaUmidade.objects.latest('timestamp').umidade

    data = {
        'umidade': umidade_atual,
    }
    return JsonResponse(data)

def get_latest_sensor_data(request):
    latest_data = DadosTemperaturaUmidade.objects.latest('timestamp')
    data = {
        'temperatura': latest_data.temperatura,
        'umidade': latest_data.umidade,
    }
    return JsonResponse(data)