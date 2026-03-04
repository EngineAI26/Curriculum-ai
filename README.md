# 🧠 CurriculumAI — Personalized Learning Orchestrator

> An AI-powered multi-agent curriculum builder that detects knowledge gaps, generates personalized learning paths, creates quizzes, and recommends curated resources — for any subject, any age.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Claude](https://img.shields.io/badge/Powered%20by-Claude%20AI-purple)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🏗 Architecture — Multi-Agent Orchestration

This project implements the **Orchestrator-Agent pattern** from modern agentic AI systems:

```
Task (User Input)
      │
      ▼
 Orchestrator ──► Task Ledger (subject, level, goal, known topics)
      │
      ▼
 Progress Ledger ──► Track completion, quiz scores, gaps
      │
      ├── Agent 1: Curriculum Generator  → Personalized module tree
      ├── Agent 2: Knowledge Gap Detector → Identifies missing concepts  
      ├── Agent 3: Quiz Generator         → 5-question MCQ per topic
      └── Agent 4: Resource Recommender   → Curated learning materials
```

**Stall Detection**: If agents produce unproductive loops or incomplete data, the orchestrator logs entries to the Progress Ledger and attempts fallback strategies.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 Knowledge Gap Detection | AI identifies what you're missing vs. what you claim to know |
| 🗺️ Personalized Curriculum | Skips known topics, builds custom module tree |
| 📊 Progress Ledger | Full orchestrator log of your learning journey |
| 🧪 Auto Quiz Generation | 5-question MCQ quiz per topic with explanations |
| 📖 Resource Recommendations | Curated videos, articles, books, and courses |
| 🎯 Gap Analysis | AI compares quiz performance vs. self-reported knowledge |

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/curriculum-ai.git
cd curriculum-ai
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

---

## ☁️ Deploy on Streamlit Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. In **Advanced Settings → Secrets**, add:

4. Click **Deploy** — your app is live! 🎉

---


## 🧩 Tech Stack

- **Frontend**: Streamlit (Python)
- **AI**: Sarvam AI
- **Pattern**: Multi-Agent Orchestration with Task & Progress Ledgers
- **Deployment**: Streamlit Cloud

---

## 📁 Project Structure

```
curriculum-ai/
├── app.py                        # Main application (all pages + orchestrator)
├── requirements.txt              # Python dependencies
├── .streamlit/
│   ├── config.toml               # Streamlit theme config
│   └── secrets.toml.example      # API key template
├── .gitignore
└── README.md
```

---

## 🎮 How to Use

1. **Enter your subject** — e.g., "Python", "Guitar", "Machine Learning"
2. **Set your level** — Beginner to Advanced
3. **State your goal** — What you want to achieve
4. **Knowledge Check** — Select topics you already know
5. **Get your curriculum** — AI builds a personalized path
6. **Learn** — Take quizzes, get resources, mark topics done
7. **Track progress** — View the Progress Ledger and Gap Analysis

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.


---

*Built with ❤️ using Sarvam AI and Streamlit*
