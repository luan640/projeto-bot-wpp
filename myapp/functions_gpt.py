import openai
import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

TOKEN_OPENAI = os.getenv("TOKEN_OPENAI")
TOKEN_FACEBOOK = os.getenv("TOKEN_FACEBOOK")

openai.api_key = TOKEN_OPENAI

def tratar_numero_wa(wa_id):
    # Verifique se o número começa com o código de país +55 (Brasil)
    if wa_id.startswith("55") and len(wa_id) >= 12:  # Considerar números com 12 ou mais dígitos
        # Verificar se já tem o dígito 9
        codigo_area = wa_id[4:6]  # Extrai o código de área
        numero_restante = wa_id[6:]
        
        if not numero_restante.startswith('9'):
            # Inserir o dígito 9 após o código de área
            return wa_id[:4] + '9' + wa_id[4:]
        else:
            return wa_id  # Se já tiver o dígito 9, retorna o número sem modificação
    else:
        # Se não for um número no formato esperado, retorna o número sem modificação
        return wa_id
    
def send_whatsapp_message(recipient_number, message_text):
    url = f"https://graph.facebook.com/v20.0/458377177351953/messages"
    headers = {
        "Authorization": f"Bearer {TOKEN_FACEBOOK}",  # Substitua pelo seu token de acesso válido
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": tratar_numero_wa(recipient_number),
        "type": "text",
        "text": {
            "body": message_text
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.status_code, response.json()

def get_chatgpt_response(message):

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "Você é um assistente virtual especializado em mecânica automotiva. "
                    "Você oferece respostas detalhadas sobre manutenção de veículos, diagnóstico de problemas, "
                    "melhores práticas para economia de combustível, e peças de reposição. Suas respostas devem "
                    "ser claras e adaptadas ao nível de conhecimento do usuário, evitando jargões técnicos, "
                    "a menos que o usuário peça explicações mais técnicas."
                )
            },
            {"role": "user", "content": message}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

