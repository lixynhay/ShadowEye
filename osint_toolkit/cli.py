import os
import sys
import asyncio

if sys.platform == 'win32':
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    except AttributeError:
        pass

from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table
from rich import box
from .ui import console, print_banner, print_menu, get_menu_choice, create_results_table, create_exif_table, print_success, print_error, print_warning, print_info
from .core.email_checker import EmailChecker
from .core.username_checker import UsernameChecker
from .core.exif_analyzer import ExifAnalyzer
from .core.phone_checker import PhoneChecker
from .core.domain_checker import DomainChecker
from .aggregator import Aggregator
from .utils.proxy_rotator import ProxyRotator
from .utils.validators import validate_email, validate_username, validate_domain, validate_phone, validate_proxy


class OSINTToolkit:
    def __init__(self):
        self.email_checker = EmailChecker()
        self.username_checker = UsernameChecker()
        self.exif_analyzer = ExifAnalyzer()
        self.phone_checker = PhoneChecker()
        self.domain_checker = DomainChecker()
        self.aggregator = Aggregator()
        self.proxy_rotator = ProxyRotator()

    def run(self):
        print_banner()
        while True:
            self._print_menu_with_proxy()
            choice = get_menu_choice()
            if choice == 1:
                self._email_mode()
            elif choice == 2:
                self._username_mode()
            elif choice == 3:
                self._phone_mode()
            elif choice == 4:
                self._domain_mode()
            elif choice == 5:
                self._exif_mode()
            elif choice == 6:
                self._all_in_one_mode()
            elif choice == 7:
                self._batch_mode()
            elif choice == 8:
                self._proxy_mode()
            elif choice == 0:
                print_success("До свидания! 👋")
                break
            else:
                print_error("Неверный выбор. Попробуйте снова.")
            console.print("\n")

    def _print_menu_with_proxy(self):
        proxy_status = ""
        if self.proxy_rotator.has_proxies():
            proxy_status = "[bold green] Прокси активны[/bold green]"
        else:
            proxy_status = "[yellow]️  Прокси не настроены[/yellow]"
        console.print(f"[dim]{proxy_status}[/dim]\n")
        menu_items = [
            "[bold green]1.[/bold green] 📧 Email OSINT (Holehe) — проверка регистрации email",
            "[bold green]2.[/bold green] 👤 Username OSINT (Maigret/Sherlock) — поиск по никнейму",
            "[bold green]3.[/bold green] 📞 Phone OSINT — анализ телефона",
            "[bold green]4.[/bold green] 🌐 Domain OSINT — WHOIS, DNS, IP",
            "[bold green]5.[/bold green] 🖼️ Image EXIF — анализ метаданных",
            "[bold green]6.[/bold green]  All-in-One — комбинированный анализ",
            "[bold green]7.[/bold green] 📦 Batch Mode — пакетная обработка",
            "[bold green]8.[/bold green] 🔧 Настройка прокси",
            "[bold red]0.[/bold red]  🚪 Выход",
        ]
        console.print(Panel("\n".join(menu_items), title="[bold cyan] ShadowEye v3.1[/bold cyan]", border_style="cyan", box=box.ROUNDED))

    def _email_mode(self):
        console.print(Panel("[bold cyan]📧 Email OSINT Mode[/bold cyan]\nПроверка регистрации email через Holehe (120+ сервисов)", border_style="cyan"))
        if not self.email_checker.is_available():
            print_error("Holehe не установлен!")
            print_info("Установите: pip install holehe")
            return
        email = Prompt.ask("[bold yellow]Введите email[/bold yellow]")
        if not validate_email(email):
            print_error("Неверный email")
            return
        cached = self.aggregator.get_cached_email(email)
        if cached:
            console.print("[green]✓ Результаты найдены в кэше![/green]")
            use_cache = Prompt.ask("[bold yellow]Использовать кэшированные результаты? (y/n)[/bold yellow]", default="y")
            if use_cache.lower() == 'y':
                found = [r for r in cached if r.get("exists")]
                if found:
                    table = create_results_table(f"Найдено в {len(found)} сервисах (ИЗ КЭША)", found)
                    console.print(table)
                return
        console.print("[cyan]Режим отображения:[/cyan]")
        console.print("[green]1.[/green] Только найденные (рекомендуется)")
        console.print("[green]2.[/green] Все результаты (включая rate limit)")
        mode = Prompt.ask("[bold yellow]Выбери режим[/bold yellow]", default="1")
        show_all = mode == "2"
        print_info(f"Проверяем email: {email}")
        results = self.email_checker.run(email, show_all=show_all)
        found = [r for r in results if r.get("exists")]
        if found:
            table = create_results_table(f"Найдено в {len(found)} сервисах", found)
            console.print(table)
        else:
            print_warning("Email не найден ни в одном сервисе")
        self.aggregator.add_email_results(email, results)
        self._ask_export()

    def _username_mode(self):
        console.print(Panel("[bold magenta]👤 Username OSINT Mode[/bold magenta]\nПоиск аккаунтов по username", border_style="magenta"))
        if not self.username_checker.is_available():
            print_error("Ни Maigret, ни Sherlock не установлены!")
            return
        username = Prompt.ask("[bold yellow]Введите username[/bold yellow]")
        if not validate_username(username):
            print_error("Неверный username. Разрешены: a-z, 0-9, _, ., -")
            return
        cached = self.aggregator.get_cached_username(username)
        if cached:
            console.print("[green]✓ Результаты найдены в кэше![/green]")
            use_cache = Prompt.ask("[bold yellow]Использовать кэшированные результаты? (y/n)[/bold yellow]", default="y")
            if use_cache.lower() == 'y':
                found = [r for r in cached if r.get("exists")]
                if found:
                    table = create_results_table(f"Найдено аккаунтов: {len(found)} (ИЗ КЭША)", found)
                    console.print(table)
                return
        print_info(f"Sherlock ищет: {username}")
        results = self.username_checker.run(username)
        found = [r for r in results if r.get("exists")]
        if found:
            table = create_results_table(f"Найдено аккаунтов: {len(found)}", found)
            console.print(table)
        else:
            print_warning("Ничего не найдено")
        self.aggregator.add_username_results(username, results)
        self._ask_export()

    def _phone_mode(self):
        console.print(Panel("[bold blue]📞 Phone OSINT Mode[/bold blue]\nАнализ телефонных номеров", border_style="blue"))
        if not self.phone_checker.is_available():
            print_error("Phonenumbers не установлен!")
            print_info("Установите: pip install phonenumbers")
            return
        phone = Prompt.ask("[bold yellow]Введите номер телефона (с кодом страны)[/bold yellow]", default="+7")
        if not validate_phone(phone):
            print_error("Неверный формат телефона. Пример: +79001234567")
            return
        print_info(f"Анализируем номер: {phone}")
        result = self.phone_checker.run(phone)
        if not result.get("error"):
            table = Table(title="📊 Результаты анализа", box=box.ROUNDED)
            table.add_column("Параметр", style="cyan")
            table.add_column("Значение", style="white")
            table.add_row("Номер", result.get('international', phone))
            table.add_row("Страна", result.get('country', 'Н/Д'))
            table.add_row("Оператор", result.get('carrier', 'Н/Д'))
            table.add_row("Тип линии", result.get('line_type', 'Н/Д'))
            table.add_row("Часовые пояса", ', '.join(result.get('timezones', [])))
            table.add_row("Валидный", "✓ Да" if result.get('is_valid') else "✗ Нет")
            console.print(table)
            self.aggregator.add_phone_results(phone, result)
        else:
            print_error(f"Ошибка: {result.get('error')}")
        self._ask_export()

    def _domain_mode(self):
        console.print(Panel("[bold green]🌐 Domain OSINT Mode[/bold green]\nWHOIS, DNS, IP Geolocation", border_style="green"))
        if not self.domain_checker.is_available():
            print_error("Зависимости не установлены!")
            print_info("Установите: pip install python-whois dnspython")
            return
        domain = Prompt.ask("[bold yellow]Введите домен[/bold yellow]")
        if not validate_domain(domain):
            print_error("Неверный домен")
            return
        print_info(f"Анализируем домен: {domain}")
        result = self.domain_checker.run(domain)
        if result.get("whois") and not result["whois"].get("error"):
            whois = result["whois"]
            table = Table(title="📋 WHOIS информация", box=box.ROUNDED)
            table.add_column("Параметр", style="cyan")
            table.add_column("Значение", style="white")
            if whois.get("registrar"):
                table.add_row("Регистратор", whois["registrar"])
            if whois.get("creation_date"):
                table.add_row("Дата создания", whois["creation_date"])
            if whois.get("expiration_date"):
                table.add_row("Дата истечения", whois["expiration_date"])
            if whois.get("country"):
                table.add_row("Страна", whois["country"])
            if whois.get("org"):
                table.add_row("Организация", whois["org"])
            if whois.get("name_servers"):
                table.add_row("DNS серверы", ', '.join(whois["name_servers"]))
            if whois.get("emails"):
                table.add_row("Email контакты", ', '.join(whois["emails"]))
            console.print(table)
        if result.get("dns") and not result["dns"].get("error"):
            dns = result["dns"]
            table = Table(title="🔍 DNS записи", box=box.ROUNDED)
            table.add_column("Тип", style="cyan")
            table.add_column("Значения", style="white")
            for record_type, values in dns.items():
                if values:
                    table.add_row(record_type, ', '.join(values))
            console.print(table)
        if result.get("ip"):
            console.print(f"[green]✓ IP адрес:[/green] {result['ip']}")
        if result.get("ip_geo"):
            geo = result["ip_geo"]
            table = Table(title="📍 IP Geolocation", box=box.ROUNDED)
            table.add_column("Параметр", style="cyan")
            table.add_column("Значение", style="white")
            if geo.get("country"):
                table.add_row("Страна", geo["country"])
            if geo.get("city"):
                table.add_row("Город", geo["city"])
            if geo.get("isp"):
                table.add_row("Провайдер", geo["isp"])
            if geo.get("org"):
                table.add_row("Организация", geo["org"])
            if geo.get("timezone"):
                table.add_row("Часовой пояс", geo["timezone"])
            if geo.get("maps_url"):
                table.add_row("Карта", geo["maps_url"])
            console.print(table)
        self.aggregator.add_domain_results(domain, result)
        self._ask_export()

    def _exif_mode(self):
        console.print(Panel("[bold green]️ EXIF Analyzer Mode[/bold green]\nАнализ метаданных изображений", border_style="green"))
        if not self.exif_analyzer.is_available():
            print_error("ExifRead не установлен!")
            print_info("Установите: pip install exifread")
            return
        path_input = Prompt.ask("[bold yellow]Путь к файлу или директории[/bold yellow]")
        path = os.path.expanduser(path_input)
        console.print(f"[cyan]ℹ Путь:[/cyan] {path}")
        if os.path.isdir(path):
            results = self.exif_analyzer.analyze_directory(path)
            for r in results:
                if not r.get("error"):
                    console.print(create_exif_table(r.get("metadata", {})))
                    if r.get("gps"):
                        print_success(f"GPS: {r['gps']['maps_url']}")
        elif os.path.isfile(path):
            result = self.exif_analyzer.analyze(path)
            if not result.get("error"):
                console.print(create_exif_table(result.get("metadata", {})))
                if result.get("gps"):
                    print_success(f"📍 GPS: {result['gps']['maps_url']}")
                    print_info(f"Координаты: {result['gps']['latitude']}, {result['gps']['longitude']}")
                self.aggregator.add_exif_results(path, result)
            else:
                print_error(f"Ошибка: {result.get('error')}")
        else:
            print_error(f"Путь не найден: {path}")
        self._ask_export()

    def _all_in_one_mode(self):
        console.print(Panel("[bold yellow]🎯 All-in-One Mode[/bold yellow]\nКомплексный анализ", border_style="yellow"))
        print_info("Укажите данные для анализа (оставьте пустым, чтобы пропустить)")
        email = Prompt.ask("[cyan]Email[/cyan]", default="")
        username = Prompt.ask("[cyan]Username[/cyan]", default="")
        phone = Prompt.ask("[cyan]Телефон[/cyan]", default="")
        domain = Prompt.ask("[cyan]Домен[/cyan]", default="")
        image_input = Prompt.ask("[cyan]Путь к изображению[/cyan]", default="")
        image = os.path.expanduser(image_input) if image_input else ""
        if email and validate_email(email) and self.email_checker.is_available():
            print_info(f"Проверяем email: {email}")
            results = self.email_checker.run(email, show_all=False)
            found = [r for r in results if r.get("exists")]
            if found:
                table = create_results_table(f"Email: {email} ({len(found)} найдено)", found)
                console.print(table)
            self.aggregator.add_email_results(email, results)
        elif email and not validate_email(email):
            print_error("Неверный email, пропускаем")
        if username and validate_username(username) and self.username_checker.is_available():
            print_info(f"Ищем username: {username}")
            results = self.username_checker.run(username, use_sherlock=True)
            found = [r for r in results if r.get("exists")]
            if found:
                table = create_results_table(f"Username: {username}", found)
                console.print(table)
            self.aggregator.add_username_results(username, results)
        elif username and not validate_username(username):
            print_error("Неверный username, пропускаем")
        if phone and validate_phone(phone) and self.phone_checker.is_available():
            print_info(f"Анализируем телефон: {phone}")
            result = self.phone_checker.run(phone)
            if not result.get("error"):
                console.print(f"[green]✓ Страна:[/green] {result.get('country', 'Н/Д')}")
                console.print(f"[green]✓ Оператор:[/green] {result.get('carrier', 'Н/Д')}")
                self.aggregator.add_phone_results(phone, result)
        elif phone and not validate_phone(phone):
            print_error("Неверный телефон, пропускаем")
        if domain and validate_domain(domain) and self.domain_checker.is_available():
            print_info(f"Анализируем домен: {domain}")
            result = self.domain_checker.run(domain)
            if result.get("ip"):
                console.print(f"[green]✓ IP:[/green] {result['ip']}")
            if result.get("ip_geo") and result["ip_geo"].get("country"):
                console.print(f"[green]✓ Страна:[/green] {result['ip_geo']['country']}")
            self.aggregator.add_domain_results(domain, result)
        elif domain and not validate_domain(domain):
            print_error("Неверный домен, пропускаем")
        if image and os.path.isfile(image) and self.exif_analyzer.is_available():
            print_info(f"Анализируем: {image}")
            result = self.exif_analyzer.analyze(image)
            if not result.get("error"):
                if result.get("gps"):
                    print_success(f"📍 GPS: {result['gps']['maps_url']}")
                console.print(create_exif_table(result.get("metadata", {})))
                self.aggregator.add_exif_results(image, result)
        self.aggregator.print_summary()
        self._ask_export()

    def _batch_mode(self):
        console.print(Panel("[bold blue] Batch Mode[/bold blue]\nПакетная обработка из файла", border_style="blue"))
        print_info("Формат файла: каждая строка - один запрос")
        print_info("Префиксы: email:user@mail.com | username:nick | phone:+7... | domain:example.com | image:path.jpg")
        filepath_input = Prompt.ask("[bold yellow]Путь к файлу[/bold yellow]")
        filepath = os.path.expanduser(filepath_input)
        if not os.path.isfile(filepath):
            print_error(f"Файл не найден: {filepath}")
            return
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = [l.strip() for l in f if l.strip()]
        for line in lines:
            if ':' in line:
                mode, value = line.split(':', 1)
                mode = mode.lower().strip()
                value = value.strip()
                if mode == "email" and validate_email(value) and self.email_checker.is_available():
                    print_info(f"Email: {value}")
                    results = self.email_checker.run(value, show_all=False)
                    self.aggregator.add_email_results(value, results)
                elif mode == "username" and validate_username(value) and self.username_checker.is_available():
                    print_info(f"Username: {value}")
                    results = self.username_checker.run(value, use_sherlock=True)
                    self.aggregator.add_username_results(value, results)
                elif mode == "phone" and validate_phone(value) and self.phone_checker.is_available():
                    print_info(f"Phone: {value}")
                    result = self.phone_checker.run(value)
                    self.aggregator.add_phone_results(value, result)
                elif mode == "domain" and validate_domain(value) and self.domain_checker.is_available():
                    print_info(f"Domain: {value}")
                    result = self.domain_checker.run(value)
                    self.aggregator.add_domain_results(value, result)
                elif mode == "image" and self.exif_analyzer.is_available():
                    image_path = os.path.expanduser(value)
                    print_info(f"Image: {image_path}")
                    result = self.exif_analyzer.analyze(image_path)
                    self.aggregator.add_exif_results(image_path, result)
                else:
                    print_warning(f"Пропущена строка (неверный формат/валидация): {line}")
        self.aggregator.print_summary()
        self._ask_export()

    def _proxy_mode(self):
        console.print(Panel("[bold cyan]🔧 Настройка прокси[/bold cyan]\nУправление прокси-серверами", border_style="cyan"))
        proxy_file = os.path.expanduser("~/.osint_proxies.txt")
        console.print(f"[cyan]📁 Файл прокси:[/cyan] {proxy_file}")
        if self.proxy_rotator.has_proxies():
            console.print(f"[green]✓ Загружено прокси:[/green] {len(self.proxy_rotator.proxies)}")
            console.print("[cyan]Список прокси:[/cyan]")
            for i, proxy in enumerate(self.proxy_rotator.proxies, 1):
                console.print(f"  {i}. {proxy}")
        else:
            console.print("[yellow]⚠️  Прокси не найдены[/yellow]")
        console.print("\n[cyan]Действия:[/cyan]")
        console.print("[green]1.[/green] Добавить прокси")
        console.print("[green]2.[/green] Удалить все прокси")
        console.print("[green]3.[/green] Открыть файл в редакторе")
        console.print("[green]0.[/green] Назад в меню")
        choice = Prompt.ask("[bold yellow]Выберите действие[/bold yellow]", default="0")
        if choice == "1":
            proxy = Prompt.ask("[bold yellow]Введите прокси (формат: http://ip:port или socks5://ip:port)[/bold yellow]")
            if not validate_proxy(proxy):
                print_error("Неверный формат прокси. Пример: http://1.2.3.4:8080 или socks5://1.2.3.4:1080")
                return
            self.proxy_rotator.add_proxy(proxy)
            try:
                with open(proxy_file, 'a') as f:
                    f.write(proxy + "\n")
                print_success(f"Прокси {proxy} добавлен!")
            except Exception as e:
                print_error(f"Ошибка сохранения: {e}")
        elif choice == "2":
            confirm = Prompt.ask("[bold yellow]Удалить все прокси? (y/n)[/bold yellow]", default="n")
            if confirm.lower() == 'y':
                try:
                    os.remove(proxy_file)
                    self.proxy_rotator.proxies = []
                    print_success("Все прокси удалены!")
                except Exception as e:
                    print_error(f"Ошибка: {e}")
        elif choice == "3":
            print_info(f"Откройте файл {proxy_file} в любом редакторе")
            print_info("Каждый прокси с новой строки")

    def _ask_export(self):
        export = Prompt.ask("[bold yellow]Экспортировать результаты? (json/html/no)[/bold yellow]", default="no")
        if export.lower() in ["json", "yes", "y"]:
            filename = Prompt.ask("Имя файла", default="osint_report.json")
            self.aggregator.export_json(filename)
        elif export.lower() == "html":
            filename = Prompt.ask("Имя файла", default="osint_report.html")
            self.aggregator.export_html(filename)


def main():
    toolkit = OSINTToolkit()
    toolkit.run()


if __name__ == "__main__":
    main()