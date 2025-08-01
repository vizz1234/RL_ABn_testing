import random

class eGreedy:

    def __init__(self, nArms, epsilon = 0.1, redisClient = None):

        self.nArms = nArms
        self.epsilon = epsilon
        self.redisClient = redisClient

        for i in range(nArms):
            key = f"eGreedy:arm:{i}"
            if not self.redisClient.exists(key):
                self.redisClient.hset(key, mapping = {"views": 0, "count": 0, "totalReward": 0})
    
    def selectArm(self):
        if random.random() < self.epsilon:
            return random.choice(self.nArms)

        # Exploitation
        bestArm = None
        bestValue = float('-inf')
        for arm in range(self.nArms):
            stats = self.redis.hgetall(f"eGreedy:arm:{arm}")
            count = int(stats.get(b'count', 0))
            rewardSum = float(stats.get(b'totalReward', 0.0))
            avgReward = rewardSum / count if count > 0 else 0.0
            if avgReward > bestValue:
                bestValue = avgReward
                bestArm = arm
        return bestArm

    def update(self, arm, reward):
        key = f"eGreedy:arm:{arm}"
        self.redis.hincrby(key, "count", 1)
        self.redis.hincrbyfloat(key, "totalReward", reward)
