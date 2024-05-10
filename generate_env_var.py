import os
import secrets

def main():
    base_dir = os.path.dirname(__file__)  # Ubicación base del script
    env_directory = os.path.join(base_dir, '.envs', '.local')
    env_file_django = os.path.join(env_directory, '.django')
    env_file_postgres = os.path.join(env_directory, '.postgres')
    
    print(f"Verificando directorio: {env_directory}")
    
    # Crea los directorios si no existen
    if not os.path.exists(env_directory):
        os.makedirs(env_directory)
        print(f"Directorio creado: {env_directory}")
    else:
        print(f"Directorio ya existe: {env_directory}")
    
    # Verificar la existencia de cada clave y actuar en consecuencia
    keys_to_check_django = ['USE_DOCKER',
                            'IPYTHONDIR',
                            'DJANGO_READ_DOT_ENV_FILE',
                            'DJANGO_ENCRYPTED_FIELD_KEY', 
                            'SECRET_KEY']
    
    keys_found_django = {key: False for key in keys_to_check_django}
    
    keys_to_check_postgres = ['POSTGRES_HOST', 
                            'POSTGRES_PORT', 
                            'POSTGRES_DB',
                            'POSTGRES_USER', 
                            'POSTGRES_PASSWORD']
    
    keys_found_postgres = {key: False for key in keys_to_check_postgres}

    
    if os.path.exists(env_file_django):
        with open(env_file_django, 'r') as file:
            lines = file.readlines()
        print(f"Archivo encontrado. Revisando claves...")
        for key in keys_to_check_django:
            if any(key in line for line in lines):
                keys_found_django[key] = True
                print(f"Clave encontrada: {key}")
            else:
                print(f"Clave no encontrada: {key}")
    else:
        print(f"Archivo no encontrado. Se creará: {env_file_django}")
        
    if os.path.exists(env_file_postgres):
        with open(env_file_postgres, 'r') as file:
            lines = file.readlines()
        print(f"Archivo encontrado. Revisando claves...")
        for key in keys_to_check_postgres:
            if any(key in line for line in lines):
                keys_found_postgres[key] = True
                print(f"Clave encontrada: {key}")
            else:
                print(f"Clave no encontrada: {key}")
    else:
        print(f"Archivo no encontrado. Se creará: {env_file_postgres}")
    
    # Actualizar el archivo .env si alguna clave no está presente
    with open(env_file_django, 'a') as file:
        for key in keys_to_check_django:
            if not keys_found_django[key]:
                if key == 'USE_DOCKER':
                    new_key = 'yes'
                elif key == 'IPYTHONDIR':
                    new_key = '/app/.ipython'
                elif key == 'DJANGO_READ_DOT_ENV_FILE':
                    new_key = True
                elif key == 'GDAL_LIBRARY_PATH':
                    new_key = '/usr/local/Cellar/gdal/3.8.1_1/lib/libgdal.dylib'
                elif key == 'DJANGO_ENCRYPTED_FIELD_KEY':
                    new_key = secrets.token_hex(16)
                elif key == 'SECRET_KEY':
                    new_key = secrets.token_urlsafe(64)
                file.write(f'{key}="{new_key}"\n')
                print(f'{key} configurada: {new_key}')
            else:
                print(f'{key} ya está configurada.')
                
    # Actualizar el archivo .env si alguna clave no está presente
    with open(env_file_postgres, 'a') as file:
        for key in keys_to_check_postgres:
            if not keys_found_postgres[key]:
                if key == 'POSTGRES_HOST':
                    new_key = 'postgres'
                elif key == 'POSTGRES_PORT':
                    new_key = 5432
                elif key == 'POSTGRES_DB':
                    new_key = 'cvback'
                elif key == 'POSTGRES_USER':
                    new_key = secrets.token_hex(16)
                elif key == 'POSTGRES_PASSWORD':
                    new_key = secrets.token_hex(32)
                    
                file.write(f'{key}="{new_key}"\n')
                print(f'{key} configurada: {new_key}')
            else:
                print(f'{key} ya está configurada.')

if __name__ == "__main__":
    main()
