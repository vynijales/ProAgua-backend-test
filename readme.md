# Instalação
Para instalar as bibliotecas necessárias, abra a pasta do projeto e execute o seguinte comando no terminal:

```sh
pip3 install -r requirements.txt
```

# Rodar servidor
Se você ainda não realizou as migrations, execute os seguintes comandos para criar o banco de dados e popular:
```sh
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py seed // Popular banco de dados com dados de teste
```

Para rodar o servidor use o seguinte comando:
```sh
python3 manage.py runserver
```
