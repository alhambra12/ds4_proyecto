'''  Programa frontend de revistas '''

import os, argparse
from journal_json import gen_journal_json
from functions import load_journals, check_path, paginate
from flask import Flask, render_template, request

def create_app(journals):
    app = Flask(__name__)

    per_page = 20

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/revistas/<id_journal>')
    def journal(id_journal):
        journal = next((j for j in journals if j.id == id_journal), None)
        return render_template('journal.html', journal=journal)

    @app.route('/areas')
    def areas():
        areas = set()
        for journal in journals:
            areas.update(journal.areas)
        return render_template('filter_selection.html', filter_type='areas', filter_list=sorted(areas))

    @app.route('/areas/<area>')
    def journals_area(area):
        page = int(request.args.get('page', 1))
        journals_by_area = [j for j in journals if area in j.areas]
        paginated, total_pages = paginate(journals_by_area, page)

        return render_template(
            'filter_results.html',
            journals=paginated,
            filter=area,
            filter_type='areas',
            page=page,
            total_pages=total_pages
        )

    @app.route('/catalogos')
    def catalogs():
        catalogs_set = set()
        for journal in journals:
            catalogs_set.update(journal.catalogs)
        return render_template('filter_selection.html', filter_type='catalogs', filter_list=sorted(catalogs_set))

    @app.route('/catalogos/<catalogs>')
    def journals_catalog(catalogs):
        page = int(request.args.get('page', 1))
        journals_by_catalog = [j for j in journals if catalogs in j.catalogs]
        paginated, total_pages = paginate(journals_by_catalog, page)

        return render_template(
            'filter_results.html',
            journals=paginated,
            filter=catalogs,
            filter_type='areas',
            page=page,
            total_pages=total_pages
        )

    return app

def main(json_dir_path, unison_json_filename, scimago_json_filename):
    global journals

    print('\nIniciando programa.')

    journals_json_filename = 'journals.json'
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
    unison_json_filename = args.unison_json_filename or 'revistas_unison_test.json'
    scimago_json_filename = args.scimago_json_filename or 'revistas_scimagojr_test.json'

    json_dir_path = os.path.normpath(json_dir_path)

    main(json_dir_path, unison_json_filename, scimago_json_filename)