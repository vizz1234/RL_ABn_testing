import random

class eGreedy:

    def __init__(self, nArms, epsilon = 0.1, redisClient = None, initial = 5):

        self.nArms = nArms
        self.epsilon = epsilon
        self.redisClient = redisClient
        self.initial = initial

        for i in range(self.nArms):
            key = f"eGreedy:arm:{i}"
            if not self.redisClient.exists(key):
                self.redisClient.hset(key, mapping = {"views": 0, "count": 0, "avgReward": self.initial})
    
    def selectArm(self):
        if random.random() < self.epsilon:
            armExplored = random.choice(list(range(self.nArms)))
            print(f"Exploring: {armExplored}")
            return armExplored
        print("Exploitation")
        # Exploitation
        bestArm = None
        bestValue = float('-inf')
        for arm in range(self.nArms):
            stats = self.redisClient.hgetall(f"eGreedy:arm:{arm}")
            count = int(stats.get('count', 0))
            views = int(stats.get('views', 0))
            avgReward = (count + self.initial) / views if views > 0 else self.initial
            if avgReward > bestValue:
                bestValue = avgReward
                bestArm = arm
        print(f'Exploiting: {bestArm}')
        return bestArm

    def update(self, arm, reward):
        key = f"eGreedy:arm:{arm}"
        self.redisClient.hincrby(key, "count", 1)
        self.redisClient.hincrbyfloat(key, "totalReward", reward)
