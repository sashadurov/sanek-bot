from aiogram import Router, F
from aiogram.types import CallbackQuery
from datetime import datetime
import time
import json
import sqlite3
from database import get_user, update_balance, set_job
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
    
    # Получаем кулдауны для всех работ
    conn = sqlite3.connect("bandit.db")
    c = conn.cursor()
    c.execute("SELECT job_cooldowns FROM users WHERE user_id = ?", (callback.from_user.id,))
    result = c.fetchone()
    conn.close()
    
    cooldowns = {}
    if result and result[0]:
        try:
            cooldowns = json.loads(result[0])
        except:
            cooldowns = {}
    
    # Проверяем кулдаун для КОНКРЕТНОЙ работы
    last_used = cooldowns.get(job_key, 0)
    if now - last_used < job["cooldown"]:
        remaining = job["cooldown"] - (now - last_used)
        minutes = remaining // 60
        seconds = remaining % 60
        await callback.answer(f"⏳ Подожди ещё {minutes}м {seconds}с!")
        return
    
    # Обновляем кулдаун для этой работы
    cooldowns[job_key] = now
    
    conn = sqlite3.connect("bandit.db")
    c = conn.cursor()
    c.execute("UPDATE users SET job_cooldowns = ? WHERE user_id = ?", (json.dumps(cooldowns), callback.from_user.id))
    conn.commit()
    conn.close()
    
    # Назначаем работу (если новая)
    if user.job != job_key:
        set_job(callback.from_user.id, job_key)
    
    # Даём зарплату
    update_balance(callback.from_user.id, job["salary"])
    
    text = (
        f"✅ <b>Работа выполнена!</b>\n\n"
        f"💼 {job['name']}\n"
        f"💰 Заработано: <b>+{job['salary']:,}₽</b>\n"
        f"⏳ Кулдаун: {job['cooldown'] // 60} мин\n\n"
        f"💰 Новый баланс: <b>{user.balance + job['salary']:,}₽</b>"
    )
    await callback.message.edit_text(text, reply_markup=work_menu(), parse_mode="HTML")
