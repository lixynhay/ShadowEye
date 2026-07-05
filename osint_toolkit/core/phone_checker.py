"""Анализ телефонных номеров через phonenumbers (Google libphonenumber)."""
from typing import Dict, Any
from ..ui import console

class PhoneChecker:
    def __init__(self):
        self._available = False
        self._check_phonenumbers()
    
    def _check_phonenumbers(self):
        try:
            import phonenumbers
            self._available = True
            console.print(f"[green]✓ Phonenumbers (Google libphonenumber) установлен[/green]")
        except ImportError:
            console.print("[yellow]⚠ Phonenumbers не установлен. pip install phonenumbers[/yellow]")
            self._available = False
    
    def is_available(self) -> bool:
        return self._available
    
    def check(self, phone: str) -> Dict[str, Any]:
        """Проверить телефон."""
        if not self._available:
            return {"error": "Phonenumbers not installed"}
        
        try:
            import phonenumbers
            from phonenumbers import carrier, geocoder, timezone

            normalized_phone = phone.strip()
            if not normalized_phone:
                return {"error": "Пустой номер телефона", "phone": phone}
            
            # Парсим номер
            parsed = phonenumbers.parse(normalized_phone, None)
            
            # Проверяем валидность
            if not phonenumbers.is_valid_number(parsed):
                return {
                    "error": "Неверный номер телефона",
                    "phone": phone
                }
            
            result = {
                "phone": normalized_phone,
                "international": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                "national": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL),
                "country_code": parsed.country_code,
                "country": geocoder.description_for_number(parsed, "ru"),
                "carrier": carrier.name_for_number(parsed, "ru"),
                "line_type": self._get_line_type(parsed),
                "timezones": timezone.time_zones_for_number(parsed),
                "is_valid": True,
                "is_possible": phonenumbers.is_possible_number(parsed)
            }
            
            return result
        
        except phonenumbers.NumberParseException as e:
            return {"error": f"Ошибка парсинга: {e}", "phone": phone}
        except (TimeoutError, ConnectionError, OSError) as e:
            return {"error": f"Ошибка сети: {e}", "phone": phone}
        except Exception as e:
            return {"error": str(e), "phone": phone}
    
    def _get_line_type(self, parsed) -> str:
        """Определить тип линии."""
        import phonenumbers
        line_type = phonenumbers.number_type(parsed)
        
        types = {
            phonenumbers.PhoneNumberType.FIXED_LINE: "Стационарный",
            phonenumbers.PhoneNumberType.MOBILE: "Мобильный",
            phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Стационарный/Мобильный",
            phonenumbers.PhoneNumberType.TOLL_FREE: "Бесплатный",
            phonenumbers.PhoneNumberType.PREMIUM_RATE: "Платный",
            phonenumbers.PhoneNumberType.SHARED_COST: "Разделённая стоимость",
            phonenumbers.PhoneNumberType.VOIP: "VoIP",
            phonenumbers.PhoneNumberType.PERSONAL_NUMBER: "Персональный",
            phonenumbers.PhoneNumberType.PAGER: "Пейджер",
            phonenumbers.PhoneNumberType.UAN: "UAN",
            phonenumbers.PhoneNumberType.VOICEMAIL: "Голосовая почта",
            phonenumbers.PhoneNumberType.UNKNOWN: "Неизвестный"
        }
        
        return types.get(line_type, "Неизвестный")
    
    def run(self, phone: str) -> Dict[str, Any]:
        return self.check(phone)
