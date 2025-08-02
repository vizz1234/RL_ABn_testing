import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math
import random

# Simulated true rewards for 3 arms
true_rewards = [0.4, 0.6, 0.5]
counts = [1, 1, 1]  # Initialize with 1 to avoid division by zero
q_estimates = [0, 0, 0]  # Optimistic initialization (optional)
views_history = [[], [], []]
iterations = 1000
c = 2  # Exploration constant
already_run = set()

fig, ax = plt.subplots()

def select_arm_ucb(t):
    ucb_values = []
    for i in range(3):
        average = q_estimates[i]
        bonus = c * math.sqrt(math.log(t) / counts[i])  # +1 to avoid log(0)
        ucb_values.append(average + bonus)
    return ucb_values.index(max(ucb_values))

def update_estimate(arm, reward):
    counts[arm] += 1
    q_estimates[arm] += (reward - q_estimates[arm]) / counts[arm]

def animate(frame):
    if frame in already_run:
        return
    already_run.add(frame)
    ax.clear()
    arm = select_arm_ucb(frame + 1)
    reward = 1 if random.random() < true_rewards[arm] else 0
    update_estimate(arm, reward)

    for i in range(3):
        views_history[i].append(counts[i] - 1)
        ax.plot(views_history[i], label=f'Arm {i} (Q={q_estimates[i]:.2f}), views = {views_history[i][-1]}')

    ax.set_xlim(0, iterations)
    ax.set_ylim(0, max(sum(counts), 1))
    ax.set_title(f"UCB (c = {c}) | Iteration {1 + frame}")
    ax.legend()

ani = FuncAnimation(fig, animate, frames=iterations, repeat=False, interval=1)
plt.show()
