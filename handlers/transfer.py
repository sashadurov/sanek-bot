from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import get_user, update_balance
from models import User
from keyboards import back_button
import sqlite3
import logging

router = Router()
logger = logging.getLogger(__name__)

class TransferState(StatesGroup):
    waiting_for_amount = State()
    waiting_for_username = State()

@router.callback_query(F.data == "menu_transfer")
async def transfer_menu(callback: CallbackQuery, state: FSMContext):
    row = get_user(callback.from_user.id)
    if not row:
        await callback.message.edit_text("❌ Ошибка! Напиши /start")
        return
    
    user = User(row)
    
    await callback.message.edit_text(
        f"💳 <b>Перевод денег</b>\n\n"
        f"💰 Баланс: <b>{user.balance:,}₽</b>\n\n"
        f"Введи сумму для перевода:",
        reply_markup=back_button(),
        parse_mode="HTML"
    )
    await state.set_state(TransferState.waiting_for_amount)

@router.message(TransferState.waiting_for_amount)
async def process_amount(message: Message, state: FSMContext):
    try:
        amount = int(message.text.strip())
        if amount <= 0:
            await message.answer("❌ Сумма должна быть больше 0!")
            return
    except ValueError:
        await message.answer("❌ Введи число!")
        return
    
    row = get_user(message.from_user.id)
    user = User(row)
    
    if user.balance < amount:
        await message.answer(f"❌ Недостаточно денег! У тебя {user.balance:,}₽")
        return
    
    await state.update_data(amount=amount)
    await message.answer(
        f"💳 Перевод <b>{amount:,}₽</b>\n\n"
        f"Введи @username получателя (без @):",
        reply_markup=back_button(),
        parse_mode="HTML"
    )
    await state.set_state(TransferState.waiting_for_username)

@router.message(TransferState.waiting_for_username)
async def process_username(message: Message, state: FSMContext):
    username = message.text.strip().replace("@", "").lower()
    data = await state.get_data()
    amount = data["amount"]
    
    conn = sqlite3.connect("bandit.db")
    c = conn.cursor()
    c.execute("SELECT user_id, username, balance FROM users WHERE LOWER(username) = ?", (username,))
    row = c.fetchone()
    conn.close()
    
    if not row:
        await message.answer(
            f"❌ Пользователь @{username} не найден!\n\n"
            f"Возможные причины:\n"
            f"• Пользователь ещё не писал боту\n"
            f"• Неправильный username\n"
            f"• У пользователя нет username в Telegram",
            reply_markup=back_button(),
            parse_mode="HTML"
        )
        await state.clear()
        return
    
    recipient_id, recipient_name, recipient_balance = row
    
    if recipient_id == message.from_user.id:
        await message.answer("❌ Нельзя перевести самому себе!")
        await state.clear()
        return
    
    update_balance(message.from_user.id, -amount)
    update_balance(recipient_id, amount)
    
    sender_row = get_user(message.from_user.id)
    sender = User(sender_row)
    
    await message.answer(
        f"✅ <b>Перевод выполнен!</b>\n\n"
        f"💰 Переведено: <b>{amount:,}₽</b>\n"
        f"👤 Получатель: @{recipient_name or username}\n"
        f"💰 Твой баланс: <b>{sender.balance:,}₽</b>",
        reply_markup=back_button(),
        parse_mode="HTML"
    )
    
    try:
        from aiogram import Bot
        from config import BOT_TOKEN
        
        temp_bot = Bot(token=BOT_TOKEN)
        sender_username = message.from_user.username or message.from_user.first_name or "Аноним"
        
        await temp_bot.send_message(
            chat_id=recipient_id,
            text=(
                f"🎉 <b>Тебе перевели деньги!</b>\n\n"
                f"💰 Сумма: <b>+{amount:,}₽</b>\n"
                f"👤 Отправитель: @{sender_username}\n"
                f"💰 Новый баланс: <b>{recipient_balance + amount:,}₽</b>\n\n"
                f"💳 Введи /start чтобы открыть меню"
            ),
            parse_mode="HTML"
        )
        
        await temp_bot.session.close()
        logger.info(f"Уведомление отправлено получателю {recipient_id}")
        
    except Exception as e:
        logger.error(f"Не удалось уведомить получателя {recipient_id}: {e}")
    
    await state.clear()
