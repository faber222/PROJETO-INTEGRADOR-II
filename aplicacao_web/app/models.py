from django.db import models

class Temperatura(models.Model):
    temperatura = models.DecimalField(max_digits=5, decimal_places=2)
    timestamp = models.DateTimeField()

    class Meta:
        db_table = 'temperatura'
        
        
class Umidade(models.Model):
    umidade = models.DecimalField(max_digits=5, decimal_places=2)
    timestamp = models.DateTimeField()

    class Meta:
        db_table = 'umidade'