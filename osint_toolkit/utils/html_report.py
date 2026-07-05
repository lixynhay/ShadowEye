"""Генерация HTML-отчёта OSINT."""
from datetime import datetime
from html import escape


def generate_html_report(data: dict) -> str:
    """Создать HTML-отчёт из словаря результатов."""
    timestamp = data.get("timestamp", datetime.now().isoformat())

    css = """
    <style>
        :root { color-scheme: dark; }
        body { font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: linear-gradient(135deg, #0d1117, #161b22); color: #c9d1d9; margin: 0; padding: 24px; }
        h1 { color: #58a6ff; border-bottom: 2px solid #30363d; padding-bottom: 10px; }
        h2 { color: #79c0ff; margin-top: 30px; }
        h3 { color: #8b949e; }
        table { width: 100%; border-collapse: collapse; margin: 15px 0; background: #161b22; border: 1px solid #30363d; border-radius: 8px; overflow: hidden; }
        th { background: #21262d; color: #58a6ff; padding: 12px; text-align: left; font-weight: 600; }
        td { padding: 10px 12px; border-top: 1px solid #30363d; word-break: break-word; }
        tr:hover { background: #1f242c; }
        .found { color: #3fb950; font-weight: bold; }
        .notfound { color: #f85149; }
        .error { color: #d29922; }
        .badge { display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 12px; background: #21262d; margin-right: 4px; }
        .summary-box { display: flex; gap: 20px; flex-wrap: wrap; margin: 20px 0; }
        .summary-card { background: rgba(22, 27, 34, 0.95); border: 1px solid #30363d; border-radius: 10px; padding: 20px; min-width: 180px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.25); }
        .summary-card .value { font-size: 28px; font-weight: bold; color: #58a6ff; }
        .summary-card .label { font-size: 14px; color: #8b949e; margin-top: 5px; }
        .gps-box { background: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 15px; margin: 15px 0; }
        .muted { color: #8b949e; }
        a { color: #58a6ff; text-decoration: none; }
        a:hover { text-decoration: underline; }
        .footer { margin-top: 40px; text-align: center; color: #484f58; font-size: 12px; border-top: 1px solid #30363d; padding-top: 20px; }
    </style>
    """

    summary = data.get("summary", {})
    summary_html = ""
    if summary:
        cards = []
        for key, value in summary.items():
            label = key.replace("_", " ").title()
            cards.append(f"""
            <div class="summary-card">
                <div class="value">{value}</div>
                <div class="label">{label}</div>
            </div>
            """)
        summary_html = f'<div class="summary-box">{"".join(cards)}</div>'

    email_html = ""
    if data.get("email_results"):
        rows = ""
        for r in data["email_results"]:
            if r.get("exists"):
                status = '<span class="found">✓ Найден</span>'
            elif r.get("error"):
                status = '<span class="error">⚠ Ошибка</span>'
            else:
                status = '<span class="notfound">✗ Не найден</span>'
            rows += f"""
            <tr>
                <td>{escape(str(r.get('service', '?')))}</td>
                <td>{status}</td>
                <td>{escape(str(r.get('details', '')))}</td>
            </tr>
            """
        email_html = f"""
        <h2>📧 Email: {data.get("email", "Unknown")}</h2>
        <table>
            <tr><th>Сервис</th><th>Статус</th><th>Детали</th></tr>
            {rows}
        </table>
        """

    username_html = ""
    if data.get("username_results"):
        rows = ""
        for r in data["username_results"]:
            if r.get("exists"):
                status = '<span class="found">✓ Найден</span>'
                url = r.get("url", "")
                url_html = f'<a href="{escape(str(url), quote=True)}" target="_blank">{escape(str(url))}</a>' if url else ""
            else:
                status = '<span class="notfound">✗ Не найден</span>'
                url_html = ""
            tags = " ".join([f'<span class="badge">{escape(str(tag))}</span>' for tag in r.get("tags", [])])
            rows += f"""
            <tr>
                <td>{escape(str(r.get('service', '?')))}</td>
                <td>{status}</td>
                <td>{escape(str(r.get('details', '')))}{url_html}</td>
                <td>{tags}</td>
            </tr>
            """
        username_html = f"""
        <h2>👤 Username: {data.get("username", "Unknown")}</h2>
        <table>
            <tr><th>Сервис</th><th>Статус</th><th>URL</th><th>Теги</th></tr>
            {rows}
        </table>
        """

    exif_html = ""
    exif = data.get("exif_results")
    if exif and not exif.get("error"):
        gps_block = ""
        if exif.get("gps"):
            gps = exif["gps"]
            gps_block = f"""
            <div class="gps-box">
                <strong>📍 Геолокация</strong><br>
                Координаты: {gps.get("latitude")}, {gps.get("longitude")}<br>
                <a href="{gps.get("maps_url")}" target="_blank">Открыть в Google Maps</a>
            </div>
            """
        meta_rows = ""
        for category, tags in exif.get("metadata", {}).items():
            first = True
            for tag_name, value in tags.items():
                short_name = tag_name.split(" ", 1)[-1] if " " in tag_name else tag_name
                cat_display = category if first else ""
                meta_rows += f"<tr><td>{escape(str(cat_display))}</td><td>{escape(str(short_name))}</td><td>{escape(str(value))}</td></tr>"
                first = False
        exif_html = f"""
        <h2>🖼️ EXIF: {exif.get("file", "Unknown")}</h2>
        {gps_block}
        <table>
            <tr><th>Категория</th><th>Тег</th><th>Значение</th></tr>
            {meta_rows}
        </table>
        """

    phone_html = ""
    phone = data.get("phone_results")
    if phone and not phone.get("error"):
        phone_html = f"""
        <h2>📞 Phone: {phone.get("phone", "Unknown")}</h2>
        <table>
            <tr><th>Параметр</th><th>Значение</th></tr>
            <tr><td>Номер</td><td>{phone.get("international", "Н/Д")}</td></tr>
            <tr><td>Страна</td><td>{phone.get("country", "Н/Д")}</td></tr>
            <tr><td>Оператор</td><td>{phone.get("carrier", "Н/Д")}</td></tr>
            <tr><td>Тип линии</td><td>{phone.get("line_type", "Н/Д")}</td></tr>
            <tr><td>Валидный</td><td>{"✓ Да" if phone.get("is_valid") else "✗ Нет"}</td></tr>
        </table>
        """

    domain_html = ""
    domain = data.get("domain_results")
    if domain:
        whois_rows = ""
        whois = domain.get("whois", {})
        if whois and not whois.get("error"):
            for k, v in whois.items():
                if v:
                    whois_rows += f"<tr><td>{escape(str(k))}</td><td>{escape(str(v))}</td></tr>"
        dns_rows = ""
        dns = domain.get("dns", {})
        if dns and not dns.get("error"):
            for record_type, values in dns.items():
                if values:
                    dns_rows += f"<tr><td>{escape(str(record_type))}</td><td>{escape(', '.join(map(str, values)))}</td></tr>"
        ip_geo = domain.get("ip_geo", {})
        geo_rows = ""
        if ip_geo:
            for k, v in ip_geo.items():
                if v and k != "maps_url":
                    geo_rows += f"<tr><td>{escape(str(k))}</td><td>{escape(str(v))}</td></tr>"
        domain_html = f"""
        <h2>🌐 Domain: {domain.get("domain", "Unknown")}</h2>
        <h3>WHOIS</h3>
        <table><tr><th>Параметр</th><th>Значение</th></tr>{whois_rows}</table>
        <h3>DNS</h3>
        <table><tr><th>Тип</th><th>Значения</th></tr>{dns_rows}</table>
        <h3>IP Geolocation</h3>
        <table><tr><th>Параметр</th><th>Значение</th></tr>{geo_rows}</table>
        """

    html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ShadowEye OSINT Report</title>
    {css}
</head>
<body>
    <h1>🎯 ShadowEye OSINT Report</h1>
    <p class="muted">Generated: {escape(str(timestamp))}</p>
    {summary_html}
    {email_html}
    {username_html}
    {phone_html}
    {domain_html}
    {exif_html}
    <div class="footer">
        Generated by <a href="https://github.com/lixynhay/ShadowEye">ShadowEye</a>
    </div>
</body>
</html>"""
    return html
