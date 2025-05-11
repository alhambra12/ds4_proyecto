import requests, json, time, random, Levenshtein
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36' 
}
scimagojr_search_url = 'https://www.scimagojr.com/journalsearch.php?q='
scimagojr_url = 'https://www.scimagojr.com'

def check_last_visit(journal, journals, journals_json_path):
    if journal and hasattr(journal, 'last_visit') and journal.last_visit:
        last_visit_date = datetime.strptime(journal.last_visit, '%Y-%m-%d')
        if datetime.now() - last_visit_date > timedelta(days=30):
            update_data(journal.id, journals, journals_json_path)

def update_data(journal_id: str, journals: list, journals_json_path: str):
    journal_obj = next((j for j in journals if j.id == journal_id), None)
    if not journal_obj:
        print(f"X No se encontró la revista con ID '{journal_id}'")
        return

    journal_name = journal_obj.title
    print(f"> Actualizando datos de: {journal_name}")

    url = find_journal_url(journal_name)
    if not url:
        print(f"X No se pudo obtener URL para '{journal_name}'")
        return

    new_data = get_journal_data(url)

    journal_obj.website = new_data.get('website')
    journal_obj.h_index = new_data.get('h_index')
    journal_obj.subjet_area_and_category = new_data.get('subjet_area_and_category')
    journal_obj.publisher = new_data.get('publisher')
    journal_obj.issn = new_data.get('issn')
    journal_obj.publication_type = new_data.get('publication_type')
    journal_obj.widget = new_data.get('widget')
    journal_obj.last_visit = datetime.now().strftime('%Y-%m-%d')

    # Guardar en el JSON
    try:
        journals_dict = {j.title: j.to_dict() for j in journals}  # Convertir objetos a diccionarios
        with open(journals_json_path, 'w', encoding='utf-8') as f:
            json.dump(journals_dict, f, ensure_ascii=False, indent=2)
        print(f"> Datos de '{journal_name}' actualizados y guardados.")
    except Exception as e:
        print(f"X Error guardando el archivo: {e}")

def scrap(url) -> requests.Response:
    ''' Función para obtener la pagina web desde internet '''
    time.sleep(random.uniform(0.5, 2))
    try:
        page = requests.get(url, headers=headers, timeout=15)
        if page.status_code != 200:
            time.sleep(5)
            return scrap(url)
        return page
    except Exception as e:
        time.sleep(2)
        raise e

def find_journal_url(title: str) -> str:
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

def get_website(soup: BeautifulSoup) -> str:
    ''' Función que obtiene la pagina web '''
    heading = soup.find('h2', string='Information')
    if heading:
        for a in heading.find_all_next('a', id='question_journal'):
            if 'Homepage' in a.text:
                return a['href'].strip()
    return None

def get_data(soup: BeautifulSoup, heading_text: str, html_tag: str, class_=None) -> str:
    ''' Función que busca datos '''
    heading = soup.find('h2', string=heading_text)
    if heading:
        text = heading.find_next(html_tag, class_=class_) if class_ else heading.find_next(html_tag)
        return text.text.strip() if text else None
    return None

def get_subject_area_and_category(soup: BeautifulSoup) -> list:
    ''' Función que obtiene el area y categorias '''
    result = {}
    heading = soup.find('h2', string='Subject Area and Category')
    if not heading:
        return None
    for area_li in heading.find_all_next('li', style="display: inline-block;"):
        area_tag = area_li.find('a')
        category_ul = area_li.find('ul', class_='treecategory')
        if area_tag and category_ul:
            area = area_tag.text.strip()
            categories = [cat.text.strip() for cat in category_ul.find_all('a')]
            result[area] = categories
    return result

def get_issn(soup: BeautifulSoup) -> list:
    ''' Función que obtiene el issn '''
    text = get_data(soup, 'ISSN', 'p')
    if text:
        return [issn.strip() for issn in text.split(',')] if text else None
    return None

def get_widget(soup: BeautifulSoup) -> str:
    ''' Función que obtiene el widget '''
    widget_div = soup.find('div', class_='widgetlegend')
    if widget_div:
        input_tag = widget_div.find('input', id='embed_code')
        if input_tag and input_tag.has_attr('value'):
            return input_tag['value']
    return None

def get_journal_data(url: str) -> dict:
    ''' Función que obtiene los datos de una revista '''
    
    # busca la revista en scimagojr
    try:
        journal_page = scrap(url)
    except Exception as e:
        print(f"X Error accediendo a '{url}': {e}")
    soup = BeautifulSoup(journal_page.text, 'html.parser')

    # obtiene datos de la revista
    data = {
        'website': get_website(soup),
        'h_index': get_data(soup, 'H-Index', 'p', 'hindexnumber'),
        'subjet_area_and_category': get_subject_area_and_category(soup),
        'publisher': get_data(soup, 'Publisher', 'a'),
        'issn': get_issn(soup),
        'publication_type': get_data(soup, 'Publication type', 'p'),
        'widget': get_widget(soup)
    }
    faltantes = [x for x, y in data.items() if y is None]
    if faltantes:
        print(f"! Datos faltantes: {', '.join(faltantes)}")
    else:
        print(f"Datos extraídos correctamente.")
    return data