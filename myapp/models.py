from django.db import models

class Interaction(models.Model):
    user_id = models.CharField(max_length=20)
    user_message = models.TextField()
    gpt_response = models.TextField()
    step = models.IntegerField(default=1)  # Etapa do fluxo
    service = models.TextField(blank=True, null=True)  # Pode armazenar JSON como string
    date = models.DateField(null=True, blank=True)
    professional = models.CharField(max_length=50, null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interação com {self.user_id} em {self.created_at}"

class Agendamento(models.Model):
    user_id = models.CharField(max_length=20)  # Número de telefone do usuário
    service = models.CharField(max_length=100)  # Serviço escolhido
    date = models.DateField()  # Data do agendamento
    time = models.TimeField()  # Hora do agendamento
    professional = models.CharField(max_length=100)  # Nome do profissional
    status = models.CharField(max_length=20, default="Ativo")  # Status do agendamento

    created_at = models.DateTimeField(auto_now_add=True)  # Data e hora de criação
    updated_at = models.DateTimeField(auto_now=True)  # Data e hora de atualização

    def __str__(self):
        return f"{self.service} em {self.date} às {self.time} com {self.professional}"
