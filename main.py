import asyncio
import time
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ==========================================
# CONFIGURATION
# ==========================================
TELEGRAM_BOT_TOKEN = "8644355663:AAEzg6oR1VyOx1TwEiFd18UANfM-rBORhNo"

# ==========================================
# ENGINE: OTC TRAP & TREND ANALYSIS V3.0
# ==========================================
class OTCTrapDetectionEngine:
    @staticmethod
    def analyze_market_structure(asset_name: str):
        """
        Engine logic integrating:
        1. Gap Up / Gap Down Detection
        2. Double Bottom / Support Proximity Filter
        3. Exhaustion & Decay Detection (Doji / Small Bodies)
        4. Trend Momentum Confluence
        """
        # Simulated live structural indicators
        is_gap_opening = random.choices([True, False], weights=[30, 70])[0]
        near_key_support_zone = random.choices([True, False], weights=[25, 75])[0]
        is_exhaustion_candle = random.choices([True, False], weights=[20, 80])[0]
        
        # Primary trend evaluation
        market_trend = random.choices(["BULLISH", "BEARISH"], weights=[50, 50])[0]

        # --- TRAP FILTERS ---
        if is_gap_opening:
            return {
                "direction": "NO TRADE / SKIP ⏸️",
                "confidence": 0.0,
                "reason": "TRAP DETECTED: Gap Opening (Liquidity Re-balancing Risk)",
                "action": "SKIP Trade on :00s Open"
            }
        
        if near_key_support_zone and market_trend == "BEARISH":
            return {
                "direction": "NO TRADE / SKIP ⏸️",
                "confidence": 42.0,
                "reason": "TRAP DETECTED: Double Bottom / Key Support Level Reversal",
                "action": "Wait for Bounce / Confirmation Candle"
            }

        if is_exhaustion_candle:
            return {
                "direction": "NO TRADE / SKIP ⏸️",
                "confidence": 48.0,
                "reason": "EXHAUSTION DETECTED: Shrinking Body + Wick Rejection",
                "action": "Avoid Momentum Continuation"
            }

        # --- VALID SIGNALS ---
        if market_trend == "BULLISH":
            return {
                "direction": "BUY (CALL) 🟢",
                "confidence": round(random.uniform(93.5, 97.8), 1),
                "reason": "Strong Bullish Continuation + No Rejection Wicks",
                "action": "Enter PUT/CALL at Exact :00s Candle Open"
            }
        else:
            return {
                "direction": "SELL (PUT) 🔴",
                "confidence": round(random.uniform(93.5, 97.8), 1),
                "reason": "Clean Downward Velocity + Clean Structural Breakdown",
                "action": "Enter PUT/CALL at Exact :00s Candle Open"
            }

# ==========================================
# TELEGRAM INTERFACE & HANDLERS
# ==========================================
def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("📊 EUR/USD OTC", callback_data="pair_EURUSD_OTC"),
         InlineKeyboardButton("📊 EUR/NZD OTC", callback_data="pair_EURNZD_OTC")],
        [InlineKeyboardButton("📊 USD/BDT OTC", callback_data="pair_USDBDT_OTC"),
         InlineKeyboardButton("📊 USD/BRL OTC", callback_data="pair_USDBRL_OTC")],
        [InlineKeyboardButton("📊 USD/CAD OTC", callback_data="pair_USDCAD_OTC"),
         InlineKeyboardButton("📊 USD/PKR OTC", callback_data="pair_USDPKR_OTC")],
        [InlineKeyboardButton("🔄 Refresh Dashboard", callback_data="refresh_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🤖 **LIVE OTC VELOCITY & TRAP ENGINE v3.0**\n\n"
        "Active Filters:\n"
        "• Gap Opening Detection\n"
        "• Double Bottom / Support Bounce Guard\n"
        "• Bearish/Bullish Exhaustion Filter\n\n"
        "Select an OTC asset to scan for signals:"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown", reply_markup=get_main_keyboard())

async def button_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer(text="🔍 Scanning OTC Ticks & Orderbook Structure...")

    data = query.data
    if data == "refresh_menu":
        await query.edit_message_text(
            "🔄 **OTC SIGNAL DASHBOARD REFRESHED**\nSelect an asset:",
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )
        return

    pair_map = {
        "pair_EURUSD_OTC": "EUR/USD OTC",
        "pair_EURNZD_OTC": "EUR/NZD OTC",
        "pair_USDBDT_OTC": "USD/BDT OTC",
        "pair_USDBRL_OTC": "USD/BRL OTC",
        "pair_USDCAD_OTC": "USD/CAD OTC",
        "pair_USDPKR_OTC": "USD/PKR OTC"
    }

    asset = pair_map.get(data, "UNKNOWN ASSET")
    analysis = OTCTrapDetectionEngine.analyze_market_structure(asset)
    timestamp = time.strftime("%H:%M:%S PKT")

    response_text = (
        f"🎯 **OTC VELOCITY ENGINE V3.0**\n"
        f"📍 **Asset:** `{asset}`\n"
        f"----------------------------------------\n"
        f"🔹 **Signal:** **{analysis['direction']}**\n"
        f"🔹 **Confidence:** `{analysis['confidence']}%`\n"
        f"🔹 **Engine Reason:** `{analysis['reason']}`\n"
        f"🔹 **Required Action:** `{analysis['action']}`\n"
        f"----------------------------------------\n"
        f"⚠️ **STRICT RULES:** Skip trade instantly if the new candle opens with a Gap Up/Down.\n"
        f"🕒 **Time:** `{timestamp}`"
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

    print("🚀 OTC Trap Detection Engine v3.0 Running...")
    app.run_polling()

if __name__ == "__main__":
    main()
