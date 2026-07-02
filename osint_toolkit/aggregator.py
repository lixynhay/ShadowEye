"""Агрегатор результатов от всех инструментов."""
import json
import os
from datetime import datetime
from typing import Dict, Any, List
from .ui import console, print_success, print_info, print_stats
from .utils.cache import CacheManager

class Aggregator:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "email": None,
            "username": None,
            "image": None,
            "email_results": [],
            "username_results": [],
            "exif_results": [],
            "summary": {}
        }
        self.cache = CacheManager()
    
    def add_email_results(self, email: str, results: list, use_cache: bool = True):
        """Добавить результаты email проверки."""
        self.results["email"] = email
        self.results["email_results"] = results
        self._update_summary()
        
        if use_cache:
            self.cache.set_email(email, results)
    
    def get_cached_email(self, email: str) -> list:
        """Получить кэшированные результаты email."""
        return self.cache.get_email(email)
    
    def add_username_results(self, username: str, results: list, use_cache: bool = True):
        """Добавить результаты username проверки."""
        self.results["username"] = username
        self.results["username_results"] = results
        self._update_summary()
        
        if use_cache:
            self.cache.set_username(username, results)
    
    def get_cached_username(self, username: str) -> list:
        """Получить кэшированные результаты username."""
        return self.cache.get_username(username)
    
    def add_exif_results(self, image_path: str, results: dict):
        """Добавить результаты EXIF анализа."""
        self.results["image"] = image_path
        self.results["exif_results"] = results
        self._update_summary()
    
    def _update_summary(self):
        """Обновить сводку."""
        summary = {}
        
        if self.results["email_results"]:
            found = sum(1 for r in self.results["email_results"] if r.get("exists"))
            summary["email_found"] = found
            summary["email_total"] = len(self.results["email_results"])
        
        if self.results["username_results"]:
            found = sum(1 for r in self.results["username_results"] if r.get("exists"))
            summary["username_found"] = found
            summary["username_total"] = len(self.results["username_results"])
        
        if self.results["exif_results"] and not self.results["exif_results"].get("error"):
            summary["exif_tags"] = self.results["exif_results"].get("tags_count", 0)
            if self.results["exif_results"].get("gps"):
                summary["has_gps"] = True
        
        self.results["summary"] = summary
    
    def export_json(self, filepath: str):
        """Экспорт в JSON."""
        try:
            # Если путь начинается с / — используем текущую директорию
            if filepath.startswith('/'):
                filepath = filepath.lstrip('/')
            
            # Если нет расширения — добавляем
            if not filepath.endswith('.json'):
                filepath += '.json'
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2, default=str)
            print_success(f"Результаты сохранены в {filepath}")
        except Exception as e:
            console.print(f"[bold red]✗ Ошибка экспорта: {e}[/bold red]")
    
    def export_html(self, filepath: str):
        """Экспорт в HTML."""
        try:
            # Если путь начинается с / — используем текущую директорию
            if filepath.startswith('/'):
                filepath = filepath.lstrip('/')
            
            # Если нет расширения — добавляем
            if not filepath.endswith('.html'):
                filepath += '.html'
            
            html = self._generate_html()
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
            print_success(f"HTML отчёт сохранён в {filepath}")
        except Exception as e:
            console.print(f"[bold red]✗ Ошибка экспорта HTML: {e}[/bold red]")
    
    def _generate_html(self) -> str:
        """Генерация HTML отчёта."""
        html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OSINT Report - {self.results['timestamp']}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .header p {{ opacity: 0.9; }}
        .content {{ padding: 30px; }}
        .section {{
            margin-bottom: 30px;
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .section h2 {{
            color: #667eea;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .stat-card .number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-card .label {{
            color: #666;
            margin-top: 5px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 10px;
            overflow: hidden;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }}
        th {{
            background: #667eea;
            color: white;
            font-weight: 600;
        }}
        tr:hover {{ background: #f5f5f5; }}
        .found {{ color: #10b981; font-weight: bold; }}
        .not-found {{ color: #ef4444; }}
        .error {{ color: #f59e0b; }}
        .gps-map {{
            width: 100%;
            height: 400px;
            border-radius: 10px;
            margin-top: 15px;
        }}
        .search-box {{
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 2px solid #667eea;
            border-radius: 5px;
            font-size: 1em;
        }}
        .tag {{
            display: inline-block;
            padding: 3px 10px;
            background: #667eea;
            color: white;
            border-radius: 15px;
            font-size: 0.85em;
            margin: 2px;
        }}
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 1.8em; }}
            .content {{ padding: 15px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 OSINT Toolkit Pro Report</h1>
            <p>Дата: {self.results['timestamp']}</p>
        </div>
        <div class="content">
"""
        
        # Статистика
        summary = self.results.get('summary', {})
        if summary:
            html += """
            <div class="stats">
"""
            for key, value in summary.items():
                label = key.replace('_', ' ').title()
                html += f"""
                <div class="stat-card">
                    <div class="number">{value}</div>
                    <div class="label">{label}</div>
                </div>
"""
            html += """
            </div>
"""
        
        # Email результаты
        if self.results["email_results"]:
            html += f"""
            <div class="section">
                <h2>📧 Email: {self.results.get('email', 'Unknown')}</h2>
                <input type="text" class="search-box" placeholder="🔍 Поиск..." onkeyup="filterTable(this, 'email-table')">
                <table id="email-table">
                    <thead>
                        <tr>
                            <th>Сервис</th>
                            <th>Статус</th>
                            <th>Детали</th>
                        </tr>
                    </thead>
                    <tbody>
"""
            for r in self.results['email_results']:
                if r.get('exists'):
                    status = '<span class="found">✓ Найден</span>'
                elif r.get('error'):
                    status = '<span class="error">⚠ Ошибка</span>'
                else:
                    status = '<span class="not-found">✗ Не найден</span>'
                
                html += f"""
                        <tr>
                            <td>{r.get('service', '?')}</td>
                            <td>{status}</td>
                            <td>{r.get('details', '')}</td>
                        </tr>
"""
            html += """
                    </tbody>
                </table>
            </div>
"""
        
        # Username результаты
        if self.results["username_results"]:
            html += f"""
            <div class="section">
                <h2>👤 Username: {self.results.get('username', 'Unknown')}</h2>
                <input type="text" class="search-box" placeholder="🔍 Поиск..." onkeyup="filterTable(this, 'username-table')">
                <table id="username-table">
                    <thead>
                        <tr>
                            <th>Сервис</th>
                            <th>Статус</th>
                            <th>URL</th>
                            <th>Детали</th>
                        </tr>
                    </thead>
                    <tbody>
"""
            for r in self.results['username_results']:
                if r.get('exists'):
                    status = '<span class="found">✓ Найден</span>'
                    url = r.get('url', '')
                    url_html = f'<a href="{url}" target="_blank">{url}</a>' if url else ''
                else:
                    status = '<span class="not-found">✗ Не найден</span>'
                    url_html = ''
                
                tags_html = ' '.join([f'<span class="tag">{tag}</span>' for tag in r.get('tags', [])])
                
                html += f"""
                        <tr>
                            <td>{r.get('service', '?')}</td>
                            <td>{status}</td>
                            <td>{url_html}</td>
                            <td>{tags_html}</td>
                        </tr>
"""
            html += """
                    </tbody>
                </table>
            </div>
"""
        
        # EXIF результаты
        if self.results["exif_results"] and not self.results["exif_results"].get("error"):
            exif = self.results["exif_results"]
            html += f"""
            <div class="section">
                <h2>🖼️ EXIF Metadata: {exif.get('file', 'Unknown')}</h2>
"""
            
            if exif.get('gps'):
                gps = exif['gps']
                html += f"""
                <h3>📍 Геолокация</h3>
                <p>Координаты: {gps['latitude']}, {gps['longitude']}</p>
                <a href="{gps['maps_url']}" target="_blank">Открыть в Google Maps</a>
                <iframe class="gps-map" src="{gps['maps_url']}&output=embed"></iframe>
"""
            
            if exif.get('metadata'):
                html += """
                <h3>📷 Метаданные</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Категория</th>
                            <th>Тег</th>
                            <th>Значение</th>
                        </tr>
                    </thead>
                    <tbody>
"""
                for category, tags in exif['metadata'].items():
                    first = True
                    for tag_name, value in tags.items():
                        short_name = tag_name.split(' ', 1)[-1] if ' ' in tag_name else tag_name
                        cat_display = category if first else ''
                        html += f"""
                        <tr>
                            <td>{cat_display}</td>
                            <td>{short_name}</td>
                            <td>{value}</td>
                        </tr>
"""
                        first = False
                html += """
                    </tbody>
                </table>
"""
            html += """
            </div>
"""
        
        html += """
        </div>
    </div>
    <script>
        function filterTable(input, tableId) {
            const filter = input.value.toLowerCase();
            const table = document.getElementById(tableId);
            const rows = table.getElementsByTagName('tr');
            
            for (let i = 1; i < rows.length; i++) {
                const cells = rows[i].getElementsByTagName('td');
                let found = false;
                for (let cell of cells) {
                    if (cell.textContent.toLowerCase().includes(filter)) {
                        found = true;
                        break;
                    }
                }
                rows[i].style.display = found ? '' : 'none';
            }
        }
    </script>
</body>
</html>
"""
        
        return html
    
    def print_summary(self):
        """Вывести сводку в консоль."""
        print_stats(self.results["summary"])
