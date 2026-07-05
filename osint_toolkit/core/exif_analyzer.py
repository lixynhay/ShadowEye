import os
from typing import Dict, Any, Optional, List
from ..ui import console

# Важные теги которые стоит показывать
IMPORTANT_TAGS = {
    'Камера': [
        'Image Make',
        'Image Model',
        'Image Software',
    ],
    'Дата и время': [
        'Image DateTime',
        'EXIF DateTimeOriginal',
        'EXIF DateTimeDigitized',
        'EXIF SubSecTime',
    ],
    'Настройки съёмки': [
        'EXIF ExposureTime',
        'EXIF FNumber',
        'EXIF ISOSpeedRatings',
        'EXIF FocalLength',
        'EXIF FocalLengthIn35mmFilm',
        'EXIF ExposureProgram',
        'EXIF MeteringMode',
        'EXIF Flash',
        'EXIF WhiteBalance',
        'EXIF ExposureMode',
        'EXIF DigitalZoomRatio',
    ],
    'Изображение': [
        'Image ImageWidth',
        'Image ImageLength',
        'Image Orientation',
        'Image XResolution',
        'Image YResolution',
        'Image ResolutionUnit',
        'EXIF ExifImageWidth',
        'EXIF ExifImageLength',
        'EXIF ColorSpace',
    ],
    'Геолокация': [
        'GPS GPSLatitude',
        'GPS GPSLatitudeRef',
        'GPS GPSLongitude',
        'GPS GPSLongitudeRef',
        'GPS GPSAltitude',
        'GPS GPSTimeStamp',
        'GPS GPSDateStamp',
    ]
}

class ExifAnalyzer:
    def __init__(self):
        self._available = False
        self._check_exifread()
    
    def _check_exifread(self):
        try:
            import exifread
            self._available = True
        except ImportError:
            self._available = False
    
    def is_available(self) -> bool:
        return self._available
    
    def analyze(self, image_path: str) -> Dict[str, Any]:
        if not self._available:
            console.print("[bold red]✗ ExifRead не установлен. pip install exifread[/bold red]")
            return {"error": "ExifRead not installed"}
        
        if not os.path.exists(image_path):
            console.print(f"[bold red]✗ Файл не найден: {image_path}[/bold red]")
            return {"error": f"File not found: {image_path}"}
        
        import exifread
        
        try:
            with open(image_path, 'rb') as f:
                tags = exifread.process_file(f, details=True)
                
                result = {
                    "file": os.path.basename(image_path),
                    "path": os.path.abspath(image_path),
                    "size": os.path.getsize(image_path),
                    "tags_count": len(tags),
                    "metadata": {},
                    "gps": None,
                    "all_tags": {}
                }
                
                # Извлекаем только важные теги
                for category, tag_names in IMPORTANT_TAGS.items():
                    category_data = {}
                    for tag_name in tag_names:
                        if tag_name in tags:
                            value = str(tags[tag_name])
                            # Фильтруем бинарные данные и мусор
                            if not self._is_binary_or_garbage(value):
                                category_data[tag_name] = value
                    
                    if category_data:
                        result["metadata"][category] = category_data
                
                # Извлекаем GPS координаты
                gps_data = self._extract_gps(tags)
                if gps_data:
                    result["gps"] = gps_data
                
                # Сохраняем все теги для полного анализа (без бинарных данных)
                for k, v in tags.items():
                    value = str(v)
                    if not self._is_binary_or_garbage(value):
                        result["all_tags"][str(k)] = value
                
                return result
        
        except Exception as e:
            console.print(f"[bold red]✗ Ошибка при чтении EXIF: {e}[/bold red]")
            return {"error": str(e)}
    
    def _is_binary_or_garbage(self, value: str) -> bool:
        """Проверяем что значение не бинарное и не мусор."""
        if not value:
            return True
        
        # Бинарные данные
        if value.startswith("b'") or value.startswith('b"'):
            return True
        
        # Массивы байтов
        if value.startswith('[') and (', 0, 0, 0' in value or len(value) > 200):
            return True
        
        # Слишком длинные значения
        if len(value) > 100:
            return True
        
        return False
    
    def _extract_gps(self, tags: dict) -> Optional[Dict[str, Any]]:
        """Извлечь GPS координаты."""
        try:
            gps_lat = tags.get('GPS GPSLatitude')
            gps_lat_ref = tags.get('GPS GPSLatitudeRef')
            gps_lon = tags.get('GPS GPSLongitude')
            gps_lon_ref = tags.get('GPS GPSLongitudeRef')
            gps_alt = tags.get('GPS GPSAltitude')
            gps_time = tags.get('GPS GPSTimeStamp')
            gps_date = tags.get('GPS GPSDateStamp')
            
            if gps_lat and gps_lon:
                lat = self._convert_gps(gps_lat.values)
                lon = self._convert_gps(gps_lon.values)
                
                if str(gps_lat_ref) == 'S':
                    lat = -lat
                if str(gps_lon_ref) == 'W':
                    lon = -lon
                
                gps_data = {
                    "latitude": lat,
                    "longitude": lon,
                    "maps_url": f"https://www.google.com/maps?q={lat},{lon}"
                }
                
                if gps_alt:
                    gps_data["altitude"] = str(gps_alt)
                if gps_time:
                    gps_data["time"] = str(gps_time)
                if gps_date:
                    gps_data["date"] = str(gps_date)
                
                return gps_data
        except Exception:
            pass
        
        return None
    
    def _convert_gps(self, values) -> float:
        """Конвертировать GPS координаты в десятичные градусы."""
        try:
            d = float(values[0].num) / float(values[0].den)
            m = float(values[1].num) / float(values[1].den)
            s = float(values[2].num) / float(values[2].den)
            return d + (m / 60.0) + (s / 3600.0)
        except Exception:
            return 0.0
    
    def analyze_directory(self, directory: str) -> list:
        """Анализ всех изображений в директории."""
        results = []
        extensions = {'.jpg', '.jpeg', '.png', '.tiff', '.tif', '.webp'}
        
        if not os.path.isdir(directory):
            console.print(f"[bold red]✗ Директория не найдена: {directory}[/bold red]")
            return results
        
        for filename in os.listdir(directory):
            ext = os.path.splitext(filename)[1].lower()
            if ext in extensions:
                file_path = os.path.join(directory, filename)
                console.print(f"[cyan]📷 Анализ:[/cyan] {filename}")
                result = self.analyze(file_path)
                results.append(result)
        
        return results
