import json, requests
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36' 
     }

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

if __name__ == '__main__':
    try:
        response = scrap("https://www.scimagojr.com")
        print(response.text)  # muestra el html
    except Exception as e:
        print(f"Error al obtener la página: {e}")
