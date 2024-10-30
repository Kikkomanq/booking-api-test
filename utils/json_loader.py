import os
import json

def load_json(file_path):
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.abspath(os.path.join(script_dir, file_path))  
    if not os.path.exists(abs_file_path):
        raise FileNotFoundError(f"JSON file not found at path: {abs_file_path}")
    
    with open(abs_file_path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)