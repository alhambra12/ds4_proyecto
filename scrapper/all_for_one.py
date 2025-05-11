''' Script para juntar todas las partes del scrap '''

import os, json

def load_json(path: str) -> dict:
    with open(path, 'r', encoding='utf8') as f:
        return json.load(f)

def save_json(data, path: str) -> None:
    with open(path, 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def merge_json_files(json_dir_path: str, output_path: str) -> None:
    merged_data = {}
    for filename in sorted(os.listdir(json_dir_path)):
        if filename.startswith('revistas_scimagojr_part') and filename.endswith('.json'):
            file_path = os.path.join(json_dir_path, filename)
            data = load_json(file_path)
            merged_data.update(data)
    save_json(merged_data, output_path)

if __name__ == '__main__':
    json_filename = 'revistas_scimagojr.json'
    json_dir_path = os.path.join(os.path.dirname(__file__), '..', 'datos', 'json')
    output_path = os.path.join(json_dir_path, json_filename)

    merge_json_files(json_dir_path, output_path)
