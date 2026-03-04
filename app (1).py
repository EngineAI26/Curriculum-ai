import streamlit as st
import json
import requests
from typing import Optional

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CurriculumAI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

:root {
    --bg: #0d0f14;
    --card: #151820;
    --card2: #1c2030;
    --accent: #7c6af7;
    --accent2: #f76a6a;
    --accent3: #6af7c8;
    --text: #e8eaf0;
    --muted: #7a7f94;
    --border: #252a3a;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--card) !important;
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] * { color: var(--text) !important; }

/* Headings */
h1, h2, h3 { font-family: 'Syne', sans-serif !important; }

/* Cards */
.card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
    transition: border-color 0.2s;
}
.card:hover { border-color: var(--accent); }

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #7c6af7, #f76a6a, #6af7c8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.1;
    margin-bottom: 8px;
}

.hero-sub {
    color: var(--muted);
    font-size: 1.1rem;
    margin-bottom: 28px;
}

.badge {
    display: inline-block;
    background: var(--card2);
    border: 1px solid var(--border);
    border-radius: 999px;
    padding: 4px 14px;
    font-size: 0.8rem;
    color: var(--muted);
    margin: 4px;
}

.badge-accent { border-color: var(--accent); color: var(--accent); }
.badge-green  { border-color: var(--accent3); color: var(--accent3); }
.badge-red    { border-color: var(--accent2); color: var(--accent2); }

.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 12px;
}

.progress-bar-bg {
    background: var(--card2);
    border-radius: 999px;
    height: 8px;
    margin: 6px 0 14px;
    overflow: hidden;
}
.progress-bar-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, var(--accent), var(--accent3));
    transition: width 0.6s ease;
}

