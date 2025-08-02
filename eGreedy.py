import random

class eGreedy:

    def __init__(self, nArms, epsilon = 0.1, redisClient = None, initial = 5, name = 'eGreedy'):

        self.nArms = nArms
        self.epsilon = epsilon
        self.redisClient = redisClient
        self.initial = initial
        self.name = name

        for i in range(self.nArms):
            key = f"{self.name}:arm:{i}"
            if not self.redisClient.exists(key):
                self.redisClient.hset(key, mapping = {"views": 0, "count": 0, "QEstimate": self.initial})
    
    def selectArm(self):
        if random.random() < self.epsilon:
            armExplored = random.choice(list(range(self.nArms)))
            return armExplored
        # Exploitation
        bestArm = None
        bestValue = float('-inf')
        for arm in range(self.nArms):
            count = int(self.redisClient.hget(f"{self.name}:arm:{arm}", "count") or 0)
            views = int(self.redisClient.hget(f"{self.name}:arm:{arm}", "views") or 0)
            avgReward = (count + self.initial) / views if views > 0 else self.initial
            self.redisClient.hset(f"{self.name}:arm:{arm}", "QEstimate", avgReward)
            if avgReward > bestValue:
                bestValue = avgReward
                bestArm = arm
        return bestArm

    def update(self, arm, reward):
        key = f"{self.name}:arm:{arm}"
        self.redisClient.hincrby(key, "count", reward)
        count = int(self.redisClient.hget(f"{self.name}:arm:{arm}", "count") or 0)
        views = int(self.redisClient.hget(f"{self.name}:arm:{arm}", "views") or 0)
        avgReward = (count + self.initial) / views if views > 0 else self.initial
        self.redisClient.hset(f"{self.name}:arm:{arm}", "QEstimate", avgReward)        
    
    def stats(self):
        statsDic = {}
        for arm in range(self.nArms):
            statsDic[arm] = self.redisClient.hgetall(f"{self.name}:arm:{arm}")
        return statsDic


