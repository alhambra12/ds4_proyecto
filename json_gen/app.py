import os, csv, json, argparse

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
    
    
def main(csv_dir_path:str, output_path:str):
    ''' Función Principal '''

    dir_areas = os.path.join(csv_dir_path, 'areas')
    dir_catalogs = os.path.join(csv_dir_path, 'catalogos')