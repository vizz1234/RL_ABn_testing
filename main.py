from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import redis
from eGreedy import eGreedy

app = FastAPI()
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
templates = Jinja2Templates(directory="templates")

VARIANTS = {
    0: "A",
    1: "B",
    2: "C"
}
reverseVARIANTS = {v: k for k, v in VARIANTS.items()}
EPSILON = 0.1
agentName = "eGreedy"
agent = eGreedy(nArms = len(VARIANTS), redisClient = r)

@app.get("/", response_class=HTMLResponse)
async def showPage(request: Request):
    action = agent.selectArm()
    variant = VARIANTS[action]
    r.hincrby(f"{agentName}:arm:{action}", "views", 1)
    return templates.TemplateResponse("index.html", {"request": request, "variant": variant})

@app.get("/click/{variant}")
async def trackClick(variant: str):
    if variant in VARIANTS.values():
        reward = 1

        agent.update(reverseVARIANTS[variant], reward)
    return RedirectResponse("/")

@app.get("/stats")
def stats():
    return {
        v: {
            "clicks": int(r.hget(f"{agentName}:arm:{v}", 'count') or 0),
            "views": int(r.hget(f"{agentName}:arm:{v}", 'views') or 0),
            "estimate": round((int(r.hget(f"{agentName}:arm:{v}", 'count') or 0) + agent.initial)/ int(r.hget(f"{agentName}:arm:{v}", 'views') or 1), 2)
        }
        for v in VARIANTS
    }
