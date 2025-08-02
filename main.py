from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import redis
from eGreedy import eGreedy
from UCB import UCB
from thompsonSampling import thompsonSampling

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
# agentName = "eGreedy"
# agentName = "UCB"
agentName = "thompsonSampling"
# agent = eGreedy(nArms = len(VARIANTS), redisClient = r)
# agent = UCB(nArms = len(VARIANTS), redisClient = r, name = agentName)
agent = thompsonSampling(nArms = len(VARIANTS), redisClient = r, name = agentName)

@app.get("/", response_class=HTMLResponse)
async def showPage(request: Request):
    action = agent.selectArm()
    variant = VARIANTS[action]
    r.hincrby(f"{agentName}:arm:{action}", "views", 1)
    agent.update(action, reward=0)
    return templates.TemplateResponse("index.html", {"request": request, "variant": variant})

@app.get("/click/{variant}")
async def trackClick(variant: str):
    if variant in VARIANTS.values():
        reward = 1

        agent.update(reverseVARIANTS[variant], reward)
    return RedirectResponse("/")

@app.get("/stats")
def stats():
    return agent.stats()
