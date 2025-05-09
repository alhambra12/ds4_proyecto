''' Archivo para generar json de revistas para frontend '''

import json

def load_json(path: str) -> dict:
    ''' Carga un archivo json '''
    with open(path, 'r', encoding='utf8') as f:
        return json.load(f)