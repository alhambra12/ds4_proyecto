'''  Programa frontend de revistas '''

import os, argparse
from flask import Flask, render_template

app = Flask(__name__)

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
scimago_json = os.path.join(json_dir_path, scimago_json_filename)



@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)