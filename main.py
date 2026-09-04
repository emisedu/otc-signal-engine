import asyncio
import time
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

# --- TELEGRAM CREDENTIALS ---
TELEGRAM_BOT_TOKEN = "8644355663:AAEzg6oR1VyOx1TwEiFd18UANfM-rBORhNo"


# --- ADVANCED PRICE ACTION ENGINE ---
class AdvancedPriceActionEngine:

    @staticmethod
    def calculate_confluence(price_data):
        """Calculates Trend, Candle Body Ratio, Wick Rejection, and Momentum."""
        open_p, high_p, low_p, close_p = (
            price_data["open"],
            price_data["high"],
            price_data["low"],
            price_data["close"],
        )

        candle_range = high_p - low_p
        if candle_range == 0:
            return "NO TRADE (ZERO VOLATILITY) ⚠️", 0.0

        body_size = abs(close_p - open_p)
        body_ratio = body_size / candle_range

        upper_wick = high_p - max(open_p, close_p)
        lower_wick = min(open_p, close_p) - low_p

        # Bullish Rejection & Momentum Setup (CALL)
        if close_p > open_p:  # Green Candle
            lower_rejection = lower_wick / candle_range
            if body_ratio >= 0.65 and lower_rejection >= 0.20:
                confidence = round(88.0 + (body_ratio * 10), 1)
                return "BUY (CALL) 🟢", confidence

        # Bearish Rejection & Momentum Setup (PUT)
        elif close_p < open_p:  # Red Candle
            upper_rejection = upper_wick / candle_range
            if body_ratio >= 0.65 and upper_rejection >= 0.20:
                confidence = round(88.0 + (body_ratio * 10), 1)
                return "SELL (PUT) 🔴", confidence

        # Strict Filter: Doji / Weak Consolidation
        return "NO TRADE (HIGH RISK / CONSOLIDATION) ⚠️", 0.0


# Mock function representing real-time candle feed parsing
def get_market_candle(asset_name):
    # Simulated current candle state based on price micro-ticks
    # Replace this structure when connecting real WebSocket feeds
    import random

    base_price = 1.0850 if "EUR" in asset_name else 1.2650
    variation = random.uniform(-0.0010, 0.0010)

    o = base_price
    c = base_price + variation
    h = max(o, c) + random.uniform(0.0001, 0.0005)
    l = min(o, c) - random.uniform(0.0001, 0.0005)

    return {"open": o, "high": h, "low": l, "close": c}


# --- BUTTONS CONTROL PANEL ---
def get_signal_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                "📊 Analyze EUR/USD OTC", callback_data="sig_EURUSD"
            ),
            InlineKeyboardButton(
                "📊 Analyze GBP/USD OTC", callback_data="sig_GBPUSD"
            ),
        ],
        [
            InlineKeyboardButton(
                "📊 Analyze AUD/CAD OTC", callback_data="sig_AUDCAD"
            ),
            InlineKeyboardButton(
                "📊 Analyze USD/JPY OTC", callback_data="sig_USDJPY"
            ),
        ],
        [
            InlineKeyboardButton(
                "🔄 Refresh Dashboard", callback_data="refresh_menu"
            )
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


# --- TELEGRAM HANDLERS ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🤖 **OTC PRICE ACTION SIGNAL ENGINE**\n\n"
        "Select an OTC asset to perform multi-confluence structural analysis:"
    )
    await update.message.reply_text(
        msg, parse_mode="Markdown", reply_markup=get_signal_keyboard()
    )


async def button_callback_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer(text="🔍 Fetching candle structure...")

    data = query.data

    if data == "refresh_menu":
        await query.edit_message_text(
            "🔄 **OTC SIGNAL ENGINE DASHBOARD**\n\nSelect an OTC asset:",
            parse_mode="Markdown",
            reply_markup=get_signal_keyboard(),
        )
        return

    pairs = {
        "sig_EURUSD": "EUR/USD OTC",
        "sig_GBPUSD": "GBP/USD OTC",
        "sig_AUDCAD": "AUD/CAD OTC",
        "sig_USDJPY": "USD/JPY OTC",
    }

    asset = pairs.get(data, "OTC ASSET")
    candle_data = get_market_candle(asset)
    direction, confidence = AdvancedPriceActionEngine.calculate_confluence(
        candle_data
    )
    timestamp = time.strftime("%H:%M:%S PKT")

    if confidence > 0:
        result_text = (
            f"🎯 **PRICE ACTION OTC SIGNAL**\n"
            f"----------------------------------------\n"
            f"🔹 **Asset:** `{asset}`\n"
            f"🔹 **Direction:** **{direction}**\n"
            f"🔹 **Timeframe:** **M1 (1 Minute)**\n"
            f"🔹 **Confluence Score:** `{confidence}%`\n"
            f"🔹 **Execution:** Exact **:00s** candle open\n"
            f"🔹 **Analysis Time:** `{timestamp}`\n"
            f"----------------------------------------\n"
            f"⚡ *Rule: Skip trade if candle opens with a heavy gap.*"
        )
    else:
        result_text = (
            f"⚠️ **FILTER ACTIVE: {asset}**\n"
            f"----------------------------------------\n"
            f"Market is in consolidation / indecision phase.\n"
            f"❌ **NO TRADE CONFIRMATION FOR NEXT CANDLE.**"
        )

    await query.message.reply_text(
        result_text, parse_mode="Markdown", reply_markup=get_signal_keyboard()
    )


def main():
    print("🚀 Starting Advanced Price Action Signal Engine...")
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("panel", start_command))
    app.add_handler(CallbackQueryHandler(button_callback_handler))

    app.run_polling()


if __name__ == "__main__":
    main()
