import requests

def inputs_ai():
    # Defina o ID da planilha e sua chave de API
    spreadsheet_id = "1JWrfUuWIQwxLU_BDf9RFh3U0WBqQYtVlfqXMWReRbFo"
    api_key = "AIzaSyD3TWAPEi3_3hUELtNp4efJSHgauIZgr7U"

    # URL para acessar a aba Inputs_AI e a coluna A
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/Inputs_AI!A:A?key={api_key}"

    # Fazer a requisição
    response = requests.get(url)
    data = response.json()

    # Extrair os valores da coluna A e colocá-los em uma lista
    resultado_input = [row[0] for row in data['values']]
    return resultado_input