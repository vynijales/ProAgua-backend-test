import requests

def obter_token_csrf(url_csrf):
    response = requests.get(url_csrf)
    response.raise_for_status()  # Lançando uma exceção se a resposta não for bem-sucedida
    return response.cookies['csrftoken']
