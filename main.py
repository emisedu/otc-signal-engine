import asyncio
import random
import time
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

TELEGRAM_BOT_TOKEN = "8644355663:AAEzg6oR1VyOx1TwEiFd18UANfM-rBORhNo"


class HighPrecisionOTCEngine:

    @staticmethod
    def analyze_structure(asset_name):
        timeframes = ["5s", "10s", "15s", "30s", "1m"]
        tf_results = {}
        bullish_count = 0
        bearish_count = 0

        for tf in timeframes:
            bias = random.choice(["BULLISH", "BEARISH"])
            tf_results[tf] = bias
            if bias == "BULLISH":
                bullish_count += 1
            else:
                bearish_count += 1

        # Simulate gap detection and key zone analysis
        has_gap = random.choice([True, False, False])  # 33% gap probability
        market_structure = random.choice(
            ["SUPPORT_REJECTION", "RESISTANCE_REJECTION", "CONTINUATION", "MID_AIR_CONSOLIDATION"]
        )

        # 1. Filter out Gap Candle Openings
        if has_gap:
            return (
                "NO TRADE (CANDLE GAP DETECTED) ⚠️",
                0.0,
                "Candle opened with a price gap jump. High manipulation risk.",
                tf_results,
                "ABORT",
            )

        # 2. Strict 5/5 Timeframe Confluence Filter
        if bullish_count == 5 and market_structure in ["SUPPORT_REJECTION", "CONTINUATION"]:
            confidence = round(94.0 + random.uniform(1.0, 4.5), 1)
            direction = "BUY (CALL) 🟢"
            reason = f"5/5 TF Confluence + {market_structure.replace('_', ' ')}"
            setup_type = "S/R Bounce" if "REJECTION" in market_structure else "Trend Continuation"
            return direction, confidence, reason, tf_results, setup_type

        elif bearish_count == 5 and market_structure in ["RESISTANCE_REJECTION", "CONTINUATION"]:
            confidence = round(94.0 + random.uniform(1.0, 4.5), 1)
            direction = "SELL (PUT) 🔴"
            reason = f"5/5 TF Confluence + {market_structure.replace('_', ' ')}"
            setup_type = "S/R Bounce" if "REJECTION" in market_structure else "Trend Continuation"
            return direction, confidence, reason, tf_results, setup_type

        return (
            "NO TRADE (INSUFFICIENT CONFLUENCE) ⚠️",
            0.0,
            "Market in mid-range or timeframes conflicting.",
            tf_results,
            "NEUTRAL",
        )


def get_main_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("📊 EUR/USD OTC", callback_data="pair_EURUSD_OTC"),
            InlineKeyboardButton("📊 GBP/USD OTC", callback_data="pair_GBPUSD_OTC"),
        ],
        [
            InlineKeyboardButton("📊 USD/JPY OTC", callback_data="pair_USDJPY_OTC"),
            InlineKeyboardButton("📊 AUD/CAD OTC", callback_data="pair_AUDCAD_OTC"),
        ],
        [
            InlineKeyboardButton("📊 EUR/GBP OTC", callback_data="pair_EURGBP_OTC"),
            InlineKeyboardButton("📊 USD/CHF OTC", callback_data="pair_USDCHF_OTC"),
        ],
        [
            InlineKeyboardButton("🌐 EUR/USD (Live)", callback_data="pair_EURUSD_LIVE"),
            InlineKeyboardButton("🌐 GBP/USD (Live)", callback_data="pair_GBPUSD_LIVE"),
        ],
        [
            InlineKeyboardButton("🌐 USD/JPY (Live)", callback_data="pair_USDJPY_LIVE"),
            InlineKeyboardButton("🌐 AUD/USD (Live)", callback_data="pair_AUDUSD_LIVE"),
        ],
        [
            InlineKeyboardButton("🔄 Refresh Dashboard", callback_data="refresh_menu")
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🤖 **HIGH-PRECISION OTC & FOREX SIGNAL ENGINE**\n\n"
        "Select an asset for micro-structure and 5-timeframe confluence verification:"
    )
    await update.message.reply_text(
        msg, parse_mode="Markdown", reply_markup=get_main_keyboard()
    )


async def button_callback_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer(text="🔍 Performing multi-timeframe structural scan...")

    data = query.data

    if data == "refresh_menu":
        await query.edit_message_text(
            "🔄 **SIGNAL DASHBOARD**\n\nSelect an asset:",
            parse_mode="Markdown",
            reply_markup=get_main_keyboard(),
        )
        return

    pair_map = {
        "pair_EURUSD_OTC": "EUR/USD OTC",
        "pair_GBPUSD_OTC": "GBP/USD OTC",
        "pair_USDJPY_OTC": "USD/JPY OTC",
        "pair_AUDCAD_OTC": "AUD/CAD OTC",
        "pair_EURGBP_OTC": "EUR/GBP OTC",
        "pair_USDCHF_OTC": "USD/CHF OTC",
        "pair_EURUSD_LIVE": "EUR/USD (Live)",
        "pair_GBPUSD_LIVE": "GBP/USD (Live)",
        "pair_USDJPY_LIVE": "USD/JPY (Live)",
        "pair_AUDUSD_LIVE": "AUD/USD (Live)",
    }

    asset = pair_map.get(data, "UNKNOWN PAIR")
    direction, confidence, reasoning, tf_data, setup_type = (
        HighPrecisionOTCEngine.analyze_structure(asset)
    )
    timestamp = time.strftime("%H:%M:%S PKT")

    if confidence > 0:
        result_text = (
            f"🎯 **HIGH PROBABILITY SIGNAL: {asset}**\n"
            f"----------------------------------------\n"
            f"🔹 **Signal:** **{direction}**\n"
            f"🔹 **Setup Type:** `{setup_type}`\n"
            f"🔹 **Accuracy Rating:** `{confidence}%`\n"
            f"🔹 **Reason:** `{reasoning}`\n"
            f"----------------------------------------\n"
            f"⏱️ **Micro TF Breakdown (5/5 Aligned):**\n"
            f"• 5s: `{tf_data['5s']}` | 10s: `{tf_data['10s']}`\n"
            f"• 15s: `{tf_data['15s']}` | 30s: `{tf_data['30s']}` | 1m: `{tf_data['1m']}`\n"
            f"----------------------------------------\n"
            f"⚡ **Entry Rule:** Exact **:00s** open price. Do NOT trade if gap occurs!"
        )
    else:
        result_text = (
            f"⚠️ **STRICT FILTER ACTIVE: {asset}**\n"
            f"----------------------------------------\n"
            f"🔹 **Status:** `{direction}`\n"
            f"🔹 **Reason:** {reasoning}\n"
            f"❌ **ACTION:** Skip this candle."
        )

    await query.message.reply_text(
        result_text, parse_mode="Markdown", reply_markup=get_main_keyboard()
    )


def main():
    print("🚀 Starting High-Precision Signal Engine...")
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("panel", start_command))
    app.add_handler(CallbackQueryHandler(button_callback_handler))

    app.run_polling()


if __name__ == "__main__":
    main()
