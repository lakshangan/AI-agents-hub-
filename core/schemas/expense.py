from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Transaction(BaseModel):
    date: str
    description: str
    amount: float
    category: Optional[str] = "Uncategorized"
    is_subscription: bool = False

class FinancialInsight(BaseModel):
    category: str
    summary: str
    impact_score: float # 0.0 to 1.0 (how much this "leaks" money)
    suggestion: str

class ExpenseReport(BaseModel):
    timestamp: datetime = datetime.now()
    transactions: List[Transaction]
    total_spent: float
    detected_leaks: List[FinancialInsight]
    top_leak: Optional[FinancialInsight] = None
