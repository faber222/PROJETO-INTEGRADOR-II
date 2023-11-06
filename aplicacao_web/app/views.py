from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.shortcuts import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from .models import Temperatura
from .models import Umidade

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
    return render(request, 'profile.html')
   
def signout(request):
    logout(request)
    return redirect('/')

def get_temperature(request):
    # Recupere o último registro de temperatura (substitua 'Temperatura' pelo seu modelo real)
    temperatura_data = Temperatura.objects.last()
    if temperatura_data:
        temperatura_dict = {
            'temperatura': temperatura_data.temperatura,
            'timestamp': temperatura_data.timestamp
        }
        return JsonResponse(temperatura_dict)
    else:
        return JsonResponse({'error': 'Nenhum registro de temperatura encontrado'})

def get_humidity(request):
    # Recupere o último registro de umidade (substitua 'Umidade' pelo seu modelo real)
    umidade_data = Umidade.objects.last()
    if umidade_data:
        umidade_dict = {
            'umidade': umidade_data.umidade,
            'timestamp': umidade_data.timestamp
        }
        return JsonResponse(umidade_dict)
    else:
        return JsonResponse({'error': 'Nenhum registro de umidade encontrado'})

def sensor_data_view(request):
    sensor_data = SensorData.objects.all()
    return render(request, 'sensor_data.html', {'sensor_data': sensor_data})
