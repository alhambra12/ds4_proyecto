''' Archivo para generar json de revistas para frontend '''

import os, re, unicodedata
from functions import load_json, save_json

def unify_data(unison_json: dict, scimago_json: dict) -> dict:
    ''' Une las revistas que aparecen en ambos JSONs '''
    unified = {}

    # revistas que este en los dos jsons
    common_titles = set(unison_json) & set(scimago_json)

    for title in sorted(common_titles):
        id_value = create_id(title)
        data = {'id': id_value}

        data.update(unison_json[title])
        data.update(scimago_json[title])

        unified[title] = data

    return unified

def create_id(journal_title:str) -> str:
    ''' Función para crear un id con el nombre de la revista '''
    text = unicodedata.normalize('NFKD', journal_title).encode('ascii', 'ignore').decode('utf-8')
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def gen_journal_json(json_dir_path: str, unison_json_path: str, scimago_json_path: str) -> None:
    ''' Combina los datos de Unison y Scimago en un solo json '''
    print('\nGenerando archivo JSON.')
    unison_json = load_json(unison_json_path)
    scimago_json = load_json(scimago_json_path)
    unified_json = unify_data(unison_json, scimago_json)
    save_json(unified_json, json_dir_path)
    print(f"Archivo JSON guardado en '{json_dir_path}'.")

if __name__ == '__main__':
    journals_json_filename = 'journals.json'
    unison_json_filename = 'revistas_unison_test.json'
    scimago_json_filename = 'revistas_scimagojr_test.json'

    json_dir_path = os.path.join(os.path.dirname(__file__), '..', 'datos', 'json')
    journals_json_path = os.path.join(json_dir_path, journals_json_filename)
    unison_json_path = os.path.join(json_dir_path, unison_json_filename)
    scimago_json_path = os.path.join(json_dir_path, scimago_json_filename)

    gen_journal_json(journals_json_path, unison_json_path, scimago_json_path)