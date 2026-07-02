"""Утилиты экспорта."""
import json
import csv
import os
from typing import List, Dict, Any

def export_to_json(data: Any, filepath: str):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)

def export_to_csv(results: List[Dict[str, Any]], filepath: str):
    if not results:
        return
    keys = results[0].keys()
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)

def ensure_dir(path: str):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
