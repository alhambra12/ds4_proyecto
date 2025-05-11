''' Programa scrapper para scimagojr.com '''

import argparse, os
from multiprocessing import Pool, cpu_count
from functions import load_json, find_journal_url, get_journal_data, save_json

def process_journal(journal_title, max_retries=3):
    '''Funcion para procesar una revista'''
    attempts = 0
    while attempts < max_retries:
        attempts += 1
        print(f"- Procesando: {journal_title}")
        journal_url = find_journal_url(journal_title)
        if journal_url:
            data = get_journal_data(journal_url, journal_title)
            if data:
                return (journal_title, data)
            else: 
                print(f"X No se pudieron extraer datos para '{journal_title}'.")
        return (journal_title, None)
    
def main(input_path:str, output_path:str, workers: int = None):

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

    print('\nIniciando scrapeo\n')

    # numero de workers 
    num_workers = workers if workers else min(3, cpu_count())

    # procesamiento en paralelo
    with Pool(num_workers) as pool:
        results = pool.map(process_journal, journal_json.keys())

    # combinamos resultados
    journal_data = {k: v for k, v in results if v is not None}

    # guardar json  
    save_json(journal_data, output_path)
    print(f"\nArchivo JSON guardado en '{output_path}'.")
    print(f"Se procesaron {len(journal_data)}/{len(journal_json)} revistas.")
    print("\nPrograma finalizado.\n")

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--datos_dir_path', type=str, help='Ruta de la carpeta datos')
    parser.add_argument('--input_filename', type=str, help='Archivo de entrada')
    parser.add_argument('--output_filename', type=str, help='Archivo de salida')
    parser.add_argument('--workers', type=int, default=3, help='Numero de workers paralelos')
    args = parser.parse_args()

    datos_dir_path = args.datos_dir_path or os.path.join(os.path.dirname(__file__), '..', 'datos')
    input_filename = args.input_filename or 'revistas_unison_part1.json'
    output_filename = args.output_filename or 'revistas_scimagojr_test.json'

    json_dir_path = os.path.normpath(os.path.join(datos_dir_path, 'json'))
    input_path = os.path.join(json_dir_path, input_filename)
    output_path = os.path.join(json_dir_path, output_filename)

    main(input_path, output_path, args.workers)
