import json, requests
from bs4 import BeautifulSoup
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36' 
     }
scimagojr_search_url = 'https://www.scimagojr.com/journalsearch.php?q='
scimagojr_search_url = 'https://www.scimagojr.com/journalsearch.php?q='

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
            results[title_result.text.strip()] = f"{scimagojr_search_url}/{a['href']}"
    if not results:
        print(f"X No hay resultados para '{title}'")
        return None

if __name__ == '__main__':
    title = 'FactaUniversitatis,Series:MechanicalEngineering'    
    url = find_journal_url(title)
    
