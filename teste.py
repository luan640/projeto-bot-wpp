import openai
import requests
import json

openai.api_key = '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'  # Substitua pela sua chave correta

response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Você é um assistente especializado em mecânica automotiva."},
        {"role": "user", "content": 'Olá'}
    ]
)

