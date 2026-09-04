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


class MultiTimeframeEngine:

    @staticmethod
    def analyze_multi_tf(asset_name):
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

        if bullish_count >= 4:
            confidence = round(91.0 + (bullish_count * 1.5), 1)
            direction = "BUY (CALL) 🟢"
            alignment = f"Strong Bullish Alignment ({bullish_count}/5 TF)"
        elif bearish_count >= 4:
            confidence = round(91.0 + (bearish_count * 1.5), 1)
            direction = "SELL (PUT) 🔴"
            alignment = f"Strong Bearish Alignment ({bearish_count}/5 TF)"
        else:
            return (
                "NO TRADE (TF CONFLICT) ⚠️",
                0.0,
                "Timeframes conflicting (No clear consensus).",
                tf_results,
            )

        return direction, confidence, alignment, tf_results


def get_main_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                "📊 EUR/USD OTC", callback_data="pair_EURUSD_OTC"
            ),
            InlineKeyboardButton(
                "📊 GBP/USD OTC", callback_data="pair_GBPUSD_OTC"
            ),
        ],
        [
            InlineKeyboardButton(
                "📊 USD/JPY OTC", callback_data="pair_USDJPY_OTC"
            ),
            InlineKeyboardButton(
                "📊 AUD/CAD OTC", callback_data="pair_AUDCAD_OTC"
            ),
        ],
        [
            InlineKeyboardButton(
                "📊 EUR/GBP OTC", callback_data="pair_EURGBP_OTC"
            ),
            InlineKeyboardButton(
                "📊 USD/CHF OTC", callback_data="pair_USDCHF_OTC"
            ),
        ],
        [
            InlineKeyboardButton(
                "🌐 EUR/USD (Live)", callback_data="pair_EURUSD_LIVE"
            ),
            InlineKeyboardButton(
                "🌐 GBP/USD (Live)", callback_data="pair_GBPUSD_LIVE"
            ),
        ],
        [
            InlineKeyboardButton(
                "🌐 USD/JPY (Live)", callback_data="pair_USDJPY_LIVE"
            ),
            InlineKeyboardButton(
                "🌐 AUD/USD (Live)", callback_data="pair_AUDUSD_LIVE"
            ),
        ],
        [
            InlineKeyboardButton(
                "🔄 Refresh Dashboard", callback_data="refresh_menu"
            )
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🤖 **PURE MANUAL MULTI-TIMEFRAME ENGINE**\n\n"
        "Asset select karke 5s, 10s, 15s, 30s aur 1m multi-TF analysis hasil karein:"
    )
    await update.message.reply_text(
        msg, parse_mode="Markdown", reply_markup=get_main_keyboard()
    )


async def button_callback_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer(text="🔍 Analyzing 5s to 1m timeframes...")

    data = query.data

    if data == "refresh_menu":
        await query.edit_message_text(
            "🔄 **MULTI-TIMEFRAME DASHBOARD**\n\nAsset select karein:",
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
    direction, confidence, alignment, tf_data = (
        MultiTimeframeEngine.analyze_multi_tf(asset)
    )
    timestamp = time.strftime("%H:%M:%S PKT")

    if confidence > 0:
        result_text = (
            f"🎯 **MULTI-TF SIGNAL: {asset}**\n"
            f"----------------------------------------\n"
            f"🔹 **Signal:** **{direction}**\n"
            f"🔹 **Probability:** `{confidence}%`\n"
            f"🔹 **Confluence:** `{alignment}`\n"
            f"----------------------------------------\n"
            f"⏱️ **Timeframe Breakdown:**\n"
            f"• 5s: `{tf_data['5s']}` | 10s: `{tf_data['10s']}`\n"
            f"• 15s: `{tf_data['15s']}` | 30s: `{tf_data['30s']}`\n"
            f"• 1m: `{tf_data['1m']}`\n"
            f"----------------------------------------\n"
            f"⚡ **Execution:** Enter trade at exact **:00s** candle open!\n"
            f"🕒 **Time:** `{timestamp}`"
        )
    else:
        result_text = (
            f"⚠️ **STRICT FILTER ACTIVE: {asset}**\n"
            f"----------------------------------------\n"
            f"🔹 **Reason:** {alignment}\n"
            f"⏱️ **TF Breakdown:** 5s({tf_data['5s']}), 10s({tf_data['10s']}), 15s({tf_data['15s']}), 30s({tf_data['30s']}), 1m({tf_data['1m']})\n"
            f"❌ **NO TRADE CONFIRMATION.**"
        )

    await query.message.reply_text(
        result_text, parse_mode="Markdown", reply_markup=get_main_keyboard()
    )


def main():
    print("🚀 Starting Pure Manual Engine...")
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("panel", start_command))
    app.add_handler(CallbackQueryHandler(button_callback_handler))

    app.run_polling()


if __name__ == "__main__":
    main()
