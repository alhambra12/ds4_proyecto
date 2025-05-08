import os, csv, json, argparse  
    
def check_dir(dir_path:str) -> bool:
    if not os.path.exists(dir_path):
        print(f"No existe el directorio '{dir_path}'.")
        return False
    print(f"Directorio encontrado en '{dir_path}'.")
    files = os.listdir(dir_path)
    if not files:
        print(f"El directorio '{dir_path}' esta vacio.")
        return False
    csv_files = [f for f in files if f.lower().endswith('.csv')]
    if not csv_files:
        print(f"El directorio '{dir_path}' no contiene archivos CSV.")
        return False
    return True

def main(csv_dir_path:str, output_path:str):
    ''' Función Principal '''

    dir_areas = os.path.join(csv_dir_path, 'areas')
    dir_catalogs = os.path.join(csv_dir_path, 'catalogos')

    # verifica si existen los directorios y contienen csv.
    print('\nVerificando directorio de areas:')
    if not check_dir(dir_areas):
        print("\nPrograma finalizado.\n")
        return
    print('\nVerificando directorio de catalogos:')
    if not check_dir(dir_catalogs):
        print("\nPrograma finalizado.\n")
        return

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--datos_dir_path', type=str, help='Ruta de la carpeta datos')
    parser.add_argument('--output_filename', type=str, help='Archivo de salida')
    args = parser.parse_args()

    datos_dir_path = args.datos_dir_path or os.path.join(os.path.dirname(__file__), '..', 'datos')
    output_filename = args.output_filename or 'revistas_unison.json'
    
    datos_dir_path = os.path.normpath(datos_dir_path)
    csv_dir_path = os.path.join(datos_dir_path, 'csv')
    output_path = os.path.join(datos_dir_path, 'json', output_filename)
    
    main(csv_dir_path, output_path)