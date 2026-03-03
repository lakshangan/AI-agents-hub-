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

    # Ask for statement or use default fake
    default_path = "apps/expense_tracker/fake_statement.csv"
    file_path = input(f"📂 Please enter your statement file (default: {default_path}): ").strip()
    if not file_path: file_path = default_path
    
    if not os.path.exists(file_path):
        print(f"❌ Error: File '{file_path}' not found. Please check the path and try again.")
        return

    try:
        with open(file_path, 'r') as f:
            raw_statement_text = f.read()
    except Exception as e:
        print(f"❌ Failed to read file: {e}")
        return

    # 1. Statement Parser: Converts messy text to structured transactions
    parser = StatementParserAgent()
    transactions = await parser.run(raw_statement_text)

    if not transactions:
        print("⚠️ No transactions could be parsed from the file content.")
        return

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
