<p align="center">
  <img src="assets/logo.png" alt="PotatoWatch Logo" width="220">
</p>

<h1 align="center">🥔 PotatoWatch</h1>

<p align="center">
  A local-first X engagement copilot that scores, ranks, remembers, and helps surface replies worth posting.
</p>

PotatoWatch is an experimental Python project built to reduce the amount of manual scrolling involved in finding worthwhile conversations on X.

Instead of blindly automating an account, PotatoWatch is designed around a simple principle:

**Let the software find and analyze opportunities. Let the human decide what gets posted.**

The project is currently in early development.

---

## Why PotatoWatch?

Finding posts worth replying to manually gets repetitive.

A typical session looks something like:

```text
scroll
scroll
scroll
irrelevant
promotion
irrelevant
interesting post
maybe reply?
scroll
scroll
```

PotatoWatch aims to turn that into:

```text
Candidate Posts
      ↓
Scoring
      ↓
Ranking
      ↓
Memory / Deduplication
      ↓
Human Review
      ↓
Reply
```

The long-term goal is a local assistant that can surface interesting developer conversations, suggest possible responses, remember previous interactions, and keep the final posting decision with the user.

---

## Current Features

PotatoWatch currently supports:

- 🧠 **Candidate post modeling** using Pydantic
- 🎯 **Deterministic post scoring**
- 📊 **Candidate ranking**
- 🚦 **REPLY / MAYBE / SKIP decisions**
- 🛑 **Hard blocking for promotional content**
- 💾 **SQLite persistence**
- 🔁 **Duplicate post detection**
- 🧪 **Automated scoring tests**
- 🥔 Extremely questionable branding

No X account automation or automatic posting is implemented.

---

## How Scoring Works

Candidate posts receive points based on simple deterministic rules.

Examples include:

```text
Developer-related content     +25
Relatable pain / debugging    +20
Contains a question           +15
Active conversation           +15
Healthy engagement            +10
Concise post                   +5
```

Certain content can also be rejected before scoring.

For example:

```text
Promotional content
        ↓
Hard Block
        ↓
Score: 0
Decision: SKIP
```

This rule-based system is intentionally simple for now.

The goal is to establish predictable behavior before introducing AI-based classification.

---

## Example

Input:

```text
@random_dev

Spent 6 hours debugging.
The problem was a missing comma.
```

PotatoWatch:

```text
Score: 75/100
Decision: REPLY

Reasons:
+25 developer-related
+20 relatable pain
+15 active conversation
+10 healthy engagement
+5 concise post
```

Meanwhile:

```text
BUY NOW!
My coding course is 90% off.
DM me.
Link in bio.
```

becomes:

```text
Score: 0/100
Decision: SKIP

BLOCKED: promotional content
```

Potato has standards.

---

## Project Structure

```text
potato-watch/
│
├── data/
│   └── potatowatch.db       # Local SQLite database (ignored by Git)
│
├── src/
│   ├── __init__.py
│   ├── database.py          # Persistence and duplicate detection
│   ├── main.py              # Current entry point
│   ├── models.py            # Pydantic models
│   ├── ranker.py            # Candidate ranking
│   └── scorer.py            # Deterministic scoring engine
│
├── tests/
│   └── test_scorer.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Far-200/potato-watch.git
cd potato-watch
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv potatowatch_venv
```

Activate it:

```powershell
.\potatowatch_venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Run PotatoWatch

```powershell
python -m src.main
```

You should see:

```text
🥔 PotatoWatch is awake.
```

---

## Running Tests

PotatoWatch currently uses Python's built-in `unittest`.

Run:

```powershell
python -m unittest discover -s tests -v
```

Expected result:

```text
Ran 4 tests

OK
```

---

## Database

PotatoWatch uses SQLite for local persistence.

The database is created automatically at:

```text
data/potatowatch.db
```

Candidate posts receive a unique key.

When a real platform post ID is available, that ID can be used directly.

For manually supplied posts, PotatoWatch generates a SHA-256 hash from:

```text
author + post text
```

This prevents the same candidate from being stored repeatedly.

---

## Current Architecture

```text
CandidatePost
      │
      ▼
┌───────────────┐
│ Hard Filters  │
└───────────────┘
      │
      ▼
┌───────────────┐
│    Scorer     │
└───────────────┘
      │
      ▼
  ScoreResult
      │
      ▼
┌───────────────┐
│    Ranker     │
└───────────────┘
      │
      ▼
┌───────────────┐
│    SQLite     │
└───────────────┘
      │
      ▼
 Human Review
```

---

## Roadmap

Planned experiments include:

- Candidate status tracking (`NEW`, `REPLIED`, `SKIPPED`, `IGNORED`)
- Better scoring heuristics
- Configurable scoring rules
- Interaction history
- CLI review queue
- Local LLM integration
- Reply suggestion generation
- Multiple reply styles / personalities
- Local Ollama support
- Source/provider abstraction
- Manual X workflow
- Optional official API integration where appropriate
- Simple local dashboard
- More automated tests

The architecture is intended to remain provider-independent so the core scoring, ranking, memory, and reply systems can work without depending entirely on a single external platform.

---

## Philosophy

PotatoWatch is **not intended to be an autonomous reply bot**.

The intended workflow is:

```text
Software discovers
        ↓
Software analyzes
        ↓
Software suggests
        ↓
Human reviews
        ↓
Human posts
```

Automation should reduce repetitive work without turning an account into a reply cannon.

---

## Tech Stack

```text
Python
Pydantic
SQLite
httpx
python-dotenv
Rich
unittest
```

Future local AI experiments may use Ollama.

---

## Development Status

```text
[✓] Project bootstrap
[✓] Candidate model
[✓] Deterministic scoring
[✓] REPLY / MAYBE / SKIP
[✓] Hard promotional blocker
[✓] Candidate ranking
[✓] Automated tests
[✓] SQLite persistence
[✓] Duplicate detection
[ ] Candidate status lifecycle
[ ] Review queue
[ ] Local AI
[ ] Reply generation
[ ] Provider integration
[ ] Dashboard
```

---

## Disclaimer

PotatoWatch is an experimental personal project.

Any future integrations with external platforms should follow the applicable platform rules, API terms, rate limits, and automation policies.

---

## Author

Built by [Farhaan Khan](https://github.com/Far-200)

Because apparently manually scrolling X was not enough suffering. 🥔💔
