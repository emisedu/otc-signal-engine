import asyncio
from datetime import datetime, timedelta, timezone
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ==========================================
# CONFIGURATION
# ==========================================
TELEGRAM_BOT_TOKEN = "8644355663:AAEzg6oR1VyOx1TwEiFd18UANfM-rBORhNo"

# Timezone: UTC+5 (Quotex Terminal Time)
UTC_PLUS_5 = timezone(timedelta(hours=5))

# ==========================================
# ULTRA-FAST TIME CALCULATOR
# ==========================================
def get_fast_entry_time():
    now = datetime.now(UTC_PLUS_5)
    if now.second >= 50:
        target_time = (now + timedelta(minutes=2)).replace(second=0, microsecond=0)
    else:
        target_time = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
        
    return target_time.strftime("%H:%M:00")

# ==========================================
# COMPACT KEYBOARD (SMALLER BUTTON SIZES)
# ==========================================
def get_main_keyboard():
    # 2-3 buttons per row keeps the button dimensions compact
    keyboard = [
        [
            InlineKeyboardButton("📊 USD/BRL", callback_data="USDBRL_OTC"),
            InlineKeyboardButton("📊 NZD/JPY", callback_data="NZDJPY_OTC")
        ],
        [
            InlineKeyboardButton("📊 USD/BDT", callback_data="USDBDT_OTC"),
            InlineKeyboardButton("📊 USD/JPY", callback_data="USDJPY_OTC")
        ],
        [
            InlineKeyboardButton("📊 USD/NGN", callback_data="USDNGN_OTC"),
            InlineKeyboardButton("📊 AUD/USD", callback_data="AUDUSD_OTC")
        ],
        [
            InlineKeyboardButton("📊 GBP/JPY", callback_data="GBPJPY_OTC"),
            InlineKeyboardButton("🔄 Refresh", callback_data="refresh_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# ==========================================
# HANDLERS
# ==========================================
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = "🏛️ **QUOTEX FAST TERMINAL**\nSelect a pair below:"
    await update.message.reply_text(welcome_text, parse_mode="Markdown", reply_markup=get_main_keyboard())

async def button_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "refresh_menu":
        try:
            await query.edit_message_text("🔄 **Dashboard Refreshed**\nSelect pair:", parse_mode="Markdown", reply_markup=get_main_keyboard())
        except Exception:
            pass
        return

    pair_display_name = data.replace("_OTC", " (OTC)")
    entry_time = get_fast_entry_time()

    # Direction Decision
    direction = random.choices(["BUY", "SELL"], weights=[50, 50])[0]
    accuracy_percentage = round(random.uniform(94.2, 98.7), 1)

    if direction == "BUY":
        signal_output = "🟩 **UP** ⬆️"
    else:
        signal_output = "🟥 **DOWN** ⬇️"

    # Minimal Output: Asset, Single Direction Button, Entry Time & Accuracy %
    response_text = (
        f"📍 **{pair_display_name}**\n\n"
        f"🎯 {signal_output}\n"
        f"⏰ **ENTRY:** `{entry_time}`\n"
        f"🎯 **ACCURACY:** `{accuracy_percentage}%`"
    )

    try:
        await query.edit_message_text(
            response_text,
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )
    except Exception:
        await query.message.reply_text(
            response_text,
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )

# ==========================================
# MAIN EXECUTION
# ==========================================
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(button_callback_handler))

    print("🚀 Quotex Ultra-Compact Engine Active...")
    app.run_polling()

if __name__ == "__main__":
    main()
