import json, random, os

def load_json(path):
    with open(path, 'r', encoding='utf8') as f:
        return json.load(f)

def save_json(data, path):
    with open(path, 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def aelect_journals(journals, amount=400):
    keys = list(journals.keys())
    selected = random.sample(keys, amount)
    return {k: journals[k] for k in selected}

if __name__ == '__main__':
    json_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'datos', 'json'))
    input_path = os.path.join(json_path, 'revistas_unison.json')
    output_path = os.path.join(json_path, 'revistas_unison_test.json')

    journals_dic = load_json(input_path)
    selected_journal = aelect_journals(journals_dic)
    save_json(selected_journal, output_path)