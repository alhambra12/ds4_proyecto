'''  Programa frontend de revistas '''

import os, argparse
from functions import load_journals
from flask import Flask, render_template

app = Flask(__name__)
journals = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/areas')
def areas():
    areas_set = set()
    for journal in journals:
        areas_set.update(journal.areas)
    return render_template('option_selection.html', option_type='areas', options_list=sorted(areas_set))

@app.route('/areas/<area>')
def journals_area(area):
    journals_by_area = [j for j in journals if area in j.areas]
    return render_template('option_results.html', journals=journals_by_area, option=area, option_type='areas')

@app.route('/catalogos')
def catalogs():
    catalogs_set = set()
    for journal in journals:
        catalogs_set.update(journal.catalogs)
    return render_template('option_selection.html', option_type='catalogs', options_list=sorted(catalogs_set))

@app.route('/catalogos/<catalogs>')
def journals_catalog(catalogs):
    journals_by_catalog = [j for j in journals if catalogs in j.catalogs]
    return render_template('option_results.html', journals=journals_by_catalog, option=catalogs, option_type='areas')

def main(json_dir_path, unison_json_path, scimago_json_path):
    global journals
    journals_json = 'revista.json'
    journals = load_journals(os.path.join(json_dir_path, journals_json))

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
    unison_json_path = os.path.join(json_dir_path, unison_json_filename)
    scimago_json_path = os.path.join(json_dir_path, scimago_json_filename)

    main(json_dir_path, unison_json_path, scimago_json_path)