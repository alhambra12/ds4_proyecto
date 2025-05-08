'''  Programa frontend de revistas '''

import os, argparse
from flask import Flask

app = Flask(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('--dir_json', type=str, help='Directorio de JSONs')
parser.add_argument('--unison_json', type=str, help='Archivo de json con los datos de la universidad')
parser.add_argument('--scimago_json', type=str, help='Archivo de json con los datos de scimagojr')
args = parser.parse_args()

dir_json = args.dir_json or os.path.join(os.path.dirname(__file__), '..', 'datos', 'json')
unison_json = args.unison_json or 'revistas_unison_test.json'
scimago_json = args.scimago_json or 'revistas_scimagojr_test.json'

if __name__ == '__main__':
    app.run(debug=True)