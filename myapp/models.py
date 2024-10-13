from django.db import models

class Conversa(models.Model):
    id_conversa = models.CharField(max_length=200,unique=True)
    telefone = models.CharField(max_length=14)

class Interacao(models.Model):
    id_conversa = models.ForeignKey(Conversa,on_delete=models.CASCADE,related_name='interacao_conversa')
    input_usuario = models.CharField(max_length=200, blank=True, null=True)
    input_gpt = models.CharField(max_length=200, blank=True, null=True)




# Create your models here.
