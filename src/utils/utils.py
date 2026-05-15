import json
import os
import hashlib
from typing import Dict, Any

def get_message_template(donation_type: str) -> Dict[str, Any]:

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'etc', 'messages_template.json')

    with open(file_path, 'r', encoding='utf-8') as f:
        templates = json.load(f)

    return templates.get("donation_type", {}).get(donation_type, {})

def hash_api_key(api_key: str) -> str:
    return hashlib.sha256(api_key.encode("utf-8")).hexdigest()
