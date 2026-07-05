<div align="center">

# 👁️ ShadowEye

### 🎯 Модульный OSINT-инструментарий

**Набор утилит для разведки: email, username, phone, domain, EXIF и агрегирование результатов.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)
[![Windows](https://img.shields.io/badge/platform-Windows-green.svg)](https://www.microsoft.com/)
[![Termux](https://img.shields.io/badge/platform-Termux-green.svg)](https://termux.com/)
[![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)](https://www.kernel.org/)
</div>

---

## 🌟 Возможности

- Email OSINT — проверка аккаунтов и утечек
- Username OSINT — поиск аккаунтов по нику (Sherlock/встроенные движки)
- Phone OSINT — определение страны, оператора, типа номера
- Domain OSINT — WHOIS, DNS, IP-геолокация
- EXIF Analyzer — извлечение метаданных изображений (GPS)
- All-in-One — комбинированный анализ по нескольким типам данных
- Batch Mode — пакетная обработка целей из файла
- Экспорт в JSON и интерактивный HTML-отчёт

### ✨ Ключевые фичи

- Кэширование результатов (избегает повторных проверок)
- Ротация прокси для обхода ограничений
- Генерация подробных HTML-отчётов с поиском и картами

---

## 🚀 Установка

1) Клонируй репозиторий:

```
git clone https://github.com/lixynhay/ShadowEye.git
cd ShadowEye
```

2) Установи зависимости:

```
pip install -r requirements.txt
```

3) Установи пакет (локально):

```
pip install -e .
```

4) Запуск:

```
shadoweye
# или
python -m osint_toolkit
```

---

## 📖 Использование

Запусти `shadoweye` или `python -m osint_toolkit` и выбери режим в интерактивном меню.

Примеры режимов: Email, Username, Phone, Domain, Image EXIF, All-in-One, Batch.

---

## 📁 Структура проекта (актуально)

```
ShadowEye/
├── osint_toolkit/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── aggregator.py
│   ├── ui.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── domain_checker.py
│   │   ├── email_checker.py
│   │   ├── exif_analyzer.py
│   │   ├── phone_checker.py
│   │   └── username_checker.py
│   ├── sherlock_builtin/
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   ├── notify.py
│   │   ├── result.py
│   │   └── sherlock.py
│   └── sherlock_project/
│       ├── __init__.py
│       ├── __main__.py
│       ├── notify.py
│       ├── result.py
│       └── sherlock.py
├── utils/
│   ├── __init__.py
│   ├── cache.py
│   ├── export.py
│   ├── html_report.py
│   ├── proxy_rotator.py
│   └── validators.py
├── requirements.txt
├── setup.py
├── README.md
├── LICENSE
└── .gitignore
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

