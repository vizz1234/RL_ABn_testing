import math

class UCB:
    def __init__(self, nArms, redisClient, name="UCB", c=2, initial = 0):
        self.nArms = nArms
        self.redisClient = redisClient
        self.name = name
        self.c = c  # Confidence level multiplier
        self.initial = initial

        for i in range(self.nArms):
            key = f"{self.name}:arm:{i}"
            if not self.redisClient.exists(key):
                self.redisClient.hset(key, mapping = {"views": 0, "count": 0, "QEstimate": self.initial})        

    def selectArm(self):
        total_views = 0
        views = []
        counts = []

        for i in range(self.nArms):
            v = int(self.r.hget(f"{self.name}:arm:{i}", "views") or 0)
            c = int(self.r.hget(f"{self.name}:arm:{i}", "count") or 0)
            views.append(v)
            counts.append(c)
            total_views += v

        if 0 in views:
            return views.index(0)  # ensure each arm is tried at least once

        ucb_values = []
        for i in range(self.nArms):
            avg = counts[i] / views[i]
            bonus = self.c * math.sqrt((math.log(total_views)) / views[i])
            ucb_values.append(avg + bonus)
            self.r.hset(f"{self.name}:arm:{i}", "QEstimate", avg + bonus)

        return ucb_values.index(max(ucb_values))

    def update(self, chosen_arm, reward):
        self.r.hincrby(f"{self.name}:arm:{chosen_arm}", "count", reward)
        total_views = 0
        views = []
        counts = []

        for i in range(self.nArms):
            v = int(self.r.hget(f"{self.name}:arm:{i}", "views") or 0)
            c = int(self.r.hget(f"{self.name}:arm:{i}", "count") or 0)
            views.append(v)
            counts.append(c)
            total_views += v
        for i in range(self.nArms):
            avg = counts[i] / views[i]
            bonus = self.c * math.sqrt((math.log(total_views)) / views[i])
            self.r.hset(f"{self.name}:arm:{i}", "QEstimate", avg + bonus)
    
    def stats(self):
        statsDic = {}
        for arm in range(self.nArms):
            statsDic[arm] = self.redisClient.hgetall(f"{self.name}:arm:{arm}")
        return statsDic
