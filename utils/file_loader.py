import yaml, json

def load_spec(filepath: str) -> dict:
    with open(filepath) as f:
        if filepath.endswith(('.yaml', '.yml')):
            return yaml.safe_load(f)
        return json.load(f)