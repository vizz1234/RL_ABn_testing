from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import redis
import random

app = FastAPI()
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
templates = Jinja2Templates(directory="templates")

VARIANTS = ["A", "B"]
EPSILON = 0.1

def get_avg_reward(variant):
    clicks = int(r.get(f"clicks:{variant}") or 0)
    views = int(r.get(f"views:{variant}") or 1)  # Avoid div by 0
    return clicks / views

def select_variant():
    if random.random() < EPSILON:
        return random.choice(VARIANTS)
    rewards = {v: get_avg_reward(v) for v in VARIANTS}
    return max(rewards, key=rewards.get)

@app.get("/", response_class=HTMLResponse)
async def show_page(request: Request):
    variant = select_variant()
    r.incr(f"views:{variant}")
    return templates.TemplateResponse("index.html", {"request": request, "variant": variant})

@app.get("/click/{variant}")
async def track_click(variant: str):
    if variant in VARIANTS:
        r.incr(f"clicks:{variant}")
    return RedirectResponse("/")

@app.get("/stats")
def stats():
    return {
        v: {
            "clicks": int(r.get(f"clicks:{v}") or 0),
            "views": int(r.get(f"views:{v}") or 0),
            "ctr": round(get_avg_reward(v), 4)
        }
        for v in VARIANTS
    }
