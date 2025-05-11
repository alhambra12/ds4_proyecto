'''  Programa frontend de revistas '''

import os, argparse 
from journal_json import gen_journal_json
from functions import load_journals, check_path, paginate, get_authors, get_search_results
from flask import Flask, render_template, request

def create_app(journals):
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/revistas/<id_journal>')
    def journal(id_journal):
        journal = next((j for j in journals if j.id == id_journal), None)
        return render_template('journal.html', journal=journal)

    @app.route('/areas')
    def areas():
        areas_set = set()
        for journal in journals:
            areas_set.update(journal.areas)
        return render_template('filter_selection.html', filter_type='areas', filter_list=sorted(areas_set))

    @app.route('/areas/<area>')
    def journals_area(area):
        search_text = request.args.get('q', '').strip().lower()
        page = int(request.args.get('pagina', 1)) 
        journals_by_area = [j for j in journals if area in j.areas]

        if search_text:
            journals_by_area = [j for j in journals_by_area if search_text in j.title.lower()]

        paginated, total_pages = paginate(journals_by_area, page)

        return render_template(
            'filter_results.html',
            journals=paginated,
            filter=area,
            filter_type='areas',
            page=page,
            total_pages=total_pages,
            search_text=search_text
        )

    @app.route('/catalogos')
    def catalogs():
        catalogs_set = set()
        for journal in journals:
            catalogs_set.update(journal.catalogs)
        return render_template('filter_selection.html', filter_type='catalogs', filter_list=sorted(catalogs_set))

    @app.route('/catalogos/<catalog>')
    def journals_catalog(catalog):
        search_text = request.args.get('q', '').strip().lower()
        page = int(request.args.get('pagina', 1))
        journals_by_catalog = [j for j in journals if catalog in j.catalogs]

        if search_text:
            journals_by_catalog = [j for j in journals_by_catalog if search_text in j.title.lower()]

        paginated, total_pages = paginate(journals_by_catalog, page)

        return render_template(
            'filter_results.html',
            journals=paginated,
            filter=catalog,
            filter_type='catalogs',
            page=page,
            total_pages=total_pages,
            search_text=search_text
        )
    
    @app.route('/explorar')
    def explore():
        import string
        from flask import request, render_template

        letter = request.args.get('letra', '').upper()
        letters = list(string.ascii_uppercase)
        page = int(request.args.get('pagina', 1))

        if letter:
            results = [j for j in journals if j.title.upper().startswith(letter)]
        else:
            results = journals
        results.sort(key=lambda r: r.title.lower())

        paginated, total_pages = paginate(results, page)

        return render_template(
            'explore.html',
            letters=letters,
            selected_letter=letter,
            journals=paginated,
            page=page,
            total_pages=total_pages
        )
    
    @app.route('/busqueda')
    def search():
        search_text = request.args.get('q', '').strip()
        page = int(request.args.get('pagina', 1))
        search_results = []

        if search_text:
            search_results = get_search_results(search_text, journals)

        paginated, total_pages = paginate(search_results, page)

        return render_template(
            'search.html',
            journals=paginated,
            search_text=search_text,
            page=page,
            total_pages=total_pages
        )
    
    @app.route('/creditos')
    def credits():
        authors = get_authors()
        return render_template('credits.html', authors=authors)

    return app

def main(json_dir_path, unison_json_filename, scimago_json_filename):
    global journals

    print('\nIniciando programa.')

    journals_json_filename = 'revistas.json'
    journals_json_path = os.path.join(json_dir_path, journals_json_filename)
    unison_json_path = os.path.join(json_dir_path, unison_json_filename)
    scimago_json_path = os.path.join(json_dir_path, scimago_json_filename)

    if check_path(journals_json_path) is False:
        if check_path(unison_json_path) is False:
            print('\nPrograma finalizado.\n')
            return
        if check_path(scimago_json_path) is False:
            print('\nPrograma finalizado.\n')
            return
        gen_journal_json(journals_json_path, unison_json_path, scimago_json_path)

    journals = load_journals(journals_json_path)

    print('\nIniciando app Flask.\n')
    app = create_app(journals)
    app.run(debug=True) 

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--json_dir_path', type=str, help='Directorio de JSONs')
    parser.add_argument('--unison_json_filename', type=str, help='Archivo de json con los datos de la universidad')
    parser.add_argument('--scimago_json_filename', type=str, help='Archivo de json con los datos de scimagojr')
    args = parser.parse_args()

    json_dir_path = args.json_dir_path or os.path.join(os.path.dirname(__file__), '..', 'datos', 'json')
    unison_json_filename = args.unison_json_filename or 'revistas_unison.json'
    scimago_json_filename = args.scimago_json_filename or 'revistas_scimagojr.json'

    json_dir_path = os.path.normpath(json_dir_path)

    main(json_dir_path, unison_json_filename, scimago_json_filename)