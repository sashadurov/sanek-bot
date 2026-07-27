from aiogram import Router, F
from aiogram.types import CallbackQuery
from datetime import datetime
import time
from database import get_user, update_balance, set_job, set_job_cooldown
from models import User
from config import JOBS
from keyboards import work_menu, back_button

router = Router()

@router.callback_query(F.data == "menu_work")
async def work_menu_handler(callback: CallbackQuery):
    row = get_user(callback.from_user.id)
    if not row:
        await callback.message.edit_text("❌ Ошибка! Напиши /start")
        return

    user = User(row)
    current_job = user.get_job_name()

    text = (
        f"💼 <b>Работа</b>\n\n"
        f"Текущая работа: <b>{current_job}</b>\n"
        f"💰 Баланс: <b>{user.balance:,}₽</b>\n\n"
        f"Выбери работу и зарабатывай!"
    )
    await callback.message.edit_text(text, reply_markup=work_menu(), parse_mode="HTML")

@router.callback_query(F.data.startswith("work_"))
async def do_work(callback: CallbackQuery):
    job_key = callback.data.replace("work_", "")

    if job_key not in JOBS:
        await callback.answer("❌ Неизвестная работа!")
        return

    row = get_user(callback.from_user.id)
    if not row:
        await callback.message.edit_text("❌ Ошибка! Напиши /start")
        return

    user = User(row)
    job = JOBS[job_key]
    now = int(time.time())

    # Проверяем кулдаун
    if user.job == job_key and now - user.job_last_used < job["cooldown"]:
        remaining = job["cooldown"] - (now - user.job_last_used)
        minutes = remaining // 60
        seconds = remaining % 60
        await callback.answer(f"⏳ Подожди ещё {minutes}м {seconds}с!")
        return

    # Назначаем работу (если новая)
    if user.job != job_key:
        set_job(callback.from_user.id, job_key)

    # Даём зарплату
    update_balance(callback.from_user.id, job["salary"])
    set_job_cooldown(callback.from_user.id, now)

    text = (
        f"✅ <b>Работа выполнена!</b>\n\n"
        f"💼 {job['name']}\n"
        f"💰 Заработано: <b>+{job['salary']:,}₽</b>\n"
        f"⏳ Кулдаун: {job['cooldown'] // 60} мин\n\n"
        f"💰 Новый баланс: <b>{user.balance + job['salary']:,}₽</b>"
    )
    await callback.message.edit_text(text, reply_markup=work_menu(), parse_mode="HTML")
