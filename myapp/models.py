from django.db import models

class Interaction(models.Model):
    user_id = models.CharField(max_length=20)
    user_message = models.TextField()
    gpt_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interação com {self.user_id} em {self.created_at}"
