from django.contrib import admin
from .models import Interaction

@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user_message', 'gpt_response')
    search_fields = ('user_id', 'user_message', 'gpt_response')
