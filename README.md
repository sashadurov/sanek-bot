# 🤖 Бот Бандит — Telegram Bot

Полноценная игра в Telegram, похожая на популярного "бот бандит". Зарабатывай деньги, покупай бизнесы, недвижимость, машины, играй в казино и стань самым богатым!

## 🎮 Возможности

- 💼 **Работа** — 5 видов работ с разной зарплатой и кулдауном
- 🛒 **Магазин** — покупка недвижимости, автомобилей и одежды
- 🏢 **Бизнес** — пассивный доход (кафе, магазин, отель, казино)
- 🎰 **Казино** — слоты, монетка, кости
- 💳 **Переводы** — переводи деньги другим игрокам
- 📊 **Топ** — рейтинг богачей
- 📦 **Инвентарь** — просмотр купленных вещей

## 📦 Установка

### 1. Клонируй проект

```bash
git clone <ссылка-на-репо>
cd bandit_bot
```

### 2. Создай виртуальное окружение

```bash
python -m venv venv
```

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Установи зависимости

```bash
pip install -r requirements.txt
```

### 4. Получи токен у @BotFather

1. Напиши [@BotFather](https://t.me/BotFather) в Telegram
2. Отправь команду `/newbot`
3. Придумай имя и username для бота
4. Скопируй полученный **API Token**

### 5. Настрой .env

Открой файл `.env` и вставь свой токен:

```
BOT_TOKEN=1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ
```

### 6. Запусти бота

```bash
python bot.py
```

Бот запустится и начнёт получать сообщения!

## 🗂️ Структура проекта

```
bandit_bot/
├── .env                    # Токен бота
├── requirements.txt        # Зависимости
├── bot.py                  # Точка входа
├── config.py               # Конфигурация (цены, работы, бизнесы)
├── database.py             # SQLite база данных
├── models.py               # Модели пользователей
├── keyboards.py            # Кнопки меню
├── handlers/
│   ├── start.py            # Профиль, топ, инвентарь
│   ├── work.py             # Работа
│   ├── shop.py             # Магазин
│   ├── casino.py           # Казино
│   ├── business.py         # Бизнесы
│   └── transfer.py         # Переводы
└── utils.py                # Утилиты
```

## 🚀 Хостинг (бесплатный)

### Вариант 1: PythonAnywhere (самый простой)

1. Зарегистрируйся на [pythonanywhere.com](https://www.pythonanywhere.com)
2. Загрузи файлы через Files → Upload
3. Открой Console → Bash
4. Установи зависимости: `pip install -r requirements.txt`
5. Запусти: `python bot.py`
6. Чтобы бот работал 24/7, создай Scheduled Task

### Вариант 2: Render.com

1. Зарегистрируйся на [render.com](https://render.com)
2. Создай Web Service
3. Подключи GitHub репозиторий
4. Укажи:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python bot.py`
5. Добавь Environment Variable `BOT_TOKEN`

### Вариант 3: VPS (самый надёжный)

```bash
# Установи Python и git
sudo apt update
sudo apt install python3 python3-pip git screen

# Клонируй проект
git clone <ссылка>
cd bandit_bot

# Установи зависимости
pip3 install -r requirements.txt

# Запусти через screen (чтобы работал в фоне)
screen -S bandit_bot
python3 bot.py

# Отключись от screen: Ctrl+A, затем D
# Подключиться обратно: screen -r bandit_bot
```

## 📝 Кастомизация

Все цены, зарплаты и настройки находятся в `config.py`. Можешь легко изменить:

- Стартовый баланс
- Цены на товары
- Зарплаты работ
- Доход бизнесов
- Кулдауны

## ⚠️ Важно

- Не коммить файл `.env` в публичный репозиторий!
- Для продакшена используй PostgreSQL вместо SQLite
- Добавь обработку ошибок и логирование для стабильности

## 📄 Лицензия

MIT — делай что хочешь! 🎉
