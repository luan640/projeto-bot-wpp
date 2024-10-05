import openai
import requests
import json

openai.api_key = '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'  # Substitua pela sua chave correta

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
        "Authorization": "Bearer EAAHV2ZBvVYMsBOZCwjEwpa0ZCpCeZCy9JfJu8YuOjzF6W2KG9ahaiqrwfBHCo1UOQeGufYvZBNHWDQIGSkeDQbBVKZB5uXUCJLDHVNz2Fl6i77jkJ4m4DvRSqaHVtdxiWDL9S15AaXzXXZAyCAJE3wf6uAQtCIEh6oKINYRe9i2MvtZCHtbp8ia3UIsUO0eGZA0QeWVZCtYUeGSS0ej87W2qJFrqJQ1iN3zIf6AQUZD",  # Substitua pelo seu token de acesso válido
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
            {"role": "system", "content": "Você é um assistente especializado em mecânica automotiva."},
            {"role": "user", "content": message}
        ]
    )
    return response['choices'][0]['message']['content']
