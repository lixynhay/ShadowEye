"""Валидация входных данных OSINT."""
import re


def validate_email(email: str) -> bool:
    """Проверить формат email."""
    if not email or len(email) > 254:
        return False
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_username(username: str) -> bool:
    """Проверить безопасность username (без shell-метасимволов)."""
    if not username or len(username) > 64:
        return False
    if re.search(r'[;|&$`\\"\n\r]', username):
        return False
    return bool(re.match(r"^[a-zA-Z0-9_.-]+$", username))


def validate_domain(domain: str) -> bool:
    """Проверить формат домена."""
    if not domain or len(domain) > 253:
        return False
    domain = re.sub(r"^https?://", "", domain)
    domain = domain.split("/")[0]
    pattern = r"^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
    return bool(re.match(pattern, domain))


def validate_phone(phone: str) -> bool:
    """Базовая проверка телефона (начинается с + и цифры)."""
    if not phone:
        return False
    cleaned = re.sub(r"[\s\-\(\)\.]", "", phone)
    return bool(re.match(r"^\+\d{7,15}$", cleaned))


def validate_proxy(proxy: str) -> bool:
    """Проверить формат прокси."""
    if not proxy:
        return False
    return bool(re.match(r"^(http|https|socks4|socks5)://", proxy))
