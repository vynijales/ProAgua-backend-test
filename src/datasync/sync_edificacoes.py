# main.py
import os
import re
import pandas as pd
from excel_utils import obter_dados_excel
from csrf_utils import obter_token_csrf
from api_utils import enviar_dados_para_api

def main():
    address = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(address, 'SI para PowerBI.xlsm')
    api_url = 'http://localhost:8000/api/v1/edificacoes/'  # Substituindo pelo URL correto da API

    df = obter_dados_excel(file_path)
    codigos_existentes = set()
    url_csrf = 'http://localhost:8000/api/v1/csrf'  # Substituindo pelo URL correto do endpoint CSRF

    csrf_token = obter_token_csrf(url_csrf)

    for indice, linha in df.iterrows():
        if indice > 5:
            if (linha.iloc[5] == 'Leste'):
                linha.iloc[5] = 'LE'
            elif (linha.iloc[5] == 'Oeste'):
                linha.iloc[5] = 'OE'

            dados = {
                "cronograma": int(re.search(r'\d+', linha.iloc[2]).group()),
                "codigo": linha.iloc[3],
                "nome": linha.iloc[4],
                "campus": linha.iloc[5]
            }

            if dados["codigo"] not in codigos_existentes:
                codigos_existentes.add(dados["codigo"])
                response = enviar_dados_para_api(api_url, csrf_token, dados)

                if response.status_code == 200:
                    dados_resposta = response.json()
                    print(dados_resposta)
                else:
                    print(f"Erro: {response.status_code}")
                    print(response.text)

if __name__ == "__main__":
    main()
