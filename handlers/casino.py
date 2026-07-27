from aiogram import Router, F
from aiogram.types import CallbackQuery
import random
from database import get_user, update_balance
from models import User
from keyboards import casino_menu, slots_buttons, coin_buttons, dice_buttons, back_button

router = Router()

SLOTS = ["🍒", "🍋", "🍊", "🍇", "💎", "7️⃣", "🎰"]

@router.callback_query(F.data == "menu_casino")
async def casino_menu_handler(callback: CallbackQuery):
    row = get_user(callback.from_user.id)
    if not row:
        await callback.message.edit_text("❌ Ошибка! Напиши /start")
        return

    user = User(row)

    text = (
        f"🎰 <b>Казино</b>\n\n"
        f"💰 Баланс: <b>{user.balance:,}₽</b>\n\n"
        f"Выбери игру:"
    )
    await callback.message.edit_text(text, reply_markup=casino_menu(), parse_mode="HTML")

# ===== СЛОТЫ =====
@router.callback_query(F.data == "casino_slots")
async def slots_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        "🎰 <b>Слоты</b>\n\n"
        "Собери 3 одинаковых символа и выиграй!\n"
        "🍒🍒🍒 = x2\n"
        "🍋🍋🍋 = x3\n"
        "🍊🍊🍊 = x4\n"
        "🍇🍇🍇 = x5\n"
        "💎💎💎 = x10\n"
        "7️⃣7️⃣7️⃣ = x20\n"
        "🎰🎰🎰 = x50",
        reply_markup=slots_buttons(),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("slots_spin_"))
async def spin_slots(callback: CallbackQuery):
    bet = int(callback.data.replace("slots_spin_", ""))

    row = get_user(callback.from_user.id)
    user = User(row)

    if user.balance < bet:
        await callback.answer(f"❌ Недостаточно денег! Нужно {bet}₽")
        return

    update_balance(callback.from_user.id, -bet)

    # Крутим слоты
    result = [random.choice(SLOTS) for _ in range(3)]

    multipliers = {
        "🍒": 2, "🍋": 3, "🍊": 4, "🍇": 5, "💎": 10, "7️⃣": 20, "🎰": 50
    }

    if result[0] == result[1] == result[2]:
        win = bet * multipliers.get(result[0], 1)
        update_balance(callback.from_user.id, win)

        text = (
            f"🎰 <b>{result[0]} | {result[1]} | {result[2]}</b>\n\n"
            f"🎉 <b>ДЖЕКПОТ!</b>\n"
            f"💰 Выигрыш: <b>+{win:,}₽</b>\n"
            f"💰 Баланс: <b>{user.balance - bet + win:,}₽</b>"
        )
    else:
        text = (
            f"🎰 <b>{result[0]} | {result[1]} | {result[2]}</b>\n\n"
            f"😢 Не повезло...\n"
            f"💰 Проиграно: <b>{bet:,}₽</b>\n"
            f"💰 Баланс: <b>{user.balance - bet:,}₽</b>"
        )

    await callback.message.edit_text(text, reply_markup=slots_buttons(), parse_mode="HTML")

# ===== МОНЕТКА =====
@router.callback_query(F.data == "casino_coin")
async def coin_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        "🪙 <b>Монетка</b>\n\n"
        "Угадай, что выпадет — Орёл или Решка!\n"
        "Правильный ответ = x2 ставка",
        reply_markup=coin_buttons(),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("coin_"))
async def flip_coin(callback: CallbackQuery):
    parts = callback.data.split("_")
    choice = parts[1]  # eagle или tails
    bet = int(parts[2])

    row = get_user(callback.from_user.id)
    user = User(row)

    if user.balance < bet:
        await callback.answer(f"❌ Недостаточно денег! Нужно {bet}₽")
        return

    update_balance(callback.from_user.id, -bet)

    result = random.choice(["eagle", "tails"])
    result_emoji = "🦅 Орёл" if result == "eagle" else "🪙 Решка"
    choice_emoji = "🦅 Орёл" if choice == "eagle" else "🪙 Решка"

    if choice == result:
        win = bet * 2
        update_balance(callback.from_user.id, win)
        text = (
            f"🪙 <b>{result_emoji}</b>\n\n"
            f"✅ Ты выбрал: {choice_emoji}\n"
            f"🎉 Правильно!\n"
            f"💰 Выигрыш: <b>+{win:,}₽</b>\n"
            f"💰 Баланс: <b>{user.balance - bet + win:,}₽</b>"
        )
    else:
        text = (
            f"🪙 <b>{result_emoji}</b>\n\n"
            f"❌ Ты выбрал: {choice_emoji}\n"
            f"😢 Не угадал...\n"
            f"💰 Проиграно: <b>{bet:,}₽</b>\n"
            f"💰 Баланс: <b>{user.balance - bet:,}₽</b>"
        )

    await callback.message.edit_text(text, reply_markup=coin_buttons(), parse_mode="HTML")

# ===== КОСТИ =====
@router.callback_query(F.data == "casino_dice")
async def dice_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        "🎲 <b>Кости</b>\n\n"
        "Брось кости!\n"
        "Если сумма > 7 — выигрыш x2\n"
        "Если сумма = 12 — выигрыш x5",
        reply_markup=dice_buttons(),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("dice_roll_"))
async def roll_dice(callback: CallbackQuery):
    bet = int(callback.data.replace("dice_roll_", ""))

    row = get_user(callback.from_user.id)
    user = User(row)

    if user.balance < bet:
        await callback.answer(f"❌ Недостаточно денег! Нужно {bet}₽")
        return

    update_balance(callback.from_user.id, -bet)

    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    total = dice1 + dice2

    if total == 12:
        win = bet * 5
        update_balance(callback.from_user.id, win)
        text = (
            f"🎲 <b>{dice1} + {dice2} = {total}</b>\n\n"
            f"🔥 <b>МАКСИМУМ!</b>\n"
            f"💰 Выигрыш: <b>+{win:,}₽</b>\n"
            f"💰 Баланс: <b>{user.balance - bet + win:,}₽</b>"
        )
    elif total > 7:
        win = bet * 2
        update_balance(callback.from_user.id, win)
        text = (
            f"🎲 <b>{dice1} + {dice2} = {total}</b>\n\n"
            f"✅ Больше 7! Победа!\n"
            f"💰 Выигрыш: <b>+{win:,}₽</b>\n"
            f"💰 Баланс: <b>{user.balance - bet + win:,}₽</b>"
        )
    else:
        text = (
            f"🎲 <b>{dice1} + {dice2} = {total}</b>\n\n"
            f"😢 7 или меньше... Проигрыш\n"
            f"💰 Проиграно: <b>{bet:,}₽</b>\n"
            f"💰 Баланс: <b>{user.balance - bet:,}₽</b>"
        )

    await callback.message.edit_text(text, reply_markup=dice_buttons(), parse_mode="HTML")
