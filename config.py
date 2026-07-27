import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Стартовый баланс
START_BALANCE = 1000

# Работы
JOBS = {
    "cleaner": {"name": "🧹 Уборщик", "salary": 50, "cooldown": 60},
    "driver": {"name": "🚗 Водитель", "salary": 120, "cooldown": 120},
    "programmer": {"name": "💻 Программист", "salary": 300, "cooldown": 300},
    "manager": {"name": "💼 Менеджер", "salary": 500, "cooldown": 600},
    "director": {"name": "👔 Директор", "salary": 1000, "cooldown": 900},
}

# Бизнесы
BUSINESSES = {
    "cafe": {"name": "☕ Кафе", "price": 5000, "income": 200, "cooldown": 3600},
    "shop": {"name": "🏪 Магазин", "price": 15000, "income": 600, "cooldown": 3600},
    "hotel": {"name": "🏨 Отель", "price": 50000, "income": 2000, "cooldown": 3600},
    "casino": {"name": "🎰 Казино", "price": 100000, "income": 5000, "cooldown": 3600},
}

# Недвижимость
HOUSES = {
    "studio": {"name": "🏠 Студия", "price": 10000, "income": 0},
    "apartment": {"name": "🏢 Квартира", "price": 50000, "income": 0},
    "villa": {"name": "🏡 Вилла", "price": 200000, "income": 0},
    "mansion": {"name": "🏰 Особняк", "price": 1000000, "income": 0},
}

# Машины
CARS = {
    "lada": {"name": "🚗 Лада", "price": 5000, "income": 0},
    "bmw": {"name": "🚙 BMW", "price": 30000, "income": 0},
    "mercedes": {"name": "🚘 Mercedes", "price": 80000, "income": 0},
    "ferrari": {"name": "🏎️ Ferrari", "price": 300000, "income": 0},
}

# Одежда
CLOTHES = {
    "tshirt": {"name": "👕 Футболка", "price": 500, "income": 0},
    "jacket": {"name": "🧥 Куртка", "price": 2000, "income": 0},
    "suit": {"name": "🤵 Костюм", "price": 10000, "income": 0},
    "rolex": {"name": "⌚ Rolex", "price": 50000, "income": 0},
}
