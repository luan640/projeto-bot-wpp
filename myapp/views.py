from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from django.http import HttpResponse
from myapp.functions_gpt import send_whatsapp_message, tratar_numero_wa, get_chatgpt_response


def home(request):
    return HttpResponse("Olá, bem-vindo ao meu app!")


class WhatsAppWebhookView(APIView):

    def get(self, request, *args, **kwargs):
        VERIFY_TOKEN = 'meu_token_seguro'
        mode = request.query_params.get('hub.mode')
        token = request.query_params.get('hub.verify_token')
        challenge = request.query_params.get('hub.challenge')

        if mode and token == VERIFY_TOKEN:
            return HttpResponse(challenge, status=200)
        else:
            return HttpResponse('Erro de verificação', status=403)

    def post(self, request, *args, **kwargs):
        data = request.data
        print('Mensagem recebida:', data)

        try:
            # Verifique se a chave "contacts" está presente
            if 'contacts' in data['entry'][0]['changes'][0]['value']:
                # Extraia o wa_id da mensagem recebida
                recipient_number = data['entry'][0]['changes'][0]['value']['contacts'][0]['wa_id']
                recipient_number_tratado = tratar_numero_wa(recipient_number)  # Tratamento do número
                print(f"WA ID tratado: {recipient_number_tratado}")

                # Verifique se a chave "messages" está presente antes de acessar
                if 'messages' in data['entry'][0]['changes'][0]['value']:
                    received_message = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
                    print(f"Mensagem recebida: {received_message}")

                    # Gere uma resposta do ChatGPT para a mensagem recebida
                    response_message = get_chatgpt_response(received_message)

                    # Envie a resposta de volta via API do WhatsApp
                    status_code, response_data = send_whatsapp_message(recipient_number_tratado, response_message)
                    print(f"Status: {status_code}, Response: {response_data}")
                else:
                    print("Nenhuma mensagem encontrada na entrada.")

            # Verifique se a chave "statuses" está presente
            elif 'statuses' in data['entry'][0]['changes'][0]['value']:
                # Trata as atualizações de status, como "delivered", "read", etc.
                status_update = data['entry'][0]['changes'][0]['value']['statuses'][0]
                print(f"Status update: {status_update}")

        except (KeyError, IndexError) as e:
            print(f"Erro ao processar a mensagem: {str(e)}")
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)

