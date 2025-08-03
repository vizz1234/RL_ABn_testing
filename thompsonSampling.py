import numpy as np

class thompsonSampling:

    def __init__(self, nArms, redisClient=None, name='thompsonSampling', alpha=1, beta=1):
        self.nArms = nArms
        self.redisClient = redisClient
        self.name = name
        self.alpha = alpha
        self.beta = beta

        for i in range(self.nArms):
            key = f"{self.name}:arm:{i}"
            if not self.redisClient.exists(key):
                self.redisClient.hset(key, mapping={
                    "successes": 0,
                    "failures": 0,
                    "views": 0  # for logging purposes
                })

    def selectArm(self):
        sampled_values = []
        for arm in range(self.nArms):
            key = f"{self.name}:arm:{arm}"
            successes = int(self.redisClient.hget(key, "successes") or 0)
            views = int(self.redisClient.hget(key, "successes") or 0)
            failures = views - successes
            sample = np.random.beta(successes + self.alpha, failures + self.beta)
            sampled_values.append((sample, arm))
        # Pick arm with highest sample
        _, selected_arm = max(sampled_values)
        return selected_arm

    def update(self, arm, reward):
        key = f"{self.name}:arm:{arm}"
        if reward > 0:
            self.redisClient.hincrby(key, "successes", 1)
            
        views = int(self.redisClient.hget(key, "views") or 0)
        s = int(self.redisClient.hget(key, "successes") or 0)
        self.redisClient.hset(key, "failures", views - s)

    def stats(self):
        statsDic = {}
        for arm in range(self.nArms):
            statsDic[arm] = self.redisClient.hgetall(f"{self.name}:arm:{arm}")
        return statsDic
