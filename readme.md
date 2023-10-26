# Instalação
Para instalar as bibliotecas necessárias, abra a pasta do projeto e execute o seguinte comando no terminal:

```sh
pip3 install -r requirements.txt
```

# Rodar servidor
Se você ainda não realizou as migrations, execute os seguintes comandos para criar o banco de dados e popular:
```sh
python3 src/manage.py makemigrations proagua_api
python3 src/manage.py migrate
python3 src/manage.py seed // Popular banco de dados com dados de teste
```

Para rodar o servidor use o seguinte comando:
```sh
python3 src/manage.py runserver
```

# Limpar o Banco de Dados
Se precisar limpar o banco de dados, execute o seguinte comando:
```sh
python3 src/manage.py clear
```

# Criar superuser padrão
Se precisar criar um superuser padrão, execute o seguinte comando:
```sh
python3 src/manage.py createadmin
```

# Configurar o Banco de Dados
Para garantir a integridade do Banco de Dados, execute o seguinte comando:
```sh
python3 src/manage.py config
```

# Testando a API
Para testar a API, mova o arquivo "SI para PowerBi.xlsm" para a pasta "src/datasync". Certifique-se de estar logado como superuser e com o servidor em execução. Em seguida, execute o seguinte comando:
```sh
python3 src/datasync/sync_edficacoes.py
```