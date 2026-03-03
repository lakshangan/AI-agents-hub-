import asyncio
from typing import List
import google.generativeai as genai
import os
import json
from core.base import BaseAgent
from core.schemas.expense import Transaction

class StatementParserAgent(BaseAgent):
    def __init__(self):
        super().__init__("StatementParser")
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def run(self, raw_text: str) -> List[Transaction]:
        self.log("Converting raw statement into structured data...")
        
        # 1. Try AI first
        try:
            prompt = f"Extract transactions into JSON (date, description, amount, is_subscription) from: {raw_text}"
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            text_data = response.text.strip().replace("```json", "").replace("```", "")
            data = json.loads(text_data)
            return [Transaction(**item) for item in data]
        except Exception as e:
            self.error("AI Parsing Failed. Switching to Synthetic Mode...")
            return self._synthetic_parse(raw_text)

    def _synthetic_parse(self, text: str) -> List[Transaction]:
        transactions = []
        lines = text.split('\n')
        for line in lines:
            if ',' in line and any(char.isdigit() for char in line):
                parts = line.split(',')
                if len(parts) >= 3:
                    try:
                        # Detect Amount: look for numbers like 14.99 or 6.50
                        desc = parts[1].strip()
                        amt_str = parts[2].strip().replace("$", "").replace(",", "")
                        amt = float(amt_str) if amt_str else 0.0
                        
                        transactions.append(Transaction(
                            date=parts[0].strip(),
                            description=desc,
                            amount=amt,
                            is_subscription=any(kw in desc.upper() for kw in ["SUBSCRIPTION", "PREMIUM", "MONTHLY", "PLUS"])
                        ))
                    except: continue
        return transactions
