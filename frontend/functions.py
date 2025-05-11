import os, json, re
from journal_class import Journal

def load_json(path: str) -> dict:
    ''' Carga un archivo json '''
    with open(path, 'r', encoding='utf8') as f:
        return json.load(f)
    
def save_json(data: dict, path: str) -> None:
    ''' Guarda diccionario como archivo json '''
    with open(path, 'w', encoding='utf8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def check_path(path:str) -> bool:
    ''' Función para verificar si existe archivo '''
    if not os.path.exists(path):
        print(f"\nEl archivo en '{path}' no existe.")
        return False
    else:
        print(f"\nArchivo encontrado en '{path}'.")
        return True

def paginate(journals, page, per_page=20):
    ''' Devuelve revistas en una página y el total de páginas '''
    total = len(journals)
    total_pages = (total + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    return journals[start:end], total_pages

def get_authors():
    return [
        'Pedro Alan Escobedo Salazar',
        'Alejandro Leyva',
        'Alex Pacheco'
    ]

def get_search_results(search_text: str, journals: dict) -> list:
    search_words = search_text.lower().split()
    
    word_dict = {}

    for word in search_words:
        word_dict[word] = [r for r in journals if re.search(r'\b' + re.escape(word) + r'\b', r.title.lower())]

    found_journals = set()

    for word in word_dict:
        found_journals.update(word_dict[word])

    results = sorted(list(found_journals), key=lambda r: r.title.lower())
    return results

def load_journals(path: str) -> list:
    ''' Crea una lista con la clase Journal '''
    journal_json = load_json(path)

    journals = []
    for title, info in sorted(journal_json.items()):
        
        journal = Journal(
            id=info.get('id', ''),
            last_visit=info.get('last_visit', ''),
            title=title,
            areas=info.get('areas', []),
            catalogs=info.get('catalogs', []),
            website=info.get('website', ''),
            h_index=info.get('h_index', ''),
            subjet_area_and_category=info.get('subjet_area_and_category', {}),
            publisher=info.get('publisher', ''),
            issn=info.get('issn', ''),
            widget=info.get('widget', ''),
            publication_type=info.get('publication_type', '')
        )
        journals.append(journal)

    return journals