import os
import re
import pandas as pd
from excel_utils import obter_dados_excel
from csrf_utils import obter_token_csrf
from api_utils import enviar_dados_para_api, receber_dados_da_api

def main():
    api_url = 'http://localhost:8000/api/v1/edificacoes/'

    df = obter_dados_excel()
    codigos_existentes = set()
    url_csrf = 'http://localhost:8000/api/v1/csrf'

    csrf_token = obter_token_csrf(url_csrf)

    response_get = receber_dados_da_api(api_url, csrf_token)

    if response_get.status_code == 200:
        dados_existentes = response_get.json()
        codigos_existentes = set(item['codigo'] for item in dados_existentes)

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

                # Verificando se o código já existe no conjunto de códigos existentes
                if dados["codigo"] not in codigos_existentes:
                    response = enviar_dados_para_api(api_url, csrf_token, dados)

                    if response.status_code == 200:
                        dados_resposta = response.json()
                        print(dados_resposta)
                        codigos_existentes.add(dados["codigo"])  # Adicionando o código ao conjunto após a inserção
                    else:
                        print(f"Erro: {response.status_code}")
                        print(response.text)
                else:
                    print(f"Dados já existentes para código {dados['codigo']}")
    else:
        print(f"Erro ao obter dados existentes: {response_get.status_code}")

if __name__ == "__main__":
    main()