.topic-chip {
    display: inline-block;
    background: var(--card2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 6px 14px;
    margin: 4px;
    font-size: 0.88rem;
    cursor: pointer;
}

.topic-chip.known   { border-color: var(--accent3); color: var(--accent3); background: rgba(106,247,200,0.07); }
.topic-chip.unknown { border-color: var(--accent2); color: var(--accent2); background: rgba(247,106,106,0.07); }
.topic-chip.learning{ border-color: var(--accent);  color: var(--accent);  background: rgba(124,106,247,0.07); }

.quiz-option {
    background: var(--card2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px 18px;
    margin: 6px 0;
    cursor: pointer;
    transition: all 0.2s;
}
.quiz-option:hover { border-color: var(--accent); }
.quiz-option.correct { border-color: var(--accent3); background: rgba(106,247,200,0.1); }
.quiz-option.wrong   { border-color: var(--accent2); background: rgba(247,106,106,0.1); }

.resource-card {
    background: var(--card2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px;
    margin: 8px 0;
}
.resource-card h4 { font-family: 'Syne', sans-serif; margin: 0 0 4px; font-size: 0.95rem; }
.resource-card p  { color: var(--muted); font-size: 0.85rem; margin: 0; }

/* Streamlit widget overrides */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), #5b4fd6) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    padding: 10px 24px !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: var(--card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
}

.stSlider > div { color: var(--text) !important; }
.stMarkdown p { color: var(--text); }
.stExpander { border: 1px solid var(--border) !important; border-radius: 12px !important; }

div[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 2rem !important;
    color: var(--accent) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Sarvam AI client ──────────────────────────────────────────────────────────
SARVAM_API_URL = "https://api.sarvam.ai/v1/chat/completions"
SARVAM_MODEL   = "sarvam-m"

def call_sarvam(prompt: str, system: str = "", max_tokens: int = 2000) -> str:
    api_key = st.secrets["SARVAM_API_KEY"]
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": SARVAM_MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.3,
    }
    resp = requests.post(SARVAM_API_URL, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]

def call_sarvam_json(prompt: str, system: str = "") -> dict:
    system_full = (system + "\n\n" if system else "") + "IMPORTANT: Respond ONLY with valid JSON. No markdown, no backticks, no extra text."
    raw = call_sarvam(prompt, system_full, max_tokens=2000)
    raw = raw.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
    return json.loads(raw)

# aliases so rest of app works unchanged
call_claude      = call_sarvam
call_claude_json = call_sarvam_json

# ── Session state defaults ────────────────────────────────────────────────────
defaults = {
    "page": "home",
    "subject": "",
    "level": "Beginner",
    "goal": "",
    "curriculum": None,
    "knowledge_map": {},     # topic -> "known"/"unknown"/"learning"
    "progress": {},          # topic -> bool (completed)
    "quiz_state": None,
    "quiz_answers": {},
    "quiz_score": None,
    "resources": None,
    "ledger": [],            # progress ledger entries
    "current_topic": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Helpers ───────────────────────────────────────────────────────────────────
def log_ledger(entry: str):
    st.session_state.ledger.append(entry)

def go(page: str):
    st.session_state.page = page
    st.rerun()

def pct_complete() -> int:
    prog = st.session_state.progress
    if not prog:
        return 0
    done = sum(1 for v in prog.values() if v)
    return int(done / len(prog) * 100)

# ── Orchestrator: generate curriculum ────────────────────────────────────────
def generate_curriculum(subject: str, level: str, goal: str, known_topics: list) -> dict:
    prompt = f"""
You are an expert curriculum designer for all ages.

Subject: {subject}
Level: {level}
Learning goal: {goal}
Topics the learner already knows: {known_topics}

Create a personalized, structured curriculum. Return JSON with this exact schema:
{{
  "title": "...",
  "description": "...",
  "estimated_hours": <int>,
  "modules": [
    {{
      "id": "m1",
      "title": "...",
      "description": "...",
      "topics": [
        {{"id": "t1", "title": "...", "summary": "...", "is_prerequisite": false}}
      ]
    }}
  ],
  "knowledge_gaps": ["topic1", "topic2"],
  "recommended_path": ["t1", "t2", "t3"]
}}
Skip topics the learner already knows. Return 3-5 modules, 3-5 topics each.
"""
    return call_claude_json(prompt)

# ── Orchestrator: generate quiz ───────────────────────────────────────────────
def generate_quiz(topic_title: str, subject: str, level: str) -> dict:
    prompt = f"""
Create a 5-question multiple-choice quiz for:
Topic: {topic_title}
Subject: {subject}
Level: {level}

JSON schema:
{{
  "topic": "...",
  "questions": [
    {{
      "id": "q1",
      "question": "...",
      "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
      "correct": "A",
      "explanation": "..."
    }}
  ]
}}
"""
    return call_claude_json(prompt)

# ── Orchestrator: get resources ───────────────────────────────────────────────
def get_resources(topic_title: str, subject: str, level: str) -> dict:
    prompt = f"""
Recommend learning resources for:
Topic: {topic_title}
Subject: {subject}
Level: {level}

Return JSON:
{{
  "resources": [
    {{
      "title": "...",
      "type": "Video|Article|Book|Course|Exercise",
      "platform": "...",
      "description": "...",
      "duration": "...",
      "url_hint": "search query to find it"
    }}
  ]
}}
Return 5 diverse resources.
"""
    return call_claude_json(prompt)

# ── Orchestrator: detect knowledge gaps ──────────────────────────────────────
def detect_gaps(subject: str, known: list, quiz_scores: dict) -> str:
    prompt = f"""
You are a learning analytics agent.

Subject: {subject}
Topics the learner claims to know: {known}
Quiz scores per topic (0-5): {quiz_scores}

Analyze knowledge gaps and provide:
1. Real vs claimed knowledge assessment
2. Critical gaps to address first
3. Personalized study recommendations

Be concise, direct, and encouraging. Use plain text with markdown formatting.
"""
    return call_claude(prompt, max_tokens=800)

# ══════════════════════════════════════════════════════════════════════════════
# PAGES
# ══════════════════════════════════════════════════════════════════════════════

def page_home():
    st.markdown('<div class="hero-title">CurriculumAI</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Your AI orchestrator for personalized learning — any subject, any age.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2], gap="large")

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">📚 Start Learning</div>', unsafe_allow_html=True)

        subject = st.text_input("What do you want to learn?", placeholder="e.g. Python, Guitar, Calculus, Spanish…", key="inp_subject")
        level   = st.selectbox("Your current level", ["Complete Beginner", "Beginner", "Intermediate", "Advanced"], key="inp_level")
        goal    = st.text_area("What's your learning goal?", placeholder="e.g. Build a web app in 4 weeks, pass my exam, start a new hobby…", height=100, key="inp_goal")

        if st.button("🚀 Build My Curriculum", use_container_width=True):
            if not subject or not goal:
                st.warning("Please fill in the subject and goal.")
            else:
                st.session_state.subject = subject
                st.session_state.level   = level
                st.session_state.goal    = goal
                go("knowledge_check")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">✨ Features</div>', unsafe_allow_html=True)
        features = [
            ("🔍", "Knowledge Gap Detection", "AI finds what you're missing"),
            ("🗺️", "Personalized Path", "Skips what you know"),
            ("📊", "Progress Ledger", "Tracks your journey"),
            ("🧪", "Auto Quiz Generation", "Tests your understanding"),
            ("📖", "Resource Recommendations", "Curated learning materials"),
        ]
        for icon, title, desc in features:
            st.markdown(f"**{icon} {title}** — {desc}")
            st.markdown("")
        st.markdown('</div>', unsafe_allow_html=True)

        if st.session_state.curriculum:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-label">📈 Your Progress</div>', unsafe_allow_html=True)
            pct = pct_complete()
            st.markdown(f'<div class="progress-bar-bg"><div class="progress-bar-fill" style="width:{pct}%"></div></div>', unsafe_allow_html=True)
            st.markdown(f"**{pct}%** complete — {st.session_state.subject}")
            if st.button("Continue Learning →"):
                go("curriculum")
            st.markdown('</div>', unsafe_allow_html=True)


def page_knowledge_check():
    st.markdown('<div class="hero-title" style="font-size:2rem;">Knowledge Check</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hero-sub">Tell us what you already know about <strong>{st.session_state.subject}</strong></div>', unsafe_allow_html=True)

    with st.spinner("🤔 Generating topic assessment…"):
        if "kc_topics" not in st.session_state:
            prompt = f"""
List 12-15 key topics for learning {st.session_state.subject} from beginner to {st.session_state.level}.
Return JSON: {{"topics": ["topic1", "topic2", ...]}}
"""
            data = call_claude_json(prompt)
            st.session_state.kc_topics = data.get("topics", [])

    topics = st.session_state.kc_topics
    st.markdown('<div class="section-label">Select topics you already know well:</div>', unsafe_allow_html=True)

    cols = st.columns(3)
    selected = []
    for i, topic in enumerate(topics):
        with cols[i % 3]:
            if st.checkbox(topic, key=f"kc_{i}"):
                selected.append(topic)

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Back"):
            del st.session_state["kc_topics"]
            go("home")
    with col2:
        if st.button("Generate My Curriculum →", use_container_width=True):
            with st.spinner("🧠 Orchestrator building your personalized curriculum…"):
                curr = generate_curriculum(
                    st.session_state.subject,
                    st.session_state.level,
                    st.session_state.goal,
                    selected,
                )
                st.session_state.curriculum    = curr
                st.session_state.knowledge_map = {t: "known" for t in selected}
                # Init progress for all topics
                for mod in curr.get("modules", []):
                    for topic in mod.get("topics", []):
                        if topic["id"] not in st.session_state.progress:
                            st.session_state.progress[topic["id"]] = False
                log_ledger(f"✅ Curriculum generated: '{curr.get('title')}' with {len(curr.get('modules', []))} modules")
                log_ledger(f"🔍 Knowledge gaps detected: {curr.get('knowledge_gaps', [])}")
                del st.session_state["kc_topics"]
            go("curriculum")


def page_curriculum():
    curr = st.session_state.curriculum
    if not curr:
        go("home")
        return

    # Header
    st.markdown(f'<div class="hero-title" style="font-size:1.9rem;">{curr["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hero-sub">{curr["description"]}</div>', unsafe_allow_html=True)

    # Stats row
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Modules",       len(curr.get("modules", [])))
    with c2: st.metric("Est. Hours",    curr.get("estimated_hours", "—"))
    with c3: st.metric("Completed",     f'{pct_complete()}%')
    with c4: st.metric("Gaps Found",    len(curr.get("knowledge_gaps", [])))

    # Progress bar
    pct = pct_complete()
    st.markdown(f'<div class="progress-bar-bg"><div class="progress-bar-fill" style="width:{pct}%"></div></div>', unsafe_allow_html=True)

    # Knowledge gaps callout
    gaps = curr.get("knowledge_gaps", [])
    if gaps:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">🔍 Knowledge Gaps Detected</div>', unsafe_allow_html=True)
        for g in gaps:
            st.markdown(f'<span class="badge badge-red">⚠ {g}</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Modules
    for mod in curr.get("modules", []):
        with st.expander(f"📦 {mod['title']}", expanded=True):
            st.markdown(f"*{mod['description']}*")
            st.markdown("")
            for topic in mod.get("topics", []):
                tid   = topic["id"]
                done  = st.session_state.progress.get(tid, False)
                status = "✅" if done else "⬜"

                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                with col1:
                    st.markdown(f"**{status} {topic['title']}**")
                    st.markdown(f"<small style='color:var(--muted)'>{topic['summary']}</small>", unsafe_allow_html=True)
                with col2:
                    if st.button("📖 Resources", key=f"res_{tid}"):
                        st.session_state.current_topic = topic
                        go("resources")
                with col3:
                    if st.button("🧪 Quiz", key=f"quiz_{tid}"):
                        st.session_state.current_topic = topic
                        st.session_state.quiz_state    = None
                        st.session_state.quiz_score    = None
                        st.session_state.quiz_answers  = {}
                        go("quiz")
                with col4:
                    if not done:
                        if st.button("Mark Done", key=f"done_{tid}"):
                            st.session_state.progress[tid] = True
                            log_ledger(f"✅ Completed topic: {topic['title']}")
                            st.rerun()
                    else:
                        if st.button("Undo", key=f"undo_{tid}"):
                            st.session_state.progress[tid] = False
                            st.rerun()
                st.markdown("---")

    # Bottom nav
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏠 Home"):
            go("home")
    with col2:
        if st.button("📊 Progress Ledger"):
            go("ledger")
    with col3:
        if st.button("🔍 Gap Analysis"):
            go("gap_analysis")


def page_quiz():
    topic = st.session_state.current_topic
    if not topic:
        go("curriculum")
        return

    st.markdown(f'<div class="hero-title" style="font-size:1.8rem;">Quiz: {topic["title"]}</div>', unsafe_allow_html=True)

    if not st.session_state.quiz_state:
        with st.spinner("🧪 Generating quiz questions…"):
            st.session_state.quiz_state   = generate_quiz(topic["title"], st.session_state.subject, st.session_state.level)
            st.session_state.quiz_answers = {}
            st.session_state.quiz_score   = None
            log_ledger(f"🧪 Quiz started: {topic['title']}")

    quiz = st.session_state.quiz_state
    questions = quiz.get("questions", [])

    submitted = st.session_state.quiz_score is not None

    for q in questions:
        st.markdown(f"**{q['question']}**")
        chosen = st.radio("", q["options"], key=f"q_{q['id']}", disabled=submitted)
        if not submitted:
            st.session_state.quiz_answers[q["id"]] = chosen
        if submitted:
            correct_letter = q["correct"]
            correct_option = next((o for o in q["options"] if o.startswith(correct_letter + ".")), None)
            user_ans       = st.session_state.quiz_answers.get(q["id"], "")
            if user_ans and user_ans.startswith(correct_letter):
                st.success(f"✅ Correct! {q['explanation']}")
            else:
                st.error(f"❌ Correct answer: {correct_option}. {q['explanation']}")
        st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        if not submitted:
            if st.button("Submit Quiz", use_container_width=True):
                score = 0
                for q in questions:
                    ans = st.session_state.quiz_answers.get(q["id"], "")
                    if ans.startswith(q["correct"]):
                        score += 1
                st.session_state.quiz_score = score
                log_ledger(f"📝 Quiz completed: {topic['title']} — Score {score}/{len(questions)}")
                if score == len(questions):
                    st.session_state.progress[topic["id"]] = True
                    log_ledger(f"✅ Topic mastered: {topic['title']}")
                st.rerun()
        else:
            score = st.session_state.quiz_score
            total = len(questions)
            pct   = int(score / total * 100)
            if pct >= 80:
                st.success(f"🎉 Score: {score}/{total} ({pct}%) — Great job!")
            elif pct >= 60:
                st.warning(f"🙂 Score: {score}/{total} ({pct}%) — Keep practicing!")
            else:
                st.error(f"😅 Score: {score}/{total} ({pct}%) — Review the material and retry.")
    with col2:
        if st.button("← Back to Curriculum"):
            go("curriculum")


def page_resources():
    topic = st.session_state.current_topic
    if not topic:
        go("curriculum")
        return

    st.markdown(f'<div class="hero-title" style="font-size:1.8rem;">Resources: {topic["title"]}</div>', unsafe_allow_html=True)

    if not st.session_state.resources or st.session_state.resources.get("_topic") != topic["id"]:
        with st.spinner("📖 Finding best resources for you…"):
            res = get_resources(topic["title"], st.session_state.subject, st.session_state.level)
            res["_topic"] = topic["id"]
            st.session_state.resources = res
            log_ledger(f"📖 Resources fetched for: {topic['title']}")

    TYPE_ICONS = {"Video": "🎬", "Article": "📄", "Book": "📚", "Course": "🎓", "Exercise": "🏋️"}

    for r in st.session_state.resources.get("resources", []):
        icon = TYPE_ICONS.get(r["type"], "📌")
        st.markdown(f"""
<div class="resource-card">
  <h4>{icon} {r['title']} <span class="badge">{r['type']}</span> <span class="badge badge-accent">{r.get('platform','')}</span></h4>
  <p>{r['description']}</p>
  <small style="color:var(--muted)">⏱ {r.get('duration','')} &nbsp;·&nbsp; 🔎 Search: <em>{r.get('url_hint','')}</em></small>
</div>
""", unsafe_allow_html=True)

    if st.button("← Back to Curriculum"):
        go("curriculum")


def page_ledger():
    st.markdown('<div class="hero-title" style="font-size:1.8rem;">Progress Ledger</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Your full learning journey tracked by the orchestrator.</div>', unsafe_allow_html=True)

    curr = st.session_state.curriculum
    if curr:
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("Overall Progress", f"{pct_complete()}%")
        with c2:
            done = sum(1 for v in st.session_state.progress.values() if v)
            st.metric("Topics Done", f"{done}/{len(st.session_state.progress)}")
        with c3: st.metric("Ledger Entries", len(st.session_state.ledger))

        pct = pct_complete()
        st.markdown(f'<div class="progress-bar-bg"><div class="progress-bar-fill" style="width:{pct}%"></div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-label">📋 Orchestrator Log</div>', unsafe_allow_html=True)

    if st.session_state.ledger:
        for entry in reversed(st.session_state.ledger):
            st.markdown(f'<div class="card" style="padding:12px 18px; margin-bottom:8px;">{entry}</div>', unsafe_allow_html=True)
    else:
        st.info("No activity yet. Start learning to see your progress here!")

    st.markdown("---")
    if st.button("← Back to Curriculum"):
        go("curriculum")


def page_gap_analysis():
    st.markdown('<div class="hero-title" style="font-size:1.8rem;">Gap Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">AI-powered analysis of your real vs. claimed knowledge.</div>', unsafe_allow_html=True)

    quiz_scores = {}
    for entry in st.session_state.ledger:
        if "Quiz completed" in entry and "Score" in entry:
            parts = entry.split("—")
            if len(parts) >= 2:
                topic_part = parts[0].replace("📝 Quiz completed: ", "").strip()
                score_part = parts[1].strip()
                try:
                    score_str = score_part.replace("Score ", "")
                    num, den  = score_str.split("/")
                    quiz_scores[topic_part] = int(num)
                except Exception:
                    pass

    known = list(st.session_state.knowledge_map.keys())

    with st.spinner("🔍 Analyzing your knowledge gaps…"):
        analysis = detect_gaps(st.session_state.subject, known, quiz_scores)

    st.markdown(analysis)

    st.markdown("---")
    gaps = st.session_state.curriculum.get("knowledge_gaps", []) if st.session_state.curriculum else []
    if gaps:
        st.markdown('<div class="section-label">⚠ Priority Gap Areas</div>', unsafe_allow_html=True)
        for g in gaps:
            st.markdown(f'<span class="badge badge-red">⚠ {g}</span>', unsafe_allow_html=True)

    st.markdown("---")
    if st.button("← Back to Curriculum"):
        go("curriculum")


# ── Router ────────────────────────────────────────────────────────────────────
PAGES = {
    "home":           page_home,
    "knowledge_check": page_knowledge_check,
    "curriculum":     page_curriculum,
    "quiz":           page_quiz,
    "resources":      page_resources,
    "ledger":         page_ledger,
    "gap_analysis":   page_gap_analysis,
}

# Sidebar nav
with st.sidebar:
    st.markdown('<div style="font-family:Syne,sans-serif; font-size:1.3rem; font-weight:800; margin-bottom:24px;">🧠 CurriculumAI</div>', unsafe_allow_html=True)

    if st.session_state.curriculum:
        curr_title = st.session_state.curriculum.get("title", "My Curriculum")
        st.markdown(f'<div class="badge badge-accent">📚 {curr_title[:30]}…</div>', unsafe_allow_html=True)
        pct = pct_complete()
        st.markdown(f'<div class="progress-bar-bg"><div class="progress-bar-fill" style="width:{pct}%"></div></div>', unsafe_allow_html=True)
        st.markdown(f"<small style='color:var(--muted)'>{pct}% complete</small>", unsafe_allow_html=True)
        st.markdown("---")

        nav_items = [
            ("🏠", "Home",           "home"),
            ("🗺️", "Curriculum",     "curriculum"),
            ("📊", "Progress Ledger","ledger"),
            ("🔍", "Gap Analysis",   "gap_analysis"),
        ]
        for icon, label, target in nav_items:
            active = "badge-accent" if st.session_state.page == target else ""
            if st.button(f"{icon} {label}", use_container_width=True, key=f"nav_{target}"):
                go(target)
    else:
        st.markdown('<small style="color:var(--muted)">Start learning to unlock navigation.</small>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<small style="color:var(--muted)">Powered by Claude AI<br>Multi-Agent Orchestration</small>', unsafe_allow_html=True)

# Render current page
PAGES.get(st.session_state.page, page_home)()
