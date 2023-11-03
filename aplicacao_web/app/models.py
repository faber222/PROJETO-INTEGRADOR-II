from django.db import models

class DadosTemperaturaUmidade(models.Model):
    temperatura = models.DecimalField(max_digits=5, decimal_places=2)
    umidade = models.DecimalField(max_digits=5, decimal_places=2)
    timestamp = models.DateTimeField()

    class Meta:
        db_table = 'dados_temperatura_umidade'