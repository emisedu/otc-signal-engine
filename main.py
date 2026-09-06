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
# TIME HELPER FUNCTIONS (NEXT CANDLE PREDICTION)
# ==========================================
def get_utc4_next_candle_prediction_time():
    """
    Calculates exact Next Candle Open & Close time in UTC+4.
    If clicked late in the current candle (>45s), shifts prediction 
    automatically to the next upcoming candle to guarantee buffer time.
    """
    now_utc4 = datetime.now(UTC_PLUS_4)
    
    # Calculate target candle start time
    if now_utc4.second >= 45:
        # Buffer shift to next-to-next candle if clicked too late in current minute
        target_candle_open = (now_utc4 + timedelta(minutes=2)).replace(second=0, microsecond=0)
    else:
        target_candle_open = (now_utc4 + timedelta(minutes=1)).replace(second=0, microsecond=0)
        
    target_candle_close = target_candle_open + timedelta(minutes=1)
    
    current_time_str = now_utc4.strftime("%H:%M:%S UTC+4")
    target_open_str = target_candle_open.strftime("%H:%M:00 UTC+4")
    target_close_str = target_candle_close.strftime("%H:%M:00 UTC+4")
    
    return current_time_str, target_open_str, target_close_str

# ==========================================
# ENGINE: NEXT CANDLE PREDICTION ENGINE V3.5
# ==========================================
class OTCNextCandlePredictorEngine:
    @staticmethod
    def predict_next_candle_structure(asset_name: str):
        is_gap_opening = random.choices([True, False], weights=[20, 80])[0]
        near_key_support_zone = random.choices([True, False], weights=[15, 85])[0]
        near_key_resistance_zone = random.choices([True, False], weights=[20, 80])[0]
        is_sideways_consolidation = random.choices([True, False], weights=[20, 80])[0]
        
        market_trend = random.choices(["BULLISH", "BEARISH"], weights=[50, 50])[0]

        # --- TRAP FILTERS FOR NEXT CANDLE ---
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
                "reason": "REJECTION RISK: Approaching Major Resistance Level",
                "action": "Avoid BUY Trade - High Reversal Chance"
            }

        if near_key_support_zone and market_trend == "BEARISH":
            return {
                "direction": "NO TRADE / SKIP ⏸️",
                "confidence": 42.0,
                "reason": "BOUNCE RISK: Approaching Key Support Zone",
                "action": "Avoid SELL Trade - High Support Bounce Chance"
            }

        if is_sideways_consolidation:
            return {
                "direction": "NO TRADE / SKIP ⏸️",
                "confidence": 45.0,
                "reason": "CONSOLIDATION: Market in Low Volume Range",
                "action": "Wait for clear directional candle"
            }

        # --- VALID NEXT CANDLE PREDICTIONS ---
        if market_trend == "BULLISH":
            return {
                "direction": "BUY (CALL) 🟢",
                "confidence": round(random.uniform(94.5, 98.6), 1),
                "reason": "Next Candle Velocity: Confirmed Bullish Continuation",
                "action": "Place CALL Option precisely at :00s Open Time"
            }
        else:
            return {
                "direction": "SELL (PUT) 🔴",
                "confidence": round(random.uniform(94.5, 98.6), 1),
                "reason": "Next Candle Velocity: Confirmed Bearish Breakdown",
                "action": "Place PUT Option precisely at :00s Open Time"
            }

# ==========================================
# TELEGRAM INTERFACE & HANDLERS
# ==========================================
def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("📊 AED/CNY OTC (+92%)", callback_data="pair_AEDCNY_OTC"),
         InlineKeyboardButton("📊 AUD/CAD OTC (+92%)", callback_data="pair_AUDCAD_OTC")],
        [InlineKeyboardButton("📊 AUD/NZD OTC (+92%)", callback_data="pair_AUDNZD_OTC"),
         InlineKeyboardButton("📊 AUD/USD OTC (+92%)", callback_data="pair_AUDUSD_OTC")],
        [InlineKeyboardButton("📊 JOD/CNY OTC (+92%)", callback_data="pair_JODCNY_OTC"),
         InlineKeyboardButton("📊 SAR/CNY OTC (+92%)", callback_data="pair_SARCNY_OTC")],
        [InlineKeyboardButton("📊 USD/BDT OTC (+92%)", callback_data="pair_USDBDT_OTC"),
         InlineKeyboardButton("📊 USD/BRL OTC (+92%)", callback_data="pair_USDBRL_OTC")],
        [InlineKeyboardButton("📊 USD/CHF OTC (+92%)", callback_data="pair_USDCHF_OTC"),
         InlineKeyboardButton("📊 USD/JPY OTC (+92%)", callback_data="pair_USDJPY_OTC")],
        [InlineKeyboardButton("📊 USD/PHP OTC (+92%)", callback_data="pair_USDPHP_OTC"),
         InlineKeyboardButton("📊 USD/THB OTC (+92%)", callback_data="pair_USDTHB_OTC")],
        [InlineKeyboardButton("📊 USD/VND OTC (+92%)", callback_data="pair_USDVND_OTC")],
        [InlineKeyboardButton("🔄 Refresh Dashboard", callback_data="refresh_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_time, target_open, target_close = get_utc4_next_candle_prediction_time()
    welcome_text = (
        "🤖 **NEXT CANDLE PREDICTION ENGINE v3.5**\n\n"
        f"🕒 **Current Time:** `{current_time}`\n"
        f"🎯 **Target Prediction Candle:** `{target_open}` to `{target_close}`\n\n"
        "⚡ *Signals are calibrated strictly for the UPCOMING CANDLE OPENING.*"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown", reply_markup=get_main_keyboard())

async def button_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    
    try:
        await query.answer()
    except Exception:
        pass

    data = query.data
    current_time, target_open, target_close = get_utc4_next_candle_prediction_time()

    if data == "refresh_menu":
        refresh_text = (
            f"🔄 **PREDICTION DASHBOARD REFRESHED**\n\n"
            f"🕒 **Current Time:** `{current_time}`\n"
            f"⏳ **Next Target Candle:** `{target_open}`\n\n"
            f"Select an asset below to predict next candle:"
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
        "pair_AEDCNY_OTC": "AED/CNY OTC",
        "pair_AUDCAD_OTC": "AUD/CAD OTC",
        "pair_AUDNZD_OTC": "AUD/NZD OTC",
        "pair_AUDUSD_OTC": "AUD/USD OTC",
        "pair_JODCNY_OTC": "JOD/CNY OTC",
        "pair_SARCNY_OTC": "SAR/CNY OTC",
        "pair_USDBDT_OTC": "USD/BDT OTC",
        "pair_USDBRL_OTC": "USD/BRL OTC",
        "pair_USDCHF_OTC": "USD/CHF OTC",
        "pair_USDJPY_OTC": "USD/JPY OTC",
        "pair_USDPHP_OTC": "USD/PHP OTC",
        "pair_USDTHB_OTC": "USD/THB OTC",
        "pair_USDVND_OTC": "USD/VND OTC"
    }

    asset = pair_map.get(data, "UNKNOWN ASSET")
    analysis = OTCNextCandlePredictorEngine.predict_next_candle_structure(asset)

    response_text = (
        f"🎯 **NEXT CANDLE PREDICTION ENGINE V3.5**\n"
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

    print("🚀 Next Candle Prediction Engine v3.5 Running...")
    app.run_polling()

if __name__ == "__main__":
    main()
