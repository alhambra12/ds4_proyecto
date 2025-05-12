'''  Programa frontend de revistas '''

import os, argparse
from journal_update import check_last_visit
from journal_json import gen_journal_json
from functions import load_journals, check_path, paginate, get_authors, get_search_results
from users import delete_saved_journal, load_users, verify_user, register_user, save_journal_for_user, get_saved_journals, define_json_path
from flask import Flask, render_template, request, session, flash, redirect, url_for

def create_app(journals, journals_json_path, users):
    app = Flask(__name__)
    app.secret_key = os.urandom(24)

    @app.route('/')
    def index():
        username = session.get('username')
        return render_template('index.html', username=username)

    @app.route('/revistas/<id_journal>', methods=['GET', 'POST'])
    def journal(id_journal):
        journal = next((j for j in journals if j.id == id_journal), None)
        if request.method == 'POST':
            if not session.get('logged_in'):
                flash('Debes tener una sesion iniciada para guarda revista.', 'warning')
                return redirect(url_for('login'))

            username = session['username']
            save_journal_for_user(username, id_journal, users)
            flash('Revista guardada.', 'success')

        check_last_visit(journal, journals, journals_json_path)
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
    
    @app.route('/iniciar', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if verify_user(username, password, users):
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('index'))
            else:
                flash('Usuario o contraseña invalido.', 'danger')
        return render_template('login.html')
    
    @app.route('/registrarse', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if register_user(username, password, users):
                flash('Registro satisfactorio.', 'success')
                return redirect(url_for('login'))
            else:
                flash('El usuario ya existe.', 'danger')
        return render_template('register.html')

    @app.route('/salir')
    def logout():
        session.clear()
        flash('Tu sesion ha cerrado.', 'info')
        return redirect(url_for('index'))

    @app.route('/misrevistas')
    def my_journals():
        if not session.get('logged_in'):
            flash('Debes de tener una sesion iniciada.', 'warning')
            return redirect(url_for('login'))

        username = session['username']
        saved_ids = get_saved_journals(username, users)
        saved = [j for j in journals if j.id in saved_ids]

        return render_template('my_journals.html', journals=saved)
    
    @app.route('/eliminar/<journal_id>')
    def delete_journal(journal_id):
        if not session.get('logged_in'):
            flash('Debes iniciar sesión.', 'warning')
            return redirect(url_for('login'))

        username = session['username']
        if delete_saved_journal(username, journal_id):
            flash('Revista eliminada de tu lista.', 'success')
        else:
            flash('No se pudo eliminar la revista.', 'danger')

        return redirect(url_for('my_journals'))

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
    define_json_path(json_dir_path)
    users = load_users()
    app = create_app(journals, journals_json_path, users)
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