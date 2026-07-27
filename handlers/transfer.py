from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import get_user, update_balance
from models import User
from keyboards import back_button

router = Router()

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
        amount = int(message.text)
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
        f"Введи @username получателя:",
        reply_markup=back_button(),
        parse_mode="HTML"
    )
    await state.set_state(TransferState.waiting_for_username)

@router.message(TransferState.waiting_for_username)
async def process_username(message: Message, state: FSMContext):
    username = message.text.strip().replace("@", "")
    data = await state.get_data()
    amount = data["amount"]

    # Находим пользователя по username
    from database import get_all_users
    users = get_all_users()

    recipient = None
    for uid, uname, balance, level in users:
        if uname and uname.lower() == username.lower():
            recipient = uid
            break

    if not recipient:
        await message.answer("❌ Пользователь не найден! Убедись, что он писал боту.")
        return

    if recipient == message.from_user.id:
        await message.answer("❌ Нельзя перевести самому себе!")
        return

    update_balance(message.from_user.id, -amount)
    update_balance(recipient, amount)

    await message.answer(
        f"✅ <b>Перевод выполнен!</b>\n\n"
        f"💰 Переведено: <b>{amount:,}₽</b>\n"
        f"👤 Получатель: @{username}",
        reply_markup=back_button(),
        parse_mode="HTML"
    )
    await state.clear()
