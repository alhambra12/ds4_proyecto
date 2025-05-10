import json, random, os, math

def load_json(path):
    with open(path, 'r', encoding='utf8') as f:
        return json.load(f)

def save_json(data, path):
    with open(path, 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def split_journals(journals, parts=3):
    """Divide el diccionario de revistas en partes iguales"""
    keys = list(journals.keys())
    random.shuffle(keys)  
    part_size = math.ceil(len(keys) / parts)
    
    # division  
    split_dicts = []
    for i in range(parts):
        start = i * part_size
        end = start + part_size
        chunk_keys = keys[start:end]
        split_dicts.append({k: journals[k] for k in chunk_keys})
    
    return split_dicts

if __name__ == '__main__':
    json_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'datos', 'json'))
    input_path = os.path.join(json_path, 'revistas_unison.json')
    
    journals_dict = load_json(input_path)
    split_parts = split_journals(journals_dict, parts=6)
    
    for i, part in enumerate(split_parts, start=1):
        output_path = os.path.join(json_path, f'revistas_unison_part{i}.json')
        save_json(part, output_path)
        print(f"Parte {i} guardada en {output_path} con {len(part)} revistas")
    
    print("\nDivisión completada exitosamente")