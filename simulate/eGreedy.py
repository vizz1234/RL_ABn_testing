import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

# Simulated true rewards for 3 arms
true_rewards = [0.4, 0.6, 0.5]
counts = [1, 1, 1]
q_estimates = [2, 2, 2]

eps = 0.1
views_history = [[], [], []]
iterations = 1000

fig, ax = plt.subplots()

def select_arm():
    if random.random() < eps:
        return random.randint(0, 2)
    return q_estimates.index(max(q_estimates))

def update_estimate(arm, reward):
    counts[arm] += 1
    q_estimates[arm] += (reward - q_estimates[arm]) / counts[arm]

def animate(frame):
    ax.clear()
    arm = select_arm()
    reward = 1 if random.random() < true_rewards[arm] else 0
    update_estimate(arm, reward)

    for i in range(3):
        views_history[i].append(counts[i] - 1)
        ax.plot(views_history[i], label=f'Arm {i} (Q={q_estimates[i]:.2f}), views = {views_history[i][-1]}')

    ax.set_xlim(0, iterations)
    ax.set_ylim(0, max(sum(counts), 1))
    ax.set_title(f"Epsilon-Greedy | Iteration {frame}")
    ax.legend()

ani = FuncAnimation(fig, animate, frames=iterations, repeat=False, interval=3)
plt.show()
