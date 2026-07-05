import re
from typing import Optional


def _normalize_input(value: Optional[str]) -> Optional[str]:
    if not isinstance(value, str):
        return None
    cleaned = value.strip()
    return cleaned or None


def validate_email(email: str) -> bool:
    normalized = _normalize_input(email)
    if not normalized:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.fullmatch(pattern, normalized))


def validate_username(username: str) -> bool:
    normalized = _normalize_input(username)
    if not normalized:
        return False
    pattern = r'^[a-zA-Z0-9_\-\.]{1,39}$'
    return bool(re.fullmatch(pattern, normalized))


def validate_domain(domain: str) -> bool:
    normalized = _normalize_input(domain)
    if not normalized:
        return False
    pattern = r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    return bool(re.fullmatch(pattern, normalized.lower()))


def validate_phone(phone: str) -> bool:
    normalized = _normalize_input(phone)
    if not normalized:
        return False
    pattern = r'^\+?[1-9]\d{1,14}$'
    return bool(re.fullmatch(pattern, normalized))


def validate_proxy(proxy: str) -> bool:
    normalized = _normalize_input(proxy)
    if not normalized:
        return False
    pattern = r'^(https?|socks5)://(?:[a-zA-Z0-9.-]+|\[[0-9a-fA-F:]+\]):\d{1,5}$'
    if not re.fullmatch(pattern, normalized):
        return False
    return 1 <= int(normalized.rsplit(':', 1)[1]) <= 65535