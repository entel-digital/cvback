# Script para generar clave de encriptación y actualizar .envs/.local/.django
import os
import secrets

env_directory = '/app/.envs/.local'
env_file = os.path.join(env_directory, '.django')
key_exists = False

# Crea los directorios si no existen
if not os.path.exists(env_directory):
    os.makedirs(env_directory)

if os.path.exists(env_file):
    with open(env_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if 'DJANGO_ENCRYPTED_FIELD_KEY' in line:
                key_exists = True
                break

if not key_exists:
    key = secrets.token_hex(16)  # Genera una clave de 32 bytes en formato hexadecimal
    with open(env_file, 'a') as file:
        file.write(f'DJANGO_ENCRYPTED_FIELD_KEY="{key}"\n')