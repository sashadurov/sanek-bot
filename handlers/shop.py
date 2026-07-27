from aiogram import Router, F
from aiogram.types import CallbackQuery
from database import get_user, update_balance, add_item
from models import User
from config import HOUSES, CARS, CLOTHES
from keyboards import shop_menu, back_button

router = Router()

@router.callback_query(F.data == "menu_shop")
async def shop_menu_handler(callback: CallbackQuery):
    row = get_user(callback.from_user.id)
    if not row:
        await callback.message.edit_text("❌ Ошибка! Напиши /start")
        return

    user = User(row)

    text = (
        f"🛒 <b>Магазин</b>\n\n"
        f"💰 Баланс: <b>{user.balance:,}₽</b>\n\n"
        f"Выбери категорию:"
    )
    await callback.message.edit_text(text, reply_markup=shop_menu(), parse_mode="HTML")

@router.callback_query(F.data == "shop_houses")
async def shop_houses(callback: CallbackQuery):
    row = get_user(callback.from_user.id)
    user = User(row)

    text = "🏠 <b>Недвижимость:</b>\n\n"
    for key, data in HOUSES.items():
        owned = "✅" if key in user.houses else ""
        text += f"{owned} {data['name']} — <b>{data['price']:,}₽</b>\n"
    text += f"\n💰 Баланс: <b>{user.balance:,}₽</b>"

    kb = InlineKeyboardMarkup(inline_keyboard=[])
    for key, data in HOUSES.items():
        kb.inline_keyboard.append([InlineKeyboardButton(
            text=f"Купить {data['name']}", 
            callback_data=f"buy_house_{key}"
        )])
    kb.inline_keyboard.append([InlineKeyboardButton(text="🔙 Назад", callback_data="menu_shop")])

    await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")

@router.callback_query(F.data == "shop_cars")
async def shop_cars(callback: CallbackQuery):
    row = get_user(callback.from_user.id)
    user = User(row)

    text = "🚗 <b>Автомобили:</b>\n\n"
    for key, data in CARS.items():
        owned = "✅" if key in user.cars else ""
        text += f"{owned} {data['name']} — <b>{data['price']:,}₽</b>\n"
    text += f"\n💰 Баланс: <b>{user.balance:,}₽</b>"

    kb = InlineKeyboardMarkup(inline_keyboard=[])
    for key, data in CARS.items():
        kb.inline_keyboard.append([InlineKeyboardButton(
            text=f"Купить {data['name']}", 
            callback_data=f"buy_car_{key}"
        )])
    kb.inline_keyboard.append([InlineKeyboardButton(text="🔙 Назад", callback_data="menu_shop")])

    await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")

@router.callback_query(F.data == "shop_clothes")
async def shop_clothes(callback: CallbackQuery):
    row = get_user(callback.from_user.id)
    user = User(row)

    text = "👕 <b>Одежда:</b>\n\n"
    for key, data in CLOTHES.items():
        owned = "✅" if key in user.clothes else ""
        text += f"{owned} {data['name']} — <b>{data['price']:,}₽</b>\n"
    text += f"\n💰 Баланс: <b>{user.balance:,}₽</b>"

    kb = InlineKeyboardMarkup(inline_keyboard=[])
    for key, data in CLOTHES.items():
        kb.inline_keyboard.append([InlineKeyboardButton(
            text=f"Купить {data['name']}", 
            callback_data=f"buy_clothes_{key}"
        )])
    kb.inline_keyboard.append([InlineKeyboardButton(text="🔙 Назад", callback_data="menu_shop")])

    await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")

@router.callback_query(F.data.startswith("buy_house_"))
async def buy_house(callback: CallbackQuery):
    item_key = callback.data.replace("buy_house_", "")
    await buy_item(callback, item_key, "house", HOUSES)

@router.callback_query(F.data.startswith("buy_car_"))
async def buy_car(callback: CallbackQuery):
    item_key = callback.data.replace("buy_car_", "")
    await buy_item(callback, item_key, "car", CARS)

@router.callback_query(F.data.startswith("buy_clothes_"))
async def buy_clothes_item(callback: CallbackQuery):
    item_key = callback.data.replace("buy_clothes_", "")
    await buy_item(callback, item_key, "clothes", CLOTHES)

async def buy_item(callback, item_key, item_type, catalog):
    if item_key not in catalog:
        await callback.answer("❌ Товар не найден!")
        return

    row = get_user(callback.from_user.id)
    user = User(row)
    item = catalog[item_key]

    # Проверяем, есть ли уже
    items_list = getattr(user, item_type + "s", [])
    if item_key in items_list:
        await callback.answer("❌ У тебя уже есть это!")
        return

    if user.balance < item["price"]:
        await callback.answer(f"❌ Недостаточно денег! Нужно {item['price']:,}₽")
        return

    update_balance(callback.from_user.id, -item["price"])
    add_item(callback.from_user.id, item_type, item_key)

    await callback.answer(f"✅ Куплено: {item['name']}!")
    await callback.message.edit_text(
        f"🎉 <b>Поздравляем с покупкой!</b>\n\n"
        f"{item['name']}\n"
        f"💰 Списано: <b>{item['price']:,}₽</b>",
        reply_markup=back_button(),
        parse_mode="HTML"
    )

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
