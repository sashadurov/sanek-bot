from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from database import init_db, create_user, get_user, get_all_users
from models import User
from keyboards import main_menu, back_button

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    init_db()
    create_user(message.from_user.id, message.from_user.username or message.from_user.first_name)

    text = (
        f"👋 <b>Привет, {message.from_user.first_name}!</b>\n\n"
        f"🎮 Добро пожаловать в <b>Бот Бандит</b>!\n"
        f"Здесь ты можешь зарабатывать деньги, покупать бизнесы, недвижимость, машины и играть в казино!\n\n"
        f"💰 Стартовый баланс: <b>1000₽</b>\n"
        f"📈 Прокачивайся и стань самым богатым!"
    )
    await message.answer(text, reply_markup=main_menu(), parse_mode="HTML")

@router.callback_query(F.data == "back_main")
async def back_main(callback: CallbackQuery):
    await show_profile(callback)

async def show_profile(callback: CallbackQuery):
    row = get_user(callback.from_user.id)
    if not row:
        await callback.message.edit_text("❌ Ошибка! Напиши /start")
        return

    user = User(row)

    text = (
        f"👤 <b>Профиль</b>\n\n"
        f"💰 Баланс: <b>{user.balance:,}₽</b>\n"
        f"⭐ Уровень: <b>{user.level}</b>\n"
        f"📊 Опыт: <b>{user.xp}</b>\n"
        f"💼 Работа: <b>{user.get_job_name()}</b>\n"
        f"🏢 Бизнесов: <b>{len(user.businesses)}</b>"
    )
    await callback.message.edit_text(text, reply_markup=main_menu(), parse_mode="HTML")

@router.callback_query(F.data == "menu_inventory")
async def show_inventory(callback: CallbackQuery):
    row = get_user(callback.from_user.id)
    if not row:
        await callback.message.edit_text("❌ Ошибка! Напиши /start")
        return

    user = User(row)
    text = user.get_inventory_text()
    await callback.message.edit_text(text, reply_markup=back_button(), parse_mode="HTML")

@router.callback_query(F.data == "menu_top")
async def show_top(callback: CallbackQuery):
    users = get_all_users()
    text = "🏆 <b>Топ 20 богачей:</b>\n\n"
    for i, (uid, uname, balance, level) in enumerate(users, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        name = uname or f"User_{uid}"
        text += f"{medal} {name} — <b>{balance:,}₽</b> (Lvl {level})\n"

    await callback.message.edit_text(text, reply_markup=back_button(), parse_mode="HTML")
