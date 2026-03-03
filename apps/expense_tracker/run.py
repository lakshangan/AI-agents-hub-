import asyncio
import os
import sys

# Ensure modular imports from root
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from apps.expense_tracker.logic.parser import StatementParserAgent
from apps.expense_tracker.logic.detector import LeakDetectorAgent
from apps.expense_tracker.logic.coach import FinancialCoachAgent
from dotenv import load_dotenv

load_dotenv()

async def main():
    print("🚀 Initializing Personal Finance 'Leak' Agents...")

    # Simulated input: Raw text from a bank statement or copy-pasted info
    # In a real app, this would come from a file upload or input field.
    raw_statement_text = """
    Date: 2024-03-01 Description: Amazon Prime Amount: 14.99
    Date: 2024-03-02 Description: Starbucks Amount: 6.50
    Date: 2024-03-05 Description: Netflix Amount: 19.99
    Date: 2024-03-10 Description: OpenAI GPT Plus Amount: 20.00
    Date: 2024-03-12 Description: Starbucks Amount: 7.25
    Date: 2024-03-14 Description: LinkedIn Premium Amount: 39.99
    Date: 2024-03-15 Description: Starbucks Amount: 5.50
    """

    # 1. Statement Parser: Converts messy text to structured transactions
    parser = StatementParserAgent()
    transactions = await parser.run(raw_statement_text)

    # 2. Leak Detector: Categorizes and finds "leaks"
    detector = LeakDetectorAgent()
    leaks = await detector.run(transactions)

    # 3. Financial Coach: Formats the insights and broadcasts to Telegram
    coach = FinancialCoachAgent()
    report = await coach.run({"transactions": transactions, "leaks": leaks})

    print("\n------------------------------")
    print("📡 FINANCIAL LEAK ANALYSIS DONE:")
    print(f"Total Transactions Scanned: {len(report.transactions)}")
    print(f"Total Amount Scraped: ${report.total_spent:.2f}")
    if report.top_leak:
        print(f"⚠️ TOP LEAK DETECTED: {report.top_leak.category} - {report.top_leak.impact_score * 100}% impact")
        print(f"📌 SUGGESTION: {report.top_leak.suggestion}")
    print("✅ Financial Advisor sent to Telegram.")
    print("------------------------------\n")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Interrupted by user.")
