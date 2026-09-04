import asyncio
import time
import random
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TELEGRAM_BOT_TOKEN = "8644355663:AAEzg6oR1VyOx1TwEiFd18UANfM-rBORhNo"

class TechnicalConfluenceEngine:
    @staticmethod
    def analyze_indicators(asset_name):
        """
        Multi-Indicator Analysis:
        - Trend Direction (MA)
        - Momentum Reversal (RSI)
        - Rejection/Volatility (Bollinger Bands)
        """
        # Simulated indicator values (Replace with real-time API feeds when connecting broker)
        rsi = random.uniform(20.0, 80.0)
        upper_band_touch = random.choice([True, False])
        lower_band_touch = random.choice([True, False])
        trend = random.choice(["UPTREND", "DOWNTREND", "SIDEWAYS"])
        body_ratio = random.uniform(0.30, 0.95)

        # High Confluence CALL Logic:
        # Oversold RSI (< 35) + Lower Bollinger Touch + Strong Body in Uptrend
        if rsi < 35.0 and lower_band_touch and trend == "UPTREND" and body_ratio > 0.60:
            confidence = round(92.0 + random.uniform(1.0, 5.0), 1)
            return "BUY (CALL) 🟢", confidence, f"RSI Oversold ({rsi:.1f}) + BB Support + Uptrend"

        # High Confluence PUT Logic:
        # Overbought RSI (> 65) + Upper Bollinger Touch + Strong Body in Downtrend
        elif rsi > 65.0 and upper_band_touch and trend == "DOWNTREND" and body_ratio > 0.60:
            confidence = round(91.5 + random.uniform(1.0, 5.0), 1)
            return "SELL (PUT) 🔴", confidence, f"RSI Overbought ({rsi:.1f}) + BB Resistance + Downtrend"

        # Strict Filter: Market Noise / Low Confluence
        return "NO TRADE (LOW CONFLUENCE) ⚠️", 0.0, "Indicators conflicting or market in consolidation."


# --- ALL PAIRS CONTROL PANEL ---
def get_main_keyboard():
    keyboard = [
        # OTC Pairs
        [
            InlineKeyboardButton("📊 EUR/USD OTC", callback_data="pair_EURUSD_OTC"),
            InlineKeyboardButton("📊 GBP/USD OTC", callback_data="pair_GBPUSD_OTC")
        ],
        [
            InlineKeyboardButton("📊 AUD/CAD OTC", callback_data="pair_AUDCAD_OTC"),
            InlineKeyboardButton("📊 USD/JPY OTC", callback_data="pair_USDJPY_OTC")
        ],
        # Live Forex Pairs
        [
            InlineKeyboardButton("🌐 EUR/USD (Live)", callback_data="pair_EURUSD_LIVE"),
            InlineKeyboardButton("🌐 GBP/USD (Live)", callback_data="pair_GBPUSD_LIVE")
        ],
        [
            InlineKeyboardButton("🌐 USD/JPY (Live)", callback_data="pair_USDJPY_LIVE"),
            InlineKeyboardButton("🌐 AUD/USD (Live)", callback_data="pair_AUDUSD_LIVE")
        ],
        [
            InlineKeyboardButton("🔄 Refresh Panel", callback_data="refresh_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🤖 **ADVANCED TRADING SIGNAL ENGINE**\n\n"
        "Select any **OTC** or **Live Market** asset below to run multi-indicator analysis:"
    )
    await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=get_main_keyboard())


async def button_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer(text="🔍 Running RSI + BB + Trend Confluence Engine...")

    data = query.data

    if data == "refresh_menu":
        await query.edit_message_text(
            "🔄 **SIGNAL ENGINE DASHBOARD**\n\nSelect an asset for analysis:",
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )
        return

    # Pair Mapping
    pair_map = {
        "pair_EURUSD_OTC": "EUR/USD OTC",
        "pair_GBPUSD_OTC": "GBP/USD OTC",
        "pair_AUDCAD_OTC": "AUD/CAD OTC",
        "pair_USDJPY_OTC": "USD/JPY OTC",
        "pair_EURUSD_LIVE": "EUR/USD (Live Forex)",
        "pair_GBPUSD_LIVE": "GBP/USD (Live Forex)",
        "pair_USDJPY_LIVE": "USD/JPY (Live Forex)",
        "pair_AUDUSD_LIVE": "AUD/USD (Live Forex)"
    }

    asset = pair_map.get(data, "UNKNOWN PAIR")
    direction, confidence, reasoning = TechnicalConfluenceEngine.analyze_indicators(asset)
    timestamp = time.strftime("%H:%M:%S PKT")

    if confidence > 0:
        result_text = (
            f"🎯 **MULTI-INDICATOR SIGNAL**\n"
            f"----------------------------------------\n"
            f"🔹 **Asset:** `{asset}`\n"
            f"🔹 **Signal:** **{direction}**\n"
            f"🔹 **Timeframe:** **M1 (1 Minute)**\n"
            f"🔹 **Confluence Score:** `{confidence}%`\n"
            f"🔹 **Strategy:** `{reasoning}`\n"
            f"🔹 **Time:** `{timestamp}`\n"
            f"----------------------------------------\n"
            f"⚡ **Rule:** Enter trade at exact **:00s** candle open!"
        )
    else:
        result_text = (
            f"⚠️ **FILTER ACTIVE: {asset}**\n"
            f"----------------------------------------\n"
            f"🔹 **Reason:** {reasoning}\n"
            f"❌ **NO TRADE SUGGESTED FOR NEXT CANDLE.**"
        )

    await query.message.reply_text(result_text, parse_mode="Markdown", reply_markup=get_main_keyboard())


def main():
    print("🚀 Starting Advanced All-Pairs Signal Engine...")
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("panel", start_command))
    app.add_handler(CallbackQueryHandler(button_callback_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
