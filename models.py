from database import get_user
from config import JOBS, BUSINESSES, HOUSES, CARS, CLOTHES
import json

class User:
    def __init__(self, row):
        self.user_id = row[0]
        self.username = row[1]
        self.balance = row[2]
        self.level = row[3]
        self.xp = row[4]
        self.job = row[5]
        self.job_last_used = row[6]
        self.businesses = json.loads(row[7]) if row[7] else {}
        self.houses = json.loads(row[8]) if row[8] else []
        self.cars = json.loads(row[9]) if row[9] else []
        self.clothes = json.loads(row[10]) if row[10] else []
        self.created_at = row[11]

    def get_job_name(self):
        if self.job and self.job in JOBS:
            return JOBS[self.job]["name"]
        return "Безработный"

    def get_businesses_list(self):
        result = []
        for key, data in self.businesses.items():
            if key in BUSINESSES:
                result.append({
                    "key": key,
                    "name": BUSINESSES[key]["name"],
                    "income": BUSINESSES[key]["income"],
                    "last_collected": data.get("last_collected", 0)
                })
        return result

    def get_inventory_text(self):
        text = "📦 <b>Инвентарь:</b>\n\n"

        if self.houses:
            text += "🏠 <b>Недвижимость:</b>\n"
            for h in self.houses:
                text += f"  • {HOUSES[h]['name']}\n"
            text += "\n"

        if self.cars:
            text += "🚗 <b>Автомобили:</b>\n"
            for c in self.cars:
                text += f"  • {CARS[c]['name']}\n"
            text += "\n"

        if self.clothes:
            text += "👕 <b>Одежда:</b>\n"
            for cl in self.clothes:
                text += f"  • {CLOTHES[cl]['name']}\n"
            text += "\n"

        if not self.houses and not self.cars and not self.clothes:
            text += "😕 Пусто... Купи что-нибудь в магазине!"

        return text
