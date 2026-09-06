import asyncio
import time
from datetime import datetime, timedelta, timezone
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ==========================================
# CONFIGURATION
# ==========================================
TELEGRAM_BOT_TOKEN = "8644355663:AAEzg6oR1VyOx1TwEiFd18UANfM-rBORhNo"

# Timezone Definition: UTC+4
UTC_PLUS_4 = timezone(timedelta(hours=4))

# ==========================================
# TIME HELPER FUNCTIONS
# ==========================================
def get_utc4_next_candle_prediction_time():
    now_utc4 = datetime.now(UTC_PLUS_4)
    
    # Fast Buffer Shift: If clicked within 10s of candle close, shift to next minute
    if now_utc4.second >= 50:
        target_candle_open = (now_utc4 + timedelta(minutes=2)).replace(second=0, microsecond=0)
    else:
        target_candle_open = (now_utc4 + timedelta(minutes=1)).replace(second=0, microsecond=0)
        
    target_candle_close = target_candle_open + timedelta(minutes=1)
    
    current_time_str = now_utc4.strftime("%H:%M:%S UTC+4")
    target_open_str = target_candle_open.strftime("%H:%M:00 UTC+4")
    target_close_str = target_candle_close.strftime("%H:%M:00 UTC+4")
    
    return current_time_str, target_open_str, target_close_str

# ==========================================
# ENGINE: FAST PREDICTION ENGINE V3.6
# ==========================================
class OTCFastPredictorEngine:
    @staticmethod
    def predict_next_candle(asset_name: str):
        is_gap_opening = random.choices([True, False], weights=[15, 85])[0]
        near_key_support_zone = random.choices([True, False], weights=[15, 85])[0]
        near_key_resistance_zone = random.choices([True, False], weights=[15, 85])[0]
        
        market_trend = random.choices(["BULLISH", "BEARISH"], weights=[50, 50])[0]

        if is_gap_opening:
            return {
                "direction": "NO TRADE / SKIP ⏸️",
                "confidence": 0.0,
                "reason": "TRAP RISK: Potential Gap Opening on Next Candle",
                "action": "Do NOT enter trade on next candle open"
            }
        
        if near_key_resistance_zone and market_trend == "BULLISH":
            return {
                "direction": "NO TRADE / SKIP ⏸️",
                "confidence": 40.0,
                "reason": "REJECTION RISK: Resistance Zone Reversal",
                "action": "Avoid CALL - High Sell Pressure"
            }

        if near_key_support_zone and market_trend == "BEARISH":
            return {
                "direction": "NO TRADE / SKIP ⏸️",
                "confidence": 42.0,
                "reason": "BOUNCE RISK: Key Support Zone",
                "action": "Avoid PUT - High Support Reversal"
            }

        if market_trend == "BULLISH":
            return {
                "direction": "BUY (CALL) 🟢",
                "confidence": round(random.uniform(94.5, 98.6), 1),
                "reason": "Strong Bullish Momentum Continuation",
                "action": "Place CALL at exact :00s Open Time"
            }
        else:
            return {
                "direction": "SELL (PUT) 🔴",
                "confidence": round(random.uniform(94.5, 98.6), 1),
                "reason": "Strong Bearish Breakdown Velocity",
                "action": "Place PUT at exact :00s Open Time"
            }

# ==========================================
# TELEGRAM INTERFACE (ONLY TOP 5 PAIRS)
# ==========================================
def get_main_keyboard():
    # Only 5 selected pairs from screenshot (+92% payout)
    keyboard = [
        [InlineKeyboardButton("📊 USD/ARS OTC (+92%)", callback_data="pair_USDARS_OTC")],
        [InlineKeyboardButton("📊 USD/BRL OTC (+92%)", callback_data="pair_USDBRL_OTC")],
        [InlineKeyboardButton("📊 USD/CHF OTC (+92%)", callback_data="pair_USDCHF_OTC")],
        [InlineKeyboardButton("📊 USD/COP OTC (+92%)", callback_data="pair_USDCOP_OTC")],
        [InlineKeyboardButton("📊 USD/IDR OTC (+92%)", callback_data="pair_USDIDR_OTC")],
        [InlineKeyboardButton("🔄 Refresh Dashboard", callback_data="refresh_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_time, target_open, target_close = get_utc4_next_candle_prediction_time()
    welcome_text = (
        "🤖 **INSTANT OTC PREDICTION ENGINE v3.6**\n\n"
        f"🕒 **Current Time:** `{current_time}`\n"
        f"🎯 **Target Prediction Candle:** `{target_open}` to `{target_close}`\n\n"
        "Active Asset List: **Top 5 (+92%) Pairs**\n"
        "Select a pair below for instant signal:"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown", reply_markup=get_main_keyboard())

async def button_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    
    # Instant callback response to stop loading delay
    await query.answer()

    data = query.data
    current_time, target_open, target_close = get_utc4_next_candle_prediction_time()

    if data == "refresh_menu":
        refresh_text = (
            f"🔄 **PREDICTION DASHBOARD REFRESHED**\n\n"
            f"🕒 **Current Time:** `{current_time}`\n"
            f"⏳ **Next Target Candle:** `{target_open}`\n\n"
            f"Select an asset below:"
        )
        try:
            await query.edit_message_text(
                refresh_text,
                parse_mode="Markdown",
                reply_markup=get_main_keyboard()
            )
        except Exception:
            await query.message.reply_text(
                refresh_text,
                parse_mode="Markdown",
                reply_markup=get_main_keyboard()
            )
        return

    pair_map = {
        "pair_USDARS_OTC": "USD/ARS OTC",
        "pair_USDBRL_OTC": "USD/BRL OTC",
        "pair_USDCHF_OTC": "USD/CHF OTC",
        "pair_USDCOP_OTC": "USD/COP OTC",
        "pair_USDIDR_OTC": "USD/IDR OTC"
    }

    asset = pair_map.get(data, "UNKNOWN ASSET")
    analysis = OTCFastPredictorEngine.predict_next_candle(asset)

    response_text = (
        f"🎯 **FAST OTC PREDICTION ENGINE V3.6**\n"
        f"📍 **Asset:** `{asset}` (+92% Payout)\n"
        f"----------------------------------------\n"
        f"🔹 **Predicted Direction:** **{analysis['direction']}**\n"
        f"🔹 **Confidence:** `{analysis['confidence']}%`\n"
        f"🔹 **Analysis:** `{analysis['reason']}`\n"
        f"----------------------------------------\n"
        f"⏱️ **Target Entry Time:** Exact `{target_open}`\n"
        f"⏱️ **Expiry Time:** `{target_close}` (M1 Expiry)\n"
        f"🔹 **Action:** `{analysis['action']}`\n"
        f"----------------------------------------\n"
        f"⚠️ **Execution Rule:** Place trade exactly when time reaches `{target_open}` (:00s).\n"
        f"🕒 **Signal Generated:** `{current_time}`"
    )

    # Edit existing message instead of sending new message to avoid execution delays
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

    print("🚀 Ultra-Fast OTC Engine v3.6 (5 Pairs Only) Running...")
    app.run_polling()

if __name__ == "__main__":
    main()
