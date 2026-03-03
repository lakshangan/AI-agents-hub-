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
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def run(self, raw_text: str) -> List[Transaction]:
        self.log("Converting raw statement into structured data...")
        
        prompt = f"""
        Extract transactions from this text and return a JSON list of objects with keys:
        'date', 'description', 'amount' (float), 'is_subscription' (boolean).
        Text: {raw_text}
        ONLY return JSON:
        """
        
        try:
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            # Remove any markdown formatting (like ```json ... ```)
            text_data = response.text.strip().replace("```json", "").replace("```", "")
            data = json.loads(text_data)
            
            transactions = [Transaction(**item) for item in data]
            self.log(f"Parser extracted {len(transactions)} transactions.")
            return transactions
        except Exception as e:
            self.error(f"Parsing Failed: {e}")
            return []
