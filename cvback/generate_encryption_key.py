import os
import secrets

def main():
    base_dir = os.path.dirname(__file__)  # Ubicación base del script
    env_directory = os.path.join(base_dir, '.envs', '.local')
    env_file = os.path.join(env_directory, '.django')
    
    print(f"Verificando directorio: {env_directory}")
    
    # Crea los directorios si no existen
    if not os.path.exists(env_directory):
        os.makedirs(env_directory)
        print(f"Directorio creado: {env_directory}")
    else:
        print(f"Directorio ya existe: {env_directory}")
    
    # Verificar la existencia de cada clave y actuar en consecuencia
    keys_to_check = ['DJANGO_ENCRYPTED_FIELD_KEY', 'SECRET_KEY']
    keys_found = {key: False for key in keys_to_check}
    
    if os.path.exists(env_file):
        with open(env_file, 'r') as file:
            lines = file.readlines()
        print(f"Archivo encontrado. Revisando claves...")
        for key in keys_to_check:
            if any(key in line for line in lines):
                keys_found[key] = True
                print(f"Clave encontrada: {key}")
            else:
                print(f"Clave no encontrada: {key}")
    else:
        print(f"Archivo no encontrado. Se creará: {env_file}")
    
    # Actualizar el archivo .env si alguna clave no está presente
    with open(env_file, 'a') as file:
        for key in keys_to_check:
            if not keys_found[key]:
                if key == 'DJANGO_ENCRYPTED_FIELD_KEY':
                    new_key = secrets.token_hex(16)
                elif key == 'SECRET_KEY':
                    new_key = secrets.token_urlsafe(50)
                file.write(f'{key}="{new_key}"\n')
                print(f'{key} configurada: {new_key}')
            else:
                print(f'{key} ya está configurada.')

if __name__ == "__main__":
    main()
