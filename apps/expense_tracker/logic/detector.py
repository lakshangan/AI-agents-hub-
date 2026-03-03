import asyncio
import os
import json
from typing import List
import google.generativeai as genai
from core.base import BaseAgent
from core.schemas.expense import Transaction, FinancialInsight

class LeakDetectorAgent(BaseAgent):
    def __init__(self):
        super().__init__("LeakDetector")
        self.api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def run(self, transactions: List[Transaction]) -> List[FinancialInsight]:
        self.log(f"Searching for 'leaks' in {len(transactions)} items...")
        
        # Prepare data for model
        tx_data = [tx.dict() for tx in transactions]
        
        prompt = f"""
        Identify at least 2 money 'leaks' from this data.
        A 'leak' is:
        - A subscription you can do without.
        - High-frequency small charges (like coffee, snacks) that add up.
        - High transaction fees or sudden amount hikes.
        
        Return a JSON list of objects with:
        'category', 'summary', 'impact_score' (0.1 to 1.0), 'suggestion'.
        Data: {json.dumps(tx_data)}
        ONLY return JSON:
        """
        
        try:
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            text_data = response.text.strip().replace("```json", "").replace("```", "")
            data = json.loads(text_data)
            
            insights = [FinancialInsight(**item) for item in data]
            self.log(f"Identified {len(insights)} potential financial leaks.")
            return insights
        except Exception as e:
            self.error(f"Leak Detection Failed: {e}")
            return []
        
