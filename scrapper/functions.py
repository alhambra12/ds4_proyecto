import json

''' Archivo de funciones '''

def load_json(path: str) -> dict:
    with open(path, 'r', encoding='utf8') as f:
        return json.load(f)