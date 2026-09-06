import random

class GapAndLiquidityTrapEngine:
    @staticmethod
    def evaluate_candle_trap(is_gap_down, near_equal_lows, body_size_decay):
        """
        Detects OTC Gap Manipulations and Equal Low Liquidity Sweeps
        """
        if is_gap_down and near_equal_lows:
            return {
                "signal": "NO TRADE / WAIT ⏸️",
                "reason": "TRAP: Gap Down at Equal Lows (Reverse Liquidity Sweep Risk)",
                "confidence": 40.0
            }
        elif body_size_decay and is_gap_down:
            return {
                "signal": "NO TRADE / WAIT ⏸️",
                "reason": "TRAP: Bearish Exhaustion + Gap Down Reversal",
                "confidence": 45.0
            }
        else:
            return {
                "signal": "PUT / SELL 🔴",
                "reason": "Clean Momentum Continuation",
                "confidence": 94.5
            }
