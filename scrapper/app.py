''' Programa scrapper para scimagojr.com '''

import argparse, os
from functions import load_json, save_json, find_journal_url, get_journal_data

def main(input_path:str, output_path:str):

    # verificar si el archivo de entrada existe
    if not os.path.exists(input_path):
        print(f"\nEl archivo de entrada en '{input_path}' no existe.")
        return
    print(f"\nArchivo de entrada encontrado en '{input_path}'.")

    # verificar si no existe el archivo de salida
    if os.path.exists(output_path):
        response = input(f"\nEl archivo de salida en '{output_path}' ya existe. ¿Desea eliminarlo? (s/n): ").strip().lower()
        if response == 's':
            os.remove(output_path)
            print(f"\nArchivo en '{output_path}' eliminado.")
        else:    
            print('\nPrograma finalizado.\n')
            return
    
    # cargar json
    journal_json = load_json(input_path)

        # buscar y obtener datos de cada revista
    journal_data = {}
    print("\nProcesando revistas:")
    for journal_title in journal_json:
        print(f"\n- Procesando: {journal_title}")
        journal_url = find_journal_url(journal_title)
        if journal_url:
            data = get_journal_data(journal_url)
            if data:
                journal_data[journal_title] = data
            else:
                print(f"X No se pudieron extraer datos para '{journal_title}'.")
                

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--datos_dir_path', type=str, help='Ruta de la carpeta datos')
    parser.add_argument('--input_filename', type=str, help='Archivo de entrada')
    parser.add_argument('--output_filename', type=str, help='Archivo de salida')
    args = parser.parse_args()

    datos_dir_path = args.datos_dir_path or os.path.join(os.path.dirname(__file__), '..', 'datos')
    input_filename = args.input_filename or 'revistas_unison_test.json'
    output_filename = args.output_filename or 'revistas_scimagojr_test.json'

    json_dir_path = os.path.normpath(os.path.join(datos_dir_path, 'json'))
    input_path = os.path.join(json_dir_path, input_filename)
    output_path = os.path.join(json_dir_path, output_filename)

    main(input_path, output_path)
