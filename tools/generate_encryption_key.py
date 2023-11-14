# Script para generar clave de encriptación y actualizar .envs/.local/.django
import os
import secrets

env_file = '../.envs/.local/.django'
key = secrets.token_urlsafe(32)  # Genera una clave segura de 32 bytes

if os.path.exists(env_file):
    with open(env_file, 'r') as file:
        lines = file.readlines()

    with open(env_file, 'w') as file:
        for line in lines:
            if 'DJANGO_ENCRYPTED_FIELD_KEY' not in line:
                file.write(line)
        file.write(f'DJANGO_ENCRYPTED_FIELD_KEY="{key}"\n')
else:
    with open(env_file, 'w') as file:
        file.write(f'DJANGO_ENCRYPTED_FIELD_KEY="{key}"\n')