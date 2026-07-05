import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.prompt import Prompt, IntPrompt
from rich import box

console = Console(highlight=False, soft_wrap=True)


def get_terminal_theme() -> str:
    """Return a simple theme hint for better readability on different platforms."""
    if os.environ.get("TERMUX_VERSION"):
        return "termux"
    if sys.platform.startswith("win"):
        return "windows"
    return "unix"


def get_banner_title() -> str:
    theme = get_terminal_theme()
    if theme == "termux":
        return "ShadowEye [bold cyan]Termux[/bold cyan]"
    if theme == "windows":
        return "ShadowEye [bold cyan]Windows[/bold cyan]"
    return "ShadowEye [bold cyan]Linux[/bold cyan]"

def print_banner():
    banner = f"""
[bold cyan]
  ███████╗██╗   ██╗███████╗████████╗███████╗███╗   ███╗
  ██╔════╝██║   ██║██╔════╝╚══██╔══╝██╔════╝████╗ ████║
  ███████╗██║   ██║███████╗   ██║   █████╗  ██╔██████║
  ╚════██║██║   ██║╚════██║   ██║   ██╔══╝  ██║╚██╔╝██║
  ███████║╚██████╔╝███████║   ██║   ███████╗██║ ╚═╝ ██║
  ╚══════╝ ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚═╝
[/bold cyan]
[bold yellow]        ShadowEye v3.1 — Multi-Tool OSINT Framework[/bold yellow]
[bold magenta]        by lixynhay[/bold magenta]
[dim]        Platform: {get_terminal_theme().title()}[/dim]
"""
    console.print(banner)

def print_menu():
    menu_items = [
        "[bold green]1.[/bold green] 📧 Email OSINT (Holehe) — проверка регистрации email",
        "[bold green]2.[/bold green] 👤 Username OSINT (Maigret/Sherlock) — поиск по никнейму",
        "[bold green]3.[/bold green] 📞 Phone OSINT — анализ телефона",
        "[bold green]4.[/bold green] 🌐 Domain OSINT — WHOIS, DNS, IP",
        "[bold green]5.[/bold green] 🖼️ Image EXIF — анализ метаданных",
        "[bold green]6.[/bold green] 🎯 All-in-One — комбинированный анализ",
        "[bold green]7.[/bold green] 📦 Batch Mode — пакетная обработка",
        "[bold green]8.[/bold green] 🔧 Настройка прокси",
        "[bold red]0.[/bold red]  🚪 Выход",
    ]
    console.print(Panel("\n".join(menu_items), title=f"[bold cyan]🎯 {get_banner_title()}[/bold cyan]", border_style="cyan", box=box.ROUNDED))

def get_menu_choice() -> int:
    try:
        return IntPrompt.ask("[bold yellow]Ваш выбор[/bold yellow]", default=0)
    except Exception:
        return -1

def create_results_table(title: str, results: list) -> Table:
    table = Table(title=f"[bold]{title}[/bold]", box=box.ROUNDED, show_header=True, header_style="bold cyan")
    table.add_column("Сервис", style="cyan", width=24)
    table.add_column("Статус", style="magenta", width=14)
    table.add_column("Детали", style="white", overflow="fold")
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
            short_name = tag_name.split(' ', 1)[-1] if ' ' in tag_name else tag_name
            cat_display = category if first else ""
            table.add_row(cat_display, short_name, str(value))
            first = False
    return table

def create_progress():
    return Progress(
        SpinnerColumn(style="green"),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=None),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
        transient=False,
    )

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