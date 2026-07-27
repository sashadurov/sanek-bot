from aiogram import Router, F
from aiogram.types import CallbackQuery
import time
from database import get_user, update_balance, add_business, update_business_cooldown
from models import User
from config import BUSINESSES
from keyboards import business_menu, back_button

router = Router()

@router.callback_query(F.data == "menu_business")
async def business_menu_handler(callback: CallbackQuery):
    row = get_user(callback.from_user.id)
    if not row:
        await callback.message.edit_text("❌ Ошибка! Напиши /start")
        return

    user = User(row)

    text = (
        f"🏢 <b>Бизнес</b>\n\n"
        f"💰 Баланс: <b>{user.balance:,}₽</b>\n"
        f"📊 Твои бизнесы:\n"
    )

    businesses = user.get_businesses_list()
    if businesses:
        for b in businesses:
            text += f"  • {b['name']} — {b['income']:,}₽/ч\n"
    else:
        text += "  😕 Пока нет бизнесов\n"

    text += "\nКупи бизнес и получай пассивный доход!"

    await callback.message.edit_text(text, reply_markup=business_menu(), parse_mode="HTML")

@router.callback_query(F.data.startswith("buy_business_"))
async def buy_business(callback: CallbackQuery):
    business_key = callback.data.replace("buy_business_", "")

    if business_key not in BUSINESSES:
        await callback.answer("❌ Бизнес не найден!")
        return

    row = get_user(callback.from_user.id)
    user = User(row)
    business = BUSINESSES[business_key]

    if business_key in user.businesses:
        await callback.answer("❌ У тебя уже есть этот бизнес!")
        return

    if user.balance < business["price"]:
        await callback.answer(f"❌ Недостаточно денег! Нужно {business['price']:,}₽")
        return

    update_balance(callback.from_user.id, -business["price"])
    add_business(callback.from_user.id, business_key)

    await callback.answer(f"✅ Куплен бизнес: {business['name']}!")
    await callback.message.edit_text(
        f"🎉 <b>Бизнес куплен!</b>\n\n"
        f"{business['name']}\n"
        f"💰 Цена: <b>{business['price']:,}₽</b>\n"
        f"📈 Доход: <b>{business['income']:,}₽/ч</b>",
        reply_markup=back_button(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "collect_income")
async def collect_income(callback: CallbackQuery):
    row = get_user(callback.from_user.id)
    user = User(row)

    if not user.businesses:
        await callback.answer("❌ У тебя нет бизнесов!")
        return

    now = int(time.time())
    total_income = 0

    for key, data in user.businesses.items():
        if key in BUSINESSES:
            business = BUSINESSES[key]
            last_collected = data.get("last_collected", 0)
            elapsed = now - last_collected

            # Сколько часов прошло
            hours_passed = elapsed // business["cooldown"]
            if hours_passed > 0:
                income = hours_passed * business["income"]
                total_income += income
                update_business_cooldown(callback.from_user.id, key, now)

    if total_income > 0:
        update_balance(callback.from_user.id, total_income)
        await callback.message.edit_text(
            f"💰 <b>Доход собран!</b>\n\n"
            f"📈 Получено: <b>+{total_income:,}₽</b>\n"
            f"💰 Новый баланс: <b>{user.balance + total_income:,}₽</b>",
            reply_markup=back_button(),
            parse_mode="HTML"
        )
    else:
        await callback.answer("⏳ Пока нет дохода для сбора!")
