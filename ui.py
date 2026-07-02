"""UI компоненты с использованием Rich library."""
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.prompt import Prompt, IntPrompt
from rich import box

console = Console()

def print_banner():
    banner = """
[bold cyan]
  ██████╗ ███████╗███╗   ██╗ ██████╗ ████████╗███████╗██╗████████╗
 ██╔═══██╗██╔════╝████╗  ██║██╔═══██╗╚══██╔══╝██╔════╝██║╚══██╔══╝
 ██║   ██║███████╗██╔██╗ ██║██║   ██║   ██║   █████╗  ██║   ██║   
 ██║   ██║╚════██║██║╚██╗██║██║   ██║   ██║   ██╔══╝  ██║   ██║   
 ╚██████╔╝███████║██║ ╚████║╚██████╔╝   ██║   ██║     ██║   ██║   
  ╚═════╝ ╚══════╝╚═╝  ╚═══╝ ╚═════╝    ╚═╝   ╚═╝     ╚═╝   ╚═╝   
[/bold cyan]
[bold yellow]        OSINT Toolkit Pro v2.0 — Multi-Tool Framework[/bold yellow]
[bold magenta]        by Dima | Email + Username + EXIF Analysis[/bold magenta]
"""
    console.print(banner)

def print_menu():
    menu_items = [
        "[bold green]1.[/bold green] 📧 Email OSINT (Holehe) — проверка регистрации email",
        "[bold green]2.[/bold green] 👤 Username OSINT (Maigret) — поиск по никнейму",
        "[bold green]3.[/bold green] 🖼️  Image EXIF — анализ метаданных изображений",
        "[bold green]4.[/bold green] 🎯 All-in-One — комбинированный анализ",
        "[bold green]5.[/bold green] 📦 Batch Mode — пакетная обработка",
        "[bold red]0.[/bold red]  🚪 Выход",
    ]
    console.print(Panel("\n".join(menu_items), title="[bold cyan]🎯 Выберите режим работы[/bold cyan]", border_style="cyan", box=box.ROUNDED))

def get_menu_choice() -> int:
    try:
        return IntPrompt.ask("[bold yellow]Ваш выбор[/bold yellow]", default=0)
    except Exception:
        return -1

def create_results_table(title: str, results: list) -> Table:
    table = Table(title=f"[bold]{title}[/bold]", box=box.ROUNDED, show_header=True, header_style="bold cyan")
    table.add_column("Сервис", style="cyan", width=25)
    table.add_column("Статус", style="magenta", width=12)
    table.add_column("Детали", style="white")
    for r in results:
        status = "[bold green]✓ Найден[/bold green]" if r.get("exists") else "[red]✗ Не найден[/red]"
        if r.get("error"):
            status = "[yellow]⚠ Ошибка[/yellow]"
        details = r.get("details", "") or ""
        table.add_row(r.get("service", "?"), status, details)
    return table

def create_exif_table(exif_data: dict) -> Table:
    """Создать таблицу EXIF данных по категориям."""
    table = Table(
        title="[bold]📷 EXIF Metadata[/bold]",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta"
    )
    table.add_column("Категория", style="cyan", width=20)
    table.add_column("Тег", style="white", width=30)
    table.add_column("Значение", style="green")
    
    for category, tags in exif_data.items():
        first = True
        for tag_name, value in tags.items():
            # Убираем префикс категории из имени тега
            short_name = tag_name.split(' ', 1)[-1] if ' ' in tag_name else tag_name
            cat_display = category if first else ""
            table.add_row(cat_display, short_name, str(value))
            first = False
    
    return table

def create_progress():
    return Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(), TextColumn("[progress.percentage]{task.percentage:>3.0f}%"), console=console)

def print_success(message: str):
    console.print(f"[bold green]✓[/bold green] {message}")

def print_error(message: str):
    console.print(f"[bold red]✗[/bold red] {message}")

def print_warning(message: str):
    console.print(f"[bold yellow]⚠[/bold yellow] {message}")

def print_info(message: str):
    console.print(f"[bold cyan]ℹ[/bold cyan] {message}")

def print_stats(stats: dict):
    stats_text = "\n".join([f"[cyan]{k}:[/cyan] [bold white]{v}[/bold white]" for k, v in stats.items()])
    console.print(Panel(stats_text, title="[bold]📊 Статистика[/bold]", border_style="green"))
