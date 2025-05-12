import os, sys, subprocess

ruta_base = os.path.normpath(os.path.dirname(__file__))

def start_json_gen():
    ''' Función para ejecutar el generador de json '''
    subprocess.run([
        sys.executable,
        os.path.join(ruta_base, 'json_gen', 'app.py'),
        '--datos_dir_path', os.path.join(ruta_base, 'datos'),
        '--output_filename', 'revistas_unison.json'
    ])

def start_scrapper():
    ''' Función para ejecutar el scrapper de scimagojr '''
    subprocess.run([
        sys.executable,
        os.path.join(ruta_base, 'scrapper', 'app.py'),
        '--datos_dir_path', os.path.join(ruta_base, 'datos'),
        '--input_filename', 'revistas_unison.json',
        '--output_filename', 'revistas_scimagojr1.json',
        '--workers', '3'
    ])

def start_frontend():
    ''' Función para ejecutar el front-end '''
    subprocess.run([
        sys.executable,
        os.path.join(ruta_base, 'frontend', 'app.py'),
        '--json_dir_path', os.path.join(ruta_base, 'datos', 'json'),
        '--unison_json_filename', 'revistas_unison.json',
        '--scimago_json_filename', 'revistas_scimagojr.json'
    ])


def main():
    ''' Función principal '''
    print("\n¿Qué programa deseas ejecutar?")
    print("1. Ejecutar JSON Generator")
    print("2. Ejecutar Scrapper")
    print("3. Ejecutar Front-End")
    print("4. Salir")

    opcion = input("Selecciona una opción: ").strip()

    match opcion:
        case '1':
            start_json_gen()
        case '2':
            start_scrapper()
        case '3':
            start_frontend()
        case '4':
            print("\nSaliendo del programa.\n")
        case _:
            print("\nOpción no válida.\n")

if __name__ == '__main__':
    main()
