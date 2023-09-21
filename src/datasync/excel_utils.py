import pandas as pd

def obter_dados_excel(file_path):
    pd.set_option('display.max_columns', None)
    df = pd.read_excel(file_path, sheet_name='Banco de Dados', engine='openpyxl')
    return df
