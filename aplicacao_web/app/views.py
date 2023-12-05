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
from .models import Luminosidade
import pandas as pd
from datetime import datetime, timedelta

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')  # Use 'password1' for the first password field
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})
   
def home(request): 
    return render(request, 'login.html')
   
  
def signin(request):
    if request.user.is_authenticated:
        return render(request, 'profile.html')
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
    temperatura_data = Temperatura.objects.last()
    if temperatura_data:
        temperatura_dict = {
            'temperatura': temperatura_data.temperatura,
            'idEsp' : temperatura_data.idEsp,
            'timestamp': temperatura_data.timestamp
        }
        return JsonResponse(temperatura_dict)
    else:
        return JsonResponse({'error': 'Nenhum registro de temperatura encontrado'})

def get_humidity(request):
    umidade_data = Umidade.objects.last()
    if umidade_data:
        umidade_dict = {
            'umidade': umidade_data.umidade,
            'idEsp' : umidade_data.idEsp,
            'timestamp': umidade_data.timestamp
        }
        return JsonResponse(umidade_dict)
    else:
        return JsonResponse({'error': 'Nenhum registro de umidade encontrado'})
    
def get_luminosidade(request):
    luminosidade_data = Luminosidade.objects.last()
    if luminosidade_data:
        if (luminosidade_data.ligado == True):
            luminosidade_data.ligado = 'Ligado'
        else:
            luminosidade_data.ligado = 'Desligado'
        luminosidade_dict = {
            'luminosidade': luminosidade_data.ligado,
            'idEsp' : luminosidade_data.idEsp,
            'timestamp': luminosidade_data.timestamp
        }
        return JsonResponse(luminosidade_dict)
    else:
        return JsonResponse({'error': 'Nenhum registro de luminosidade encontrado'})

def sensor_data_view(request):
    sensor_data = SensorData.objects.all()
    return render(request, 'sensor_data.html', {'sensor_data': sensor_data})



def analise(request, intervalo_tempo=None):
    # Obtenha os dados do banco de dados
    historico_temperatura = Temperatura.objects.all()
    historico_umidade = Umidade.objects.all()

    # Cria DataFrames a partir dos dados do banco de dados
    df_temperatura = pd.DataFrame(list(historico_temperatura.values()))
    df_umidade = pd.DataFrame(list(historico_umidade.values()))

    # Converta a coluna 'timestamp' para datetime
    df_temperatura['timestamp'] = pd.to_datetime(df_temperatura['timestamp'])
    df_umidade['timestamp'] = pd.to_datetime(df_umidade['timestamp'])

    # Ordene os DataFrames por timestamp, se necessário
    df_temperatura = df_temperatura.sort_values(by='timestamp')
    df_umidade = df_umidade.sort_values(by='timestamp')

 # Lógica para converter o intervalo de tempo em um timedelta
    if intervalo_tempo == 'today':
        filtro_tempo = datetime.now() - timedelta(days=1)
    elif intervalo_tempo == 'this_week':
        filtro_tempo = datetime.now() - timedelta(weeks=1)
    elif intervalo_tempo == 'this_month':
        filtro_tempo = datetime.now() - timedelta(weeks=4)
    else:
        # Para 'all_time', não aplicamos nenhum filtro de tempo
        filtro_tempo = None

    # Aplicar o filtro de tempo nos DataFrames
    if filtro_tempo is not None:
        df_temperatura['timestamp'] = pd.to_datetime(df_temperatura['timestamp'], utc=True).dt.tz_localize(None)
        df_umidade['timestamp'] = pd.to_datetime(df_umidade['timestamp'], utc=True).dt.tz_localize(None)

        df_temperatura = df_temperatura[df_temperatura['timestamp'] >= filtro_tempo]
        df_umidade = df_umidade[df_umidade['timestamp'] >= filtro_tempo]

    # Restante do seu código...

    return render(request, 'analise.html', {'df_temperatura': df_temperatura, 'df_umidade': df_umidade})