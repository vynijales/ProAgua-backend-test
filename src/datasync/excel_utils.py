import pandas as pd
import os

def obter_dados_excel():
    address = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(address, 'SI para PowerBi.xlsm')
    pd.set_option('display.max_columns', None)
    df = pd.read_excel(file_path, sheet_name='Banco de Dados', engine='openpyxl')
    return df
