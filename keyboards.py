from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Главное меню
def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💼 Работа", callback_data="menu_work"),
         InlineKeyboardButton(text="🛒 Магазин", callback_data="menu_shop")],
        [InlineKeyboardButton(text="🏢 Бизнес", callback_data="menu_business"),
         InlineKeyboardButton(text="🎰 Казино", callback_data="menu_casino")],
        [InlineKeyboardButton(text="💳 Перевод", callback_data="menu_transfer"),
         InlineKeyboardButton(text="📊 Топ", callback_data="menu_top")],
        [InlineKeyboardButton(text="📦 Инвентарь", callback_data="menu_inventory")],
    ])

# Меню работы
def work_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧹 Уборщик (50₽/мин)", callback_data="work_cleaner")],
        [InlineKeyboardButton(text="🚗 Водитель (120₽/2мин)", callback_data="work_driver")],
        [InlineKeyboardButton(text="💻 Программист (300₽/5мин)", callback_data="work_programmer")],
        [InlineKeyboardButton(text="💼 Менеджер (500₽/10мин)", callback_data="work_manager")],
        [InlineKeyboardButton(text="👔 Директор (1000₽/15мин)", callback_data="work_director")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_main")],
    ])

# Меню магазина
def shop_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Недвижимость", callback_data="shop_houses")],
        [InlineKeyboardButton(text="🚗 Автомобили", callback_data="shop_cars")],
        [InlineKeyboardButton(text="👕 Одежда", callback_data="shop_clothes")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_main")],
    ])

# Меню казино
def casino_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎰 Слоты", callback_data="casino_slots")],
        [InlineKeyboardButton(text="🪙 Монетка", callback_data="casino_coin")],
        [InlineKeyboardButton(text="🎲 Кости", callback_data="casino_dice")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_main")],
    ])

# Меню бизнеса
def business_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="☕ Кафе (5000₽ / 200₽/ч)", callback_data="buy_business_cafe")],
        [InlineKeyboardButton(text="🏪 Магазин (15000₽ / 600₽/ч)", callback_data="buy_business_shop")],
        [InlineKeyboardButton(text="🏨 Отель (50000₽ / 2000₽/ч)", callback_data="buy_business_hotel")],
        [InlineKeyboardButton(text="🎰 Казино (100000₽ / 5000₽/ч)", callback_data="buy_business_casino")],
        [InlineKeyboardButton(text="💰 Собрать доход", callback_data="collect_income")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_main")],
    ])

# Назад в главное меню
def back_button():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_main")],
    ])

# Кнопки для слотов
def slots_buttons():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎰 Крутить (100₽)", callback_data="slots_spin_100")],
        [InlineKeyboardButton(text="🎰 Крутить (500₽)", callback_data="slots_spin_500")],
        [InlineKeyboardButton(text="🎰 Крутить (1000₽)", callback_data="slots_spin_1000")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="menu_casino")],
    ])

# Кнопки для монетки
def coin_buttons():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🦅 Орёл (100₽)", callback_data="coin_eagle_100")],
        [InlineKeyboardButton(text="🪙 Решка (100₽)", callback_data="coin_tails_100")],
        [InlineKeyboardButton(text="🦅 Орёл (500₽)", callback_data="coin_eagle_500")],
        [InlineKeyboardButton(text="🪙 Решка (500₽)", callback_data="coin_tails_500")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="menu_casino")],
    ])

# Кнопки для костей
def dice_buttons():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎲 Бросить (100₽)", callback_data="dice_roll_100")],
        [InlineKeyboardButton(text="🎲 Бросить (500₽)", callback_data="dice_roll_500")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="menu_casino")],
    ])
