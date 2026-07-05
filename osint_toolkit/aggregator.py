import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from .utils.cache import CacheManager
from .utils.html_report import generate_html_report
from .ui import console, print_success, print_error, print_info


class Aggregator:
    def __init__(self):
        self.results: Dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "email_results": [],
            "username_results": [],
            "exif_results": {},
            "phone_results": {},
            "domain_results": {},
            "summary": {},
        }
        self.cache = CacheManager()

    def add_email_results(self, email: str, results: List[Dict]):
        self.results["email"] = email
        self.results["email_results"] = results
        self.cache.set_email(email, results)

    def get_cached_email(self, email: str) -> Optional[List[Dict]]:
        return self.cache.get_email(email)

    def add_username_results(self, username: str, results: List[Dict]):
        self.results["username"] = username
        self.results["username_results"] = results
        self.cache.set_username(username, results)

    def get_cached_username(self, username: str) -> Optional[List[Dict]]:
        return self.cache.get_username(username)

    def add_exif_results(self, path: str, result: Dict):
        self.results["exif_results"] = result

    def add_phone_results(self, phone: str, result: Dict):
        self.results["phone"] = phone
        self.results["phone_results"] = result

    def add_domain_results(self, domain: str, result: Dict):
        self.results["domain"] = domain
        self.results["domain_results"] = result

    def print_summary(self):
        email_found = sum(
            1 for r in self.results.get("email_results", [])
            if r.get("exists")
        )
        username_found = sum(
            1 for r in self.results.get("username_results", [])
            if r.get("exists")
        )
        exif = self.results.get("exif_results", {})
        gps = "✓ GPS найден" if (exif and exif.get("gps")) else "✗ GPS отсутствует"
        self.results["summary"] = {
            "email_found": email_found,
            "username_found": username_found,
            "exif_gps": gps,
            "timestamp": self.results["timestamp"],
        }
        console.print("\n[bold cyan]📊 Сводка по цели[/bold cyan]")
        console.print(f"  📧 Email найден в сервисах: {email_found}")
        console.print(f"  👤 Username найдено аккаунтов: {username_found}")
        console.print(f"  🖼️ EXIF GPS: {gps}")

    def export_json(self, filename: str):
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2, default=str)
            print_success(f"Отчёт JSON сохранён: {os.path.abspath(filename)}")
        except Exception as e:
            print_error(f"Ошибка сохранения JSON: {e}")

    def export_html(self, filename: str):
        try:
            html = generate_html_report(self.results)
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html)
            print_success(f"Отчёт HTML сохранён: {os.path.abspath(filename)}")
        except Exception as e:
            print_error(f"Ошибка сохранения HTML: {e}")
            import traceback
            traceback.print_exc()