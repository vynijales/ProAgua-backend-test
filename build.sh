#!/usr/bin/env bash

echo "Migrando banco de dados..."
python3 src/manage.py makemigrations --noinput
python3 src/manage.py migrate --noinput

echo "Criando usuário padrão..."
DJANGO_SUPERUSER_PASSWORD=admin
DJANGO_SUPERUSER_USERNAME=admin
python3 src/manage.py createsuperuser --noinput

echo "Tudo pronto!"