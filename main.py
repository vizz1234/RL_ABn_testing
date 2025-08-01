from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import redis
from eGreedy import eGreedy

app = FastAPI()
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
templates = Jinja2Templates(directory="templates")

VARIANTS = {
    "A": 0,
    "B": 1,
    "C": 2
}
EPSILON = 0.1
agentName = "eGreedy"
agent = eGreedy(nArms = len(VARIANTS), redisClient = r)

@app.get("/", response_class=HTMLResponse)
async def showPage(request: Request):
    variant = VARIANTS[agent.selectArm()]
    r.incr(f"{agentName}:arm:{variant}:views")
    return templates.TemplateResponse("index.html", {"request": request, "variant": variant})

@app.get("/click/{variant}")
async def trackClick(variant: str):
    if variant in VARIANTS:
        reward = 1
        agent.update(VARIANTS[variant], reward)
    return RedirectResponse("/")

@app.get("/stats")
def stats():
    return {
        v: {
            "clicks": int(r.get(f"{agentName}:arm:{v}:count") or 0),
            "views": int(r.get(f"{agentName}:arm:{v}:views") or 0),
            "ctr": round(r.get(f"{agentName}:arm:{v}:count") / int(r.get(f"{agentName}:arm:{v}:views") or 1), 2)
        }
        for v in VARIANTS.values()
    }
