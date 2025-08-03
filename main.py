from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import redis
from eGreedy import eGreedy
from UCB import UCB
from thompsonSampling import thompsonSampling
from config import REDIS_HOST, REDIS_PORT, REDIS_DECODE_RESPONSES, VARIANTS, EPSILON, AGENT_NAME, C

app = FastAPI()
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=REDIS_DECODE_RESPONSES)
templates = Jinja2Templates(directory="templates")
reverseVARIANTS = {v: k for k, v in VARIANTS.items()}
agentName = AGENT_NAME

if agentName == "eGreedy":
    agent = eGreedy(nArms = len(VARIANTS), epsilon= EPSILON, redisClient = r)
if agentName == "UCB":
    agent = UCB(nArms = len(VARIANTS), redisClient = r, name = agentName, c = C)
if agentName == "thompsonSampling":
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
