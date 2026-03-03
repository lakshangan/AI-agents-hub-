# 🤖 AI Agents Hub (v1.0)

Welcome to your scalable AI Agent Hub. This repository is designed to host multiple independent AI applications, all powered by a shared core architecture.

---

## 🏗️ Architecture
- **`/core`**: Shared base classes and communication schemas (News, Expenses).
- **`/apps`**: Individual agency containers.
  - **`ai_news`**: AI News Briefing Agent.
  - **`expense_tracker`**: Personal Finance Leak Detector.

---

## 🚀 How to Run the Agents

### 1. Run Personal Finance Agent (apps/expense_tracker)
Identify money leaks and get financial advice.
```bash
./.venv/bin/python3 apps/expense_tracker/run.py
```
> **Tip:** When prompted for a file, just press **Enter** to use the `fake_statement.csv` for a demo!

### 2. Run AI News Agent (apps/ai_news)
Get your morning AI intelligence report via Telegram.
```bash
./.venv/bin/python3 apps/ai_news/run.py
```

---

## 🛠️ Adding New Agents
1. Create a new folder in `apps/your_new_app`.
2. Create a `logic/` folder for your specialized agents.
3. Inherit from `BaseAgent` in `core/base.py`.
4. Create a `run.py` to orchestrate your new agent flow.

Enjoy your automated AI fleet! 🚀
