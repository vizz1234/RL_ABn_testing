# config.py

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DECODE_RESPONSES = True

VARIANTS = {
    0: "A",
    1: "B",
    2: "C"
}
EPSILON = 0.1 #Hyper Parameter for epsilon-greedy
C = 2 #Hyper parameter for UCB
AGENT_NAME = "thompsonSampling"  # or "eGreedy" / "UCB"
