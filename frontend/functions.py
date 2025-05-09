import os, json
from journal_class import Journal

def load_json(path: str) -> dict:
    ''' Carga un archivo json '''
    with open(path, 'r', encoding='utf8') as f:
        return json.load(f)

def check_path(path:str) -> bool:
    ''' Función para verificar si existe archivo '''
    if not os.path.exists(path):
        print(f"\nEl archivo en '{path}' no existe.")
        return False
    else:
        print(f"\nArchivo encontrado en '{path}'.")
        return True

def load_journals(path: str) -> list:
    ''' Crea una lista con la clase Journal '''
    journal_json = load_json(path)

    journals = []
    for idx, (title, info) in enumerate(sorted(journal_json.items())):
        journal = Journal(
            id=str(idx),
            title=title,
            areas=info.get('areas', []),
            catalogs=info.get('catalogs', []),
            website=info.get('website', ''),
            h_index=info.get('h_index', ''),
            subjet_area_and_category=info.get('subjet_area_and_category', []),
            publisher=info.get('publisher', ''),
            issn=info.get('issn', ''),
            widget=info.get('widget', ''),
            publication_type=info.get('publication_type', '')
        )
        journals.append(journal)

    return journals