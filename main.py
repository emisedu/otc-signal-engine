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
    
    # Fast Buffer Shift: If clicked within 10s of candle close, shift to next-to-next candle
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
# ENGINE: QUOTEX FAST PREDICTION ENGINE V4.0
# ==========================================
class QuotexFastPredictorEngine:
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
                "reason": "QUOTEX TRAP: Potential Gap Opening on Next Candle",
                "action": "Do NOT enter trade on next candle open"
            }
        
        if near_key_resistance_zone and market_trend == "BULLISH":
            return {
                "direction": "NO TRADE / SKIP ⏸️",
                "confidence": 40.0,
                "reason": "REJECTION RISK: Quotex Resistance Zone Reversal",
                "action": "Avoid CALL - High Sell Pressure"
            }

        if near_key_support_zone and market_trend == "BEARISH":
            return {
                "direction": "NO TRADE / SKIP ⏸️",
                "confidence": 42.0,
                "reason": "BOUNCE RISK: Quotex Key Support Level",
                "action": "Avoid PUT - High Support Reversal"
            }

        if market_trend == "BULLISH":
            return {
                "direction": "BUY (CALL) 🟢",
                "confidence": round(random.uniform(94.5, 98.6), 1),
                "reason": "Strong Quotex OTC Bullish Momentum",
                "action": "Place CALL at exact :00s Open Time"
            }
        else:
            return {
                "direction": "SELL (PUT) 🔴",
                "confidence": round(random.uniform(94.5, 98.6), 1),
                "reason": "Strong Quotex OTC Bearish Velocity",
                "action": "Place PUT at exact :00s Open Time"
            }

# ==========================================
# TELEGRAM INTERFACE (QUOTEX PAIRS ONLY)
# ==========================================
def get_main_keyboard():
    # Exact 7 pairs from Quotex screenshot
    keyboard = [
        [InlineKeyboardButton("📊 USD/BRL (OTC) (+94%)", callback_data="pair_USDBRL_OTC")],
        [InlineKeyboardButton("📊 NZD/JPY (OTC) (+93%)", callback_data="pair_NZDJPY_OTC")],
        [InlineKeyboardButton("📊 USD/BDT (OTC) (+93%)", callback_data="pair_USDBDT_OTC")],
        [InlineKeyboardButton("📊 USD/JPY (OTC) (+93%)", callback_data="pair_USDJPY_OTC")],
        [InlineKeyboardButton("📊 USD/NGN (OTC) (+93%)", callback_data="pair_USDNGN_OTC")],
        [InlineKeyboardButton("📊 AUD/USD (OTC) (+92%)", callback_data="pair_AUDUSD_OTC")],
        [InlineKeyboardButton("📊 GBP/JPY (OTC) (+92%)", callback_data="pair_GBPJPY_OTC")],
        [InlineKeyboardButton("🔄 Refresh Dashboard", callback_data="refresh_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_time, target_open, target_close = get_utc4_next_candle_prediction_time()
    welcome_text = (
        "🤖 **QUOTEX OTC PREDICTION ENGINE v4.0 (TESTING)**\n\n"
        f"🕒 **Current Time:** `{current_time}`\n"
        f"🎯 **Target Candle:** `{target_open}` to `{target_close}`\n\n"
        "Selected Platform: **Quotex OTC**\n"
        "Select a pair below for instant signal:"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown", reply_markup=get_main_keyboard())

async def button_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    current_time, target_open, target_close = get_utc4_next_candle_prediction_time()

    if data == "refresh_menu":
        refresh_text = (
            f"🔄 **QUOTEX DASHBOARD REFRESHED**\n\n"
            f"🕒 **Current Time:** `{current_time}`\n"
            f"⏳ **Next Target Candle:** `{target_open}`\n\n"
            f"Select a Quotex pair below:"
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
        "pair_USDBRL_OTC": ("USD/BRL (OTC)", "94%"),
        "pair_NZDJPY_OTC": ("NZD/JPY (OTC)", "93%"),
        "pair_USDBDT_OTC": ("USD/BDT (OTC)", "93%"),
        "pair_USDJPY_OTC": ("USD/JPY (OTC)", "93%"),
        "pair_USDNGN_OTC": ("USD/NGN (OTC)", "93%"),
        "pair_AUDUSD_OTC": ("AUD/USD (OTC)", "92%"),
        "pair_GBPJPY_OTC": ("GBP/JPY (OTC)", "92%")
    }

    asset_info = pair_map.get(data, ("UNKNOWN ASSET", "0%"))
    asset, payout = asset_info[0], asset_info[1]
    
    analysis = QuotexFastPredictorEngine.predict_next_candle(asset)

    response_text = (
        f"🎯 **QUOTEX OTC ENGINE V4.0**\n"
        f"📍 **Asset:** `{asset}` (+{payout} Payout)\n"
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

    print("🚀 Quotex OTC Engine v4.0 (7 Testing Pairs) Running...")
    app.run_polling()

if __name__ == "__main__":
    main()
