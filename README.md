<div align="center">

# 👁️ ShadowEye

### 🎯 Multi-Tool OSINT Framework for Linux & Windows

**Мощный консольный инструмент для разведки: Email, Username, Phone, Domain, EXIF.**  
Кроссплатформенность, кэширование, прокси-ротация и красивые отчеты.

[![PyPI version](https://badge.fury.io/py/shadoweye.svg)](https://pypi.org/project/shadoweye/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-orange.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20Termux-green.svg)](https://github.com/lixynhay/ShadowEye)

</div>

---

##  Возможности

| Модуль | Описание | Технологии |
| :--- | :--- | :--- |
| 📧 **Email OSINT** | Проверка регистрации в 120+ сервисах | Holehe |
| 👤 **Username OSINT** | Поиск аккаунтов по никнейму | Maigret + Sherlock (Built-in) |
| 📞 **Phone OSINT** | Анализ номера (страна, оператор, тип) | Google libphonenumber |
| 🌐 **Domain OSINT** | WHOIS, DNS записи, IP Geolocation | python-whois, dnspython |
| 🖼️ **EXIF Analyzer** | Метаданные фото + GPS на карте | ExifRead |
| 🎯 **All-in-One** | Комплексный анализ всех типов данных | — |
| 📦 **Batch Mode** | Пакетная обработка целей из файла | — |
| 🔧 **Proxy Manager** | Ротация прокси для обхода блокировок | HTTP/SOCKS5 support |

### ✨ Ключевые преимущества
- **🔄 Умное кэширование**: Результаты сохраняются на 24ч, чтобы не тратить время на повторные проверки.
- **🌍 Прокси-ротация**: Автоматическая смена IP для обхода Rate Limit.
- **📊 Интерактивные отчеты**: Экспорт в JSON и красивый HTML с поиском и картами.
- ** Кроссплатформенность**: Стабильная работа на Windows 10/11, Linux и Android (Termux).
- **⚡ Валидация данных**: Встроенная проверка формата email, телефонов и доменов перед запросом.

---

## 🚀 Установка

### Вариант 1: Через PyPI (Рекомендуется)
Самый быстрый способ установки. Открой терминал и выполни:

```bash
pip install shadoweye
```

### Вариант 2: Из исходников (GitHub)
Если хочешь получить самую свежую версию или внести изменения:

```bash
git clone https://github.com/lixynhay/ShadowEye.git
cd ShadowEye
pip install -r requirements.txt
pip install -e .
```

---

## 📖 Использование

После установки просто запусти команду в терминале:

```bash
shadoweye
```

Или используй модульный запуск:
```bash
python -m osint_toolkit
```


### Примеры работы

**📧 Email Check:**
> Введи `example@gmail.com` → Получи список сервисов, где этот email зарегистрирован.

** Username Search:**
> Введи `nickname` → Выбери Sherlock (быстро) или Maigret (глубоко) → Найди профили в соцсетях.

**🌐 Domain Analysis:**
> Введи `target.com` → Узнай регистратора, DNS-серверы и физическое расположение сервера.

---

##  Структура проекта

Проект имеет четкую модульную архитектуру:

```text
ShadowEye/
├── osint_toolkit/          # Основной пакет
│   ├── cli.py              # Главный интерфейс и меню
│   ├── aggregator.py       # Сбор и экспорт результатов
│   ├── ui.py               # UI компоненты (Rich library)
│   ├── core/               # Ядро инструментов
│   │   ├── email_checker.py
│   │   ├── username_checker.py
│   │   ├── phone_checker.py
│   │   ├── domain_checker.py
│   │   └── exif_analyzer.py
│   ├── utils/              # Вспомогательные утилиты
│   │   ├── cache.py        # Система кэширования
│   │   ├── validators.py   # Валидация входных данных
│   │   ├── proxy_rotator.py# Управление прокси
│   │   ── html_report.py  # Генератор HTML-отчетов
│   └── sherlock_builtin/   # Встроенная версия Sherlock
├── setup.py                # Конфигурация пакета
├── requirements.txt        # Зависимости
└── README.md
```

---

## 🛠️ Требования

- Python 3.10+
- Работает на Linux, macOS и Windows (ограничения зависят от движков и наличия зависимостей)

Опционально: прокси для обхода rate-limits и дополнительная оперативная память при полносканировании.

---

## 📤 Экспорт отчётов

- JSON — структурированные данные для автоматизации и интеграций
- HTML — интерактивный отчёт с поиском и картой для визуального анализа

---

## 🤝 Вклад

Pull requests и issues приветствуются. Для крупных изменений открой issue заранее.

---

## 📜 Лицензия

Этот проект распространяется под лицензией MIT. См. файл [LICENSE](LICENSE).

---

**Сделано с ❤️ для OSINT сообщества**