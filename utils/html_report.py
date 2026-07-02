"""Генерация красивого HTML отчёта."""
import json
from datetime import datetime
from typing import Dict, Any, List

def generate_html_report(data: Dict[str, Any]) -> str:
    """Генерировать интерактивный HTML отчёт."""
    
    html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OSINT Report - {data.get('timestamp', 'Unknown')}</title>
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
            <p>Дата: {data.get('timestamp', 'Unknown')}</p>
        </div>
        <div class="content">
"""
    
    # Статистика
    summary = data.get('summary', {})
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
    if data.get('email_results'):
        html += f"""
            <div class="section">
                <h2>📧 Email: {data.get('email', 'Unknown')}</h2>
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
        for r in data['email_results']:
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
    if data.get('username_results'):
        html += f"""
            <div class="section">
                <h2>👤 Username: {data.get('username', 'Unknown')}</h2>
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
        for r in data['username_results']:
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
    if data.get('exif_results') and not data['exif_results'].get('error'):
        exif = data['exif_results']
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
