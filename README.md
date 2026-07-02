<div align="center">

# 👁️ ShadowEye

### 🎯 Multi-Tool OSINT Framework for Termux

**Твой карманный инструмент разведки — email, username, phone, domain, EXIF**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Termux-green.svg)](https://termux.com/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

</div>

---

## 🌟 Возможности

| # | Режим | Описание | Движок |
|---|-------|----------|--------|
| 1 | 📧 Email OSINT | Проверка регистрации в 120+ сервисах | Holehe |
| 2 | 👤 Username OSINT | Поиск аккаунтов по никнейму | Maigret (3000+) / Sherlock (400+) |
| 3 | 📞 Phone OSINT | Анализ номера (страна, оператор, тип) | Google libphonenumber |
| 4 | 🌐 Domain OSINT | WHOIS, DNS, IP Geolocation | python-whois + dnspython |
| 5 | ️ EXIF Analyzer | Метаданные фото + GPS на карте | ExifRead |
| 6 | 🎯 All-in-One | Комбинированный анализ всех типов | — |
| 7 | 📦 Batch Mode | Пакетная обработка из файла | — |
| 8 | 🔧 Proxy Manager | Ротация прокси для обхода блокировок | — |

### ✨ Ключевые фичи

- 🔄 **Кэширование** — не проверяет повторно (24ч)
- 🌍 **Прокси-ротация** — обход rate limit
- 📊 **Экспорт** — JSON и красивый интерактивный HTML
- 🗺️ **GPS карта** — встроенная Google Maps для EXIF
- 🔍 **Поиск в отчётах** — фильтрация в HTML
- 📱 **Termux-first** — оптимизировано под Android

---

## 🚀 Установка

### 1. Клонируй репозиторий

    git clone https://github.com/lixynhay/ShadowEye.git
    cd ShadowEye

### 2. Установи зависимости

    pip install -r requirements.txt

### 3. Установи пакет

    pip install -e .

### 4. Запуск

    shadoweye
    # или
    python -m osint_toolkit

---

## 📖 Использование

Запусти и выбери режим из меню:

    shadoweye

Меню:

    ────────────────────────── 🎯 ShadowEye v3.1 ─────────────────────────────
    │ 1. 📧 Email OSINT (Holehe) — проверка регистрации email                  │
    │ 2. 👤 Username OSINT (Maigret/Sherlock) — поиск по никнейму              │
    │ 3.  Phone OSINT — анализ телефона                                      │
    │ 4. 🌐 Domain OSINT — WHOIS, DNS, IP                                      │
    │ 5. 🖼️  Image EXIF — анализ метаданных                                    │
    │ 6. 🎯 All-in-One — комбинированный анализ                                │
    │ 7. 📦 Batch Mode — пакетная обработка                                    │
    │ 8. 🔧 Настройка прокси                                                   │
    │ 0.  Выход                                                              │
    ──────────────────────────────────────────────────────────────────────────

### Примеры

**Email OSINT:**

    Введите email: example@gmail.com
    → Проверка в 120+ сервисах
    → Результат: найден на GitHub, VK, Twitch...

**Username OSINT:**

    Введите username: "username"
    → Maigret: 3000+ сайтов или Sherlock: 400+ сайтов
    → Найдено: GitHub, VK, Kick, Roblox...

**Domain OSINT:**

    Введите домен: example.com
    → WHOIS: регистратор, даты, контакты
    → DNS: A, MX, TXT, NS записи
    → IP: геолокация на карте

### Batch Mode

Создай файл `targets.txt`:

    email:email@gmail.com
    username:hacker1337
    phone:+79001234567
    domain:target.com
    image:~/photos/leak.jpg

Запусти пакетную обработку — получи отчёт по всем целям.

---

## 📁 Структура проекта

    ShadowEye/
    ├── osint_toolkit/
    │   ├── __init__.py
    │   ├── cli.py              # Главный CLI интерфейс
    │   ├── aggregator.py       # Агрегатор результатов
    │   ├── ui.py               # UI компоненты (Rich)
    │   ├── core/
    │   │   ├── email_checker.py      # Holehe интеграция
    │   │   ├── username_checker.py   # Maigret + Sherlock
    │   │   ├── phone_checker.py      # Phonenumbers
    │   │   ├── domain_checker.py     # WHOIS + DNS
    │   │   └── exif_analyzer.py      # EXIF метаданные
    │   ├── utils/
    │   │   ├── cache.py              # Кэш результатов
    │   │   └── proxy_rotator.py      # Ротация прокси
    │   └── sherlock_builtin/         # Встроенный Sherlock
    ├── requirements.txt
    ├── setup.py
    ├── README.md
    └── LICENSE

---

## 🛠️ Требования

- **Python** 3.10+
- **Termux** (рекомендуется) или любой Linux
- **16 GB RAM** (для полного поиска Maigret)

### Опционально

- **Прокси** — для обхода rate limit (`~/.osint_proxies.txt`)

---

## 📤 Экспорт отчётов

### JSON
Структурированные данные для дальнейшей обработки.

### HTML
Красивый интерактивный отчёт с:
- 🔍 Поиском по таблицам
- 🗺️ Встроенной GPS картой
- 📊 Статистикой
- 🎨 Адаптивным дизайном

---

## ⚠️ Дисклеймер

Этот инструмент создан **только для образовательных целей** и легального OSINT.

**Не используй для:**
- ❌ Преследования людей
- ❌ Несанкционированного доступа
- ❌ Нарушения законов

Автор не несёт ответственности за неправомерное использование.

---

## 🤝 Вклад

Pull requests приветствуются! Для крупных изменений сначала открой issue.

---

## 📜 Лицензия

MIT License — используй свободно.

---

<div align="center">

**Сделано с ❤️ для OSINT сообщества**

*ShadowEye — видит то, что скрыто в тени* 👁️🌑

</div>
