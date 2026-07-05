import asyncio
import json
import socket
from typing import Dict, Any, List
from ..ui import console, create_progress

class DomainChecker:
    def __init__(self):
        self._whois_available = False
        self._dns_available = False
        self._check_tools()
    
    def _check_tools(self):
        try:
            import whois
            self._whois_available = True
        except ImportError:
            console.print("[yellow]⚠ python-whois не установлен. pip install python-whois[/yellow]")
        
        try:
            import dns.resolver
            self._dns_available = True
        except ImportError:
            console.print("[yellow]⚠ dnspython не установлен. pip install dnspython[/yellow]")
    
    def is_available(self) -> bool:
        return self._whois_available or self._dns_available
    
    def check(self, domain: str) -> Dict[str, Any]:
        """Проверить домен."""
        normalized_domain = domain.strip().lower() if isinstance(domain, str) else ""
        result = {
            "domain": normalized_domain,
            "whois": None,
            "dns": {},
            "ip": None,
            "ip_geo": None
        }
        
        # WHOIS
        if self._whois_available and normalized_domain:
            result["whois"] = self._get_whois(normalized_domain)
        
        # DNS
        if self._dns_available and normalized_domain:
            result["dns"] = self._get_dns(normalized_domain)
        
        # IP и геолокация
        ip = self._get_ip(normalized_domain) if normalized_domain else None
        if ip:
            result["ip"] = ip
            result["ip_geo"] = self._get_ip_geo(ip)
        
        return result
    
    def _get_whois(self, domain: str) -> Dict[str, Any]:
        """Получить WHOIS информацию."""
        try:
            import whois
            w = whois.whois(domain)
            
            return {
                "registrar": w.registrar,
                "creation_date": str(w.creation_date) if w.creation_date else None,
                "expiration_date": str(w.expiration_date) if w.expiration_date else None,
                "updated_date": str(w.updated_date) if w.updated_date else None,
                "name_servers": w.name_servers if isinstance(w.name_servers, list) else [w.name_servers],
                "status": w.status if isinstance(w.status, list) else [w.status],
                "country": w.country,
                "state": w.state,
                "city": w.city,
                "org": w.org,
                "emails": w.emails if isinstance(w.emails, list) else [w.emails] if w.emails else []
            }
        except (TimeoutError, ConnectionError, OSError) as e:
            return {"error": f"Ошибка сети: {e}"}
        except Exception as e:
            return {"error": str(e)}
    
    def _get_dns(self, domain: str) -> Dict[str, List[str]]:
        """Получить DNS записи."""
        try:
            import dns.resolver
            
            records = {}
            
            # A записи
            try:
                answers = dns.resolver.resolve(domain, 'A')
                records['A'] = [str(rdata) for rdata in answers]
            except:
                records['A'] = []
            
            # MX записи
            try:
                answers = dns.resolver.resolve(domain, 'MX')
                records['MX'] = [str(rdata.exchange) for rdata in answers]
            except:
                records['MX'] = []
            
            # TXT записи
            try:
                answers = dns.resolver.resolve(domain, 'TXT')
                records['TXT'] = [str(rdata) for rdata in answers]
            except:
                records['TXT'] = []
            
            # CNAME записи
            try:
                answers = dns.resolver.resolve(domain, 'CNAME')
                records['CNAME'] = [str(rdata.target) for rdata in answers]
            except:
                records['CNAME'] = []
            
            # NS записи
            try:
                answers = dns.resolver.resolve(domain, 'NS')
                records['NS'] = [str(rdata.target) for rdata in answers]
            except Exception:
                records['NS'] = []
            
            return records
        except (TimeoutError, ConnectionError, OSError) as e:
            return {"error": f"Ошибка сети: {e}"}
        except Exception as e:
            return {"error": str(e)}
    
    def _get_ip(self, domain: str) -> str:
        """Получить IP адрес домена."""
        try:
            ip = socket.gethostbyname(domain)
            return ip
        except (socket.gaierror, TimeoutError, OSError):
            return None
    
    def _get_ip_geo(self, ip: str) -> Dict[str, Any]:
        """Получить геолокацию IP (используем бесплатный API)."""
        try:
            import requests
            
            response = requests.get(f"https://ip-api.com/json/{ip}", timeout=10)
            data = response.json()
            
            if data.get('status') == 'success':
                return {
                    "country": data.get('country'),
                    "region": data.get('regionName'),
                    "city": data.get('city'),
                    "isp": data.get('isp'),
                    "org": data.get('org'),
                    "as": data.get('as'),
                    "lat": data.get('lat'),
                    "lon": data.get('lon'),
                    "timezone": data.get('timezone'),
                    "maps_url": f"https://www.google.com/maps?q={data.get('lat')},{data.get('lon')}"
                }
        except (requests.RequestException, TimeoutError, OSError):
            pass
        
        return None
    
    def run(self, domain: str) -> Dict[str, Any]:
        return self.check(domain)
