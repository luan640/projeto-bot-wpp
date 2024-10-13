'''
P. Ativar a aplicação
1. ngrok http 8000
2. token ngrok
3. token meta

Doc. para liberação do token permanente do WPP
https://developers.facebook.com/docs/whatsapp/business-management-api/get-started#1--acquire-an-access-token-using-a-system-user-or-facebook-login

'''

import openai
import requests
import json
from myapp.sheets import inputs_ai
from myapp.models import Conversa, Interacao

OPENAI_KEY = "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"
openai.api_key = OPENAI_KEY

#from dotenv import load_dotenv,dotenv_values
#load_dotenv()
#config = dotenv_values(".env2")
#print(config.get('MEUTOKEN'))


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
        "Authorization": "Bearer EAAH2zMGGDWEBO8jZCBvW3tOw5LXrQHJ01vEq6gTMrvNRrixLFlMYmjVJrTQKdhxzKYtqpyW4vs61Ac9CwZBb6ei92YLgGCyeQxrwZAjfI8Hozwmy3IRIZBUpzSuxxU9scgorgWDgugeCSzUyjlWx5EL0mPL5ONNhmdTqXKn4ZAgtTkM1cwVCdDZCjeqIUL1Wf4YHo87FZCx40Hv11c6NiQhiOujisevpE7h8SkZD",  # Substitua pelo seu token de acesso válido
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
                "content": inputs_ai()[0]
            },
            {"role": "user", "content": message}
        ]
    )
    return response['choices'][0]['message']['content'].strip()


# def criar_conversa(id_conversa, telefone):
#     Conversa.objects.create(
#         id_conversa = id_conversa,
#         telefone = telefone
#     )

# def interacao(id_conversa, input_usuario):
#     id_conversa = Conversa.objects.get(id_conversa = id_conversa)
#     Interacao.objects.create(
#         id_conversa = id_conversa,
#         input_usuario = input_usuario,
#     )


#data
#response_message