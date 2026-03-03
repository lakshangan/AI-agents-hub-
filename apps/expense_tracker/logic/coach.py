import aiohttp
from typing import List
from core.base import BaseAgent
from core.schemas.expense import Transaction, FinancialInsight, ExpenseReport
import os
import asyncio

class FinancialCoachAgent(BaseAgent):
    def __init__(self, bot_token: str = None, chat_id: str = None):
        super().__init__("FinancialCoach")
        self.bot_token = bot_token or os.getenv("BOT_TOKEN")
        self.chat_id = chat_id or os.getenv("CHAT_ID")
        self.enabled = bool(self.bot_token and self.chat_id)

    async def run(self, input_data: dict) -> ExpenseReport:
        transactions = input_data.get("transactions", [])
        leaks = input_data.get("leaks", [])
        
        total_spent = sum(t.amount for t in transactions)
        top_leak = max(leaks, key=lambda x: x.impact_score) if leaks else None
        
        report = ExpenseReport(
            transactions=transactions,
            total_spent=total_spent,
            detected_leaks=leaks,
            top_leak=top_leak
        )
        
        self.log(f"Financial Report Created. Total Spent: {total_spent}")

        if self.enabled:
            await self._send_to_telegram(report)
        else:
            self.log("Broadcast disabled (No Telegram config).")

        return report

    async def _send_to_telegram(self, report: ExpenseReport):
        header = f"💰 *Hey Lakshan! Here's your Bank Briefing*\n" \
                 f"---------------------------------\n" \
                 f"💸 *Total Spending Detected:* ${report.total_spent:.2f}\n\n"
        
        # Leak Highlights
        leaks_section = "⚠️ *Watch Out For These 'Leaks':*\n"
        for leak in report.detected_leaks:
             leaks_section += f"🏷️ *{leak.category}*: {leak.summary}\n💡 _Suggestion: {leak.suggestion}_\n\n"

        if not report.detected_leaks:
            leaks_section = "✅ No major leaks found. Your spending looks clean!\n\n"

        close_section = "🚀 _I'll keep a sharp eye for more leaks._"
        full_message = header + leaks_section + close_section

        # Send via Telegram API
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": full_message,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as resp:
                    if resp.status == 200:
                        self.log("Financial Advisor message sent to Telegram!")
                    else:
                        rtext = await resp.text()
                        self.error(f"Telegram API Error ({resp.status}): {rtext}")
        except Exception as e:
            self.error(f"Failed to broadcast via Telegram: {e}")
