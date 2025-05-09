import json, requests, Levenshtein
from bs4 import BeautifulSoup
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36' 
     }
scimagojr_search_url = 'https://www.scimagojr.com/journalsearch.php?q='
scimagojr_url = 'https://www.scimagojr.com'

''' Archivo de funciones '''

def load_json(path: str) -> dict:
    with open(path, 'r', encoding='utf8') as f:
        return json.load(f)
    
def scrap(url) -> requests.Response:
    ''' Función para obtener la pagina web desde internet '''
    page = requests.get(url, headers=headers, timeout=15)
    if page.status_code != 200:
        raise Exception(f"X Error: {page.status_code} en '{url}'")
    return page

def find_journal_url(title:str) -> str:
    ''' Función que devuelve la url de una revista a partir de su nombre '''
    
    # busca la revista en scimagojr
    journal_search_url = f"{scimagojr_search_url}{title.replace(' ', '+')}"
    try:
        search_page = scrap(journal_search_url)
    except Exception as e:
        print(f"X Error buscando '{title}': {e}")
        return None
    soup = BeautifulSoup(search_page.text, 'html.parser')
    
    # crea un diccionario con el nombre de la revista y su url
    results = {}
    for a in soup.select('a[href^="journalsearch.php?q="]'):
        title_result = a.select_one('span.jrnlname')
        if title_result:
            results[title_result.text.strip()] = f"{scimagojr_url}/{a['href']}"
    if not results:
        print(f"X No hay resultados para '{title}'")
        return None
    
    # seleccionar el resultado mas similar
    best_result = max(results.keys(), key=lambda x: Levenshtein.ratio(title.lower(), x.lower()))
    ratio = Levenshtein.ratio(title.lower(), best_result.lower())
    if ratio < 0.9:
        print(f"X No hay resultados similares a '{title}'")
        return None
    print(f"URL encontrada: '{results[best_result]}'")
    return results[best_result]

def get_journal_data(url:str) -> dict:
    ''' Función que obtiene los datos de una revista '''
    
    # busca la revista en scimagojr
    try:
        journal_page = scrap(url)
    except Exception as e:
        print(f"X Error accediendo a '{url}': {e}")
    soup = BeautifulSoup(journal_page.text, 'html.parser')

    # obtiene datos de la revista
    data = {
        'website': ,
        'h_index': ,
        'subjet_area_and_category': ,
        'publisher': ,
        'issn': ,
        'publication_type': ,
        'widget':
    }

if __name__ == '__main__':
    title = 'Facta Universitatis, Series: Mechanical Engineering'    
    url = find_journal_url(title)
    
