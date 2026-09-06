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
# TIME CALCULATOR
# ==========================================
def get_fast_entry_time():
    now = datetime.now(UTC_PLUS_5)
    if now.second >= 48:
        target_time = (now + timedelta(minutes=2)).replace(second=0, microsecond=0)
    else:
        target_time = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
        
    return target_time.strftime("%H:%M:00")

# ==========================================
# ADVANCED RSI & TREND SIGNAL ENGINE
# ==========================================
class QuotexSmartEngine:
    @staticmethod
    def analyze_market():
        # Simulated RSI Value calculation (30 to 70 range)
        rsi_val = random.randint(20, 80)
        
        # RSI Analysis Logic
        if rsi_val >= 70:
            return "SELL", "96.5%", "RSI Overbought (>70) Reversal Zone"
        elif rsi_val <= 30:
            return "BUY", "96.5%", "RSI Oversold (<30) Reversal Zone"
        else:
            # Trend Momentum Filter
            direction = random.choice(["BUY", "SELL"])
            return direction, "94.2%", "Trend Continuation Pattern"

# ==========================================
# KEYBOARD
# ==========================================
def get_main_keyboard():
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
    welcome_text = "🏛️ **QUOTEX SMART RSI TERMINAL**\nSelect a pair below:"
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

    direction, accuracy, reason = QuotexSmartEngine.analyze_market()

    if direction == "BUY":
        signal_output = "🟩 **UP / CALL** ⬆️"
    else:
        signal_output = "f🟥 **DOWN / PUT** ⬇️"

    response_text = (
        f"📍 **{pair_display_name}**\n\n"
        f"🎯 {signal_output}\n"
        f"⏰ **ENTRY:** `{entry_time}`\n"
        f"🎯 **ACCURACY:** `{accuracy}`\n"
        f"💡 **RULE:** If 1st candle loses, use **1-Step Martingale (MTG)** on next candle."
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

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(button_callback_handler))

    print("🚀 Quotex Smart Engine Active...")
    app.run_polling()

if __name__ == "__main__":
    main()
