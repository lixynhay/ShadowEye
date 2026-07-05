"""Утилиты экспорта."""
import csv
import json
import os
from typing import Any, Dict, List


def export_to_json(data: Any, filepath: str):
    ensure_dir(filepath)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)


def export_to_csv(results: List[Dict[str, Any]], filepath: str):
    if not results:
        return
    ensure_dir(filepath)
    keys = list(results[0].keys())
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)


def ensure_dir(path: str):
    parent = os.path.dirname(os.path.abspath(path))
    if parent:
        os.makedirs(parent, exist_ok=True)
