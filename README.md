# 🎯 RL-Based A/B/n Testing

A practical, plug-and-play framework to run **real-time A/B/n testing** using **Reinforcement Learning (Multi-Armed Bandits)**. Supports Epsilon-Greedy, UCB, and Thompson Sampling agents, both in **live deployments** (via FastAPI + Redis) and **offline simulations**.

---

## 🧠 Why Reinforcement Learning for A/B/n Testing?

Traditional A/B testing wastes traffic by allocating equally or randomly. RL-based approaches adaptively shift traffic to better-performing variants, increasing engagement during testing — not just after.

---

## 📦 Installation

> ⚙️ Requires Python 3.10+ (tested on 3.10/3.11/3.13), and Redis installed locally or via Docker.

### 1. Clone the repo
```bash
git clone https://github.com/vizz1234/RL_ABn_testing.git
cd RL-AB-testing
```

## 📦 Installation

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```
### 2. Start Redis server
If installed locally:

```bash
brew services start redis
```

## 🗂 Project Structure

```
RL-AB-testing/
├── main.py                  # FastAPI app for real-time testing
├── config.py                # App config (epsilon, Redis, etc.)
├── templates/
│   └── index.html           # Jinja2 template to serve variants
├── eGreedy.py               # Online Epsilon-Greedy agent
├── UCB.py                   # Online UCB agent
├── thompsonSampling.py      # Online Thompson Sampling agent
├── simulate/
│   ├── eGreedy.py           # Offline simulation for e-Greedy
│   ├── UCB.py               # Offline simulation for UCB
│   ├── thompsonSampling.py  # Offline simulation for Thompson Sampling
├── requirements.txt         # Minimal project dependencies
└── README.md                # You're reading it.
```

## 🚀 Running the Live App
This app mimics a web experiment where users are shown different variants.

```
fastapi dev main.py
```

Then open http://localhost:8000 — each refresh mimics a new user. Behind the scenes, the selected agent (e.g., ε-Greedy) updates estimates and shifts traffic in real-time, backed by Redis. 

Go to http://localhost:8000/stats for viewing metrics of each variant.


## 📊 Simulation Mode (Offline)
To visualize how each agent behaves in controlled setups, run:

```
cd simulate
python eGreedy.py
python UCB.py
python thompsonSampling.py
```

Each script:

Runs 1000 simulated users.

Logs views and estimates per variant. 

Displays an animation of progression of each variant over time.

