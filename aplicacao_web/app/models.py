from django.db import models

class Temperatura(models.Model):
    temperatura = models.DecimalField(max_digits=5, decimal_places=2)
    idEsp = models.IntegerField()
    timestamp = models.DateTimeField()

    class Meta:
        db_table = 'temperatura'
        
        
class Umidade(models.Model):
    umidade = models.DecimalField(max_digits=5, decimal_places=2)
    idEsp = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'umidade'
        
class Luminosidade(models.Model):
    ligado = models.BooleanField()
    idEsp = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'luminosidade'
        
class Lampada(models.Model):
    ligado = models.BooleanField()
    idEsp = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'lampada'
        
class Ar_Condicionado(models.Model):
    ligado = models.BooleanField()
    idEsp = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ar_condicionado'