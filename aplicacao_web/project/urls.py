"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signin/',views.signin, name='signin'),
    path('signout/',views.signout, name='signout'),
    path('signup/',views.signup, name='signup'),
    path('profile/',views.profile, name='profile'),
    path('get_temperature/', views.get_temperature, name='get_temperature'),
    path('get_humidity/', views.get_humidity, name='get_humidity'),
    path('get_luminosidade/', views.get_luminosidade, name='get_luminosidade'),
    path('analise/', views.analise, name='analise'),
    path('analise/<str:intervalo_tempo>/', views.analise, name='analise'),
    path('ligar_desligar_lampada/', views.ligar_desligar_lampada, name='ligar_desligar_lampada'),
    path('ligar_desligar_ar_condicionado/', views.ligar_desligar_ar_condicionado, name='ligar_desligar_ar_condicionado'),
]

