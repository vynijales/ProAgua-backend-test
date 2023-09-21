import json
import requests

def enviar_dados_para_api(api_url, csrf_token, data):
    headers = {
        'X-CSRFToken': csrf_token,
        'Content-Type': 'application/json'
    }
    json_data = json.dumps(data)
    response = requests.post(api_url, data=json_data, headers=headers)
    return response
