"""Username OSINT через Maigret + Sherlock."""
import asyncio
import os
import json
import tempfile
import shutil
from typing import List, Dict, Any
from ..ui import console, create_progress

class UsernameChecker:
    def __init__(self, proxy: str = None, timeout: int = 30):
        self.proxy = proxy
        self.timeout = timeout
        self._maigret_available = False
        self._sherlock_available = False
        self._db_path = None
        self._sherlock_path = None
        self._check_tools()
    
    def _check_tools(self):
        # Maigret
        try:
            import maigret
            self._maigret_available = True
            
            possible_paths = [
                os.path.expanduser('~/.maigret/data.json'),
                os.path.join(os.path.dirname(maigret.__file__), 'resources', 'data.json'),
            ]
            for p in possible_paths:
                if os.path.exists(p):
                    self._db_path = p
                    break
        except ImportError:
            self._maigret_available = False
        
        # Sherlock (встроенный)
        sherlock_paths = [
            os.path.join(os.path.dirname(__file__), '..', 'sherlock_builtin', 'sherlock.py'),
            os.path.expanduser('~/sherlock/sherlock_project/sherlock.py'),
        ]
        for p in sherlock_paths:
            if os.path.exists(p):
                self._sherlock_path = p
                self._sherlock_available = True
                break
        
        if self._sherlock_available:
            console.print(f"[green]✓ Sherlock найден: {self._sherlock_path}[/green]")
    
    def is_available(self) -> bool:
        return self._maigret_available or self._sherlock_available
    
    async def check(self, username: str, use_sherlock: bool = False, full_search: bool = False) -> List[Dict[str, Any]]:
        if use_sherlock and self._sherlock_available:
            return await self._check_sherlock(username)
        elif self._maigret_available:
            return await self._check_maigret(username, full_search)
        elif self._sherlock_available:
            console.print("[yellow]⚠ Maigret недоступен, используем Sherlock[/yellow]")
            return await self._check_sherlock(username)
        else:
            console.print("[bold red]✗ Ни Maigret, ни Sherlock не установлены[/bold red]")
            return []
    
    async def _check_maigret(self, username: str, full_search: bool = False) -> List[Dict[str, Any]]:
        """Проверка через Maigret."""
        results = []
        tmpdir = tempfile.mkdtemp(prefix="maigret_", dir=os.path.expanduser('~'))
        
        try:
            cmd = [
                "python", "-m", "maigret",
                username,
                "--timeout", str(self.timeout),
                "--dns-resolver", "threaded",
                "--no-progressbar",
                "--folderoutput", tmpdir,
                "-J", "simple",
            ]
            
            if full_search:
                cmd.append("-a")
            
            if self._db_path:
                cmd.extend(["--db", self._db_path])
            
            if self.proxy:
                cmd.extend(["--proxy", self.proxy])
            
            console.print(f"[cyan]ℹ Maigret ищет: {username}[/cyan]")
            
            with create_progress() as progress:
                task = progress.add_task(f"[cyan]Maigret сканирует...", total=100)
                
                proc = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                stdout, stderr = await proc.communicate()
                progress.update(task, completed=100)
                
                stdout_text = stdout.decode('utf-8', errors='ignore') if stdout else ""
                
                for line in stdout_text.split('\n'):
                    if 'accounts' in line.lower() or 'returned' in line.lower():
                        console.print(f"[cyan]{line}[/cyan]")
            
            json_files = [f for f in os.listdir(tmpdir) if f.endswith('.json')]
            
            if not json_files:
                return results
            
            json_path = os.path.join(tmpdir, json_files[0])
            
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            console.print(f"[green]✓ Всего сайтов: {len(data)}[/green]")
            
            for site_name, site_data in data.items():
                status_info = site_data.get('status', {})
                status_str = status_info.get('status', 'unknown')
                exists = status_str == 'Claimed'
                
                url = status_info.get('url', site_data.get('url_user', ''))
                tags = status_info.get('tags', site_data.get('site', {}).get('tags', []))
                ids = status_info.get('ids', {})
                
                details_parts = []
                if ids.get('created_at'):
                    details_parts.append(f"Создан: {ids['created_at']}")
                if ids.get('fullname'):
                    details_parts.append(f"Имя: {ids['fullname']}")
                
                details = " | ".join(details_parts) if details_parts else ""
                
                results.append({
                    "service": site_name,
                    "exists": exists,
                    "url": url,
                    "status": status_str,
                    "details": details,
                    "tags": tags,
                    "ids": ids
                })
        
        except Exception as e:
            console.print(f"[bold red]✗ Ошибка Maigret: {e}[/bold red]")
        finally:
            try:
                shutil.rmtree(tmpdir)
            except:
                pass
        
        return results
    
    async def _check_sherlock(self, username: str) -> List[Dict[str, Any]]:
        """Проверка через Sherlock."""
        results = []
        
        try:
            cmd = [
                "python", self._sherlock_path,
                username,
                "--print-found",
            ]
            
            if self.proxy:
                cmd.extend(["--proxy", self.proxy])
            
            console.print(f"[cyan]ℹ Sherlock ищет: {username}[/cyan]")
            
            with create_progress() as progress:
                task = progress.add_task(f"[cyan]Sherlock сканирует...", total=100)
                
                proc = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                stdout, stderr = await proc.communicate()
                progress.update(task, completed=100)
                
                stdout_text = stdout.decode('utf-8', errors='ignore') if stdout else ""
                
                # Парсим вывод Sherlock: [+] Service: URL
                for line in stdout_text.split('\n'):
                    if line.strip().startswith('[+]'):
                        # Формат: [+] Service: https://...
                        parts = line.replace('[+]', '').split(':', 1)
                        if len(parts) >= 2:
                            service = parts[0].strip()
                            url = parts[1].strip()
                            
                            results.append({
                                "service": service,
                                "exists": True,
                                "url": url,
                                "status": "Claimed",
                                "details": "",
                                "tags": [],
                                "ids": {}
                            })
                
                console.print(f"[green]✓ Найдено аккаунтов: {len(results)}[/green]")
        
        except Exception as e:
            console.print(f"[bold red]✗ Ошибка Sherlock: {e}[/bold red]")
        
        return results
    
    def run(self, username: str, use_sherlock: bool = False, full_search: bool = False) -> List[Dict[str, Any]]:
        return asyncio.run(self.check(username, use_sherlock, full_search))
