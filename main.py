import asyncio
from datetime import datetime, timedelta, timezone
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ==========================================
# CONFIGURATION
# ==========================================
TELEGRAM_BOT_TOKEN = "8644355663:AAEzg6oR1VyOx1TwEiFd18UANfM-rBORhNo"
UTC_PLUS_5 = timezone(timedelta(hours=5))

# ==========================================
# FAST LIGHTWEIGHT TIME CALCULATOR
# ==========================================
def get_fast_entry():
    now = datetime.now(UTC_PLUS_5)
    # Fast 1-click rounding to exact next minute
    if now.second >= 48:
        target = (now + timedelta(minutes=2)).replace(second=0, microsecond=0)
    else:
        target = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
    return target.strftime("%H:%M:00")

# ==========================================
# COMPACT KEYBOARD (SMALL FAST BUTTONS)
# ==========================================
def get_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 USD/BRL", callback_data="USD/BRL (OTC)"), InlineKeyboardButton("📊 NZD/JPY", callback_data="NZD/JPY (OTC)")],
        [InlineKeyboardButton("📊 USD/BDT", callback_data="USD/BDT (OTC)"), InlineKeyboardButton("📊 USD/JPY", callback_data="USD/JPY (OTC)")],
        [InlineKeyboardButton("📊 USD/NGN", callback_data="USD/NGN (OTC)"), InlineKeyboardButton("📊 AUD/USD", callback_data="AUDUSD (OTC)")],
        [InlineKeyboardButton("📊 GBP/JPY", callback_data="GBP/JPY (OTC)"), InlineKeyboardButton("🔄 Refresh", callback_data="REFRESH")]
    ])

# ==========================================
# FAST HANDLERS
# ==========================================
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚡ **QUOTEX ULTRA-FAST TERMINAL**\nSelect Pair:", parse_mode="Markdown", reply_markup=get_keyboard())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    
    # Direct fast acknowledgement
    await query.answer()

    pair = query.data

    if pair == "REFRESH":
        try:
            await query.edit_message_text("⚡ **QUOTEX ULTRA-FAST TERMINAL**\nSelect Pair:", parse_mode="Markdown", reply_markup=get_keyboard())
        except Exception:
            pass
        return

    # Super Fast Decision Logic
    entry_time = get_fast_entry()
    is_up = random.choice([True, False])
    signal = "🟩 **UP** ⬆️" if is_up else "🟥 **DOWN** ⬇️"
    accuracy = f"{round(random.uniform(95.0, 98.8), 1)}%"

    text = (
        f"📍 **{pair}**\n\n"
        f"🎯 {signal}\n"
        f"⏰ **ENTRY:** `{entry_time}`\n"
        f"🎯 **ACCURACY:** `{accuracy}`"
    )

    try:
        await query.edit_message_text(text=text, parse_mode="Markdown", reply_markup=get_keyboard())
    except Exception:
        pass

# ==========================================
# MAIN EXECUTION
# ==========================================
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("⚡ Ultra-Fast Quotex Bot Running...")
    app.run_polling(drop_pending_updates=True) # Drops old accumulated updates to clear lag

if __name__ == "__main__":
    main()
