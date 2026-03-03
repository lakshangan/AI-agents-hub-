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
        self.model = genai.GenerativeModel('gemini-1.5-pro')

    async def run(self, transactions: List[Transaction]) -> List[FinancialInsight]:
        self.log(f"Searching for 'leaks' in {len(transactions)} items...")
        
        try:
            tx_data = [tx.dict() for tx in transactions]
            prompt = f"Identify 2 money leaks (JSON: category, summary, impact_score, suggestion) from: {json.dumps(tx_data)}"
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            text_data = response.text.strip().replace("```json", "").replace("```", "")
            data = json.loads(text_data)
            return [FinancialInsight(**item) for item in data]
        except Exception:
            self.error("AI Leak Detection Failed. Switching to Synthetic Insight...")
            return self._synthetic_detect(transactions)

    def _synthetic_detect(self, transactions: List[Transaction]) -> List[FinancialInsight]:
        insights = []
        # Logical check for common leak types
        subscriptions = [t for t in transactions if t.is_subscription]
        if subscriptions:
            insights.append(FinancialInsight(
                category="Subscriptions",
                summary=f"Found {len(subscriptions)} recurring payments totaling ${sum(s.amount for s in subscriptions)}",
                impact_score=0.8,
                suggestion="Review your Netflix and Prime accounts to see if you use them enough to justify the price."
            ))
        
        food = [t for t in transactions if any(x in t.description.upper() for x in ["SWIGGY", "ZOMATO", "STARBUCKS", "FOOD"])]
        if food:
            total_food = sum(f.amount for f in food)
            insights.append(FinancialInsight(
                category="Dining Out",
                summary=f"Detected {len(food)} food orders totaling ${total_food}. These small frequent habits 'leak' cash over time.",
                impact_score=0.6,
                suggestion="Try meal prepping 2 days a week to lower your monthly Swiggy/Zomato bills."
            ))
        return insights
        
