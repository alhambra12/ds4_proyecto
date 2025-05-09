''' Archivo para generar json de revistas para frontend '''

import re, json, unicodedata

def load_json(path: str) -> dict:
    ''' Carga un archivo json '''
    with open(path, 'r', encoding='utf8') as f:
        return json.load(f)
    
def save_json(data: dict, path: str) -> None:
    ''' Guarda diccionario como archivo json '''
    with open(path, 'w', encoding='utf8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def unify_data(unison_json: dict, scimago_json: dict) -> dict:
    ''' Une solo los títulos que aparecen en ambos JSONs '''
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
    unison_json = load_json(unison_json_path)
    scimago_json = load_json(scimago_json_path)
    unified_json = unify_data(unison_json, scimago_json)
    save_json(json_dir_path, unified_json)