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
from .models import Lampada
from .models import Ar_Condicionado
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
from plotly.offline import plot
import plotly.io as pio
from django.templatetags.static import static
import os
from django.utils import timezone
from datetime import timedelta


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
            return render(request, 'profile.html') #profile
        else:
            msg = 'Error Login'
            form = AuthenticationForm(request.POST)
            return render(request, 'login.html', {'form': form, 'msg': msg})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})
  
def profile(request):
    lampada_status = Lampada.objects.latest('timestamp')
    ar_condicionado_status = Ar_Condicionado.objects.latest('timestamp')

    context = {
        'lampada_status': lampada_status,
        'ar_condicionado_status': ar_condicionado_status,
    }

    return render(request, 'profile.html', context)
   
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
            luminosidade_data.ligado = 'Ligada'
        else:
            luminosidade_data.ligado = 'Desligada'
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

    # Criação dos gráficos
    fig_temperatura = px.line(df_temperatura, x='timestamp', y='temperatura', labels={'temperatura': 'Temperatura (°C)'}, title='Gráfico de Temperatura')
    fig_umidade = px.line(df_umidade, x='timestamp', y='umidade', labels={'umidade': 'Umidade (%)'}, title='Gráfico de Umidade')

    # Salve os gráficos em arquivos HTML temporários dentro do diretório 'plots'
    temp_path_temperatura = os.path.join('app', 'static', 'plots', 'graph_temperatura.html')
    temp_path_umidade = os.path.join('app', 'static', 'plots', 'graph_umidade.html')

    pio.write_html(fig_temperatura, file=temp_path_temperatura, auto_open=False)
    pio.write_html(fig_umidade, file=temp_path_umidade, auto_open=False)

    return render(request, 'analise.html', {
        'df_temperatura': df_temperatura,
        'df_umidade': df_umidade,
        'temp_path_temperatura': temp_path_temperatura,
        'temp_path_umidade': temp_path_umidade,
    })
    
    
def ligar_desligar_lampada(request):
    try:
        lampada_status = Lampada.objects.latest('timestamp')
    except Lampada.DoesNotExist:
        # Se não houver nenhum objeto, crie um novo
        lampada_status = Lampada.objects.create(ligado=False, idEsp=1)  # Substitua 1 pelo valor correto

    lampada_status.ligado = not lampada_status.ligado
    lampada_status.timestamp = timezone.now() - timedelta(hours=3)  # Subtrai 3 horas do timestamp
    lampada_status.save()

    return redirect('profile')

def ligar_desligar_ar_condicionado(request):
    try:
        ar_condicionado_status = Ar_Condicionado.objects.latest('timestamp')
    except Ar_Condicionado.DoesNotExist:
        # Se não houver nenhum objeto, crie um novo
        ar_condicionado_status = Ar_Condicionado.objects.create(ligado=False, idEsp=1)  # Substitua 1 pelo valor correto

    ar_condicionado_status.ligado = not ar_condicionado_status.ligado
    ar_condicionado_status.timestamp = timezone.now() - timedelta(hours=3)  # Subtrai 3 horas do timestamp
    ar_condicionado_status.save()

    return redirect('profile')