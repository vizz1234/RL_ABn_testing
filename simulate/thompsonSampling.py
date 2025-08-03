import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import random
from scipy.stats import beta

# Simulated true rewards for 3 arms
true_rewards = [0.4, 0.6, 0.5]
successes = [1, 1, 1]  # Beta(1,1) prior
failures = [1, 1, 1]
views_history = [[], [], []]
iterations = 1000

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
x_vals = np.linspace(0.001, 0.999, 200)

already_run = set()

def select_arm_ts():
    samples = [np.random.beta(successes[i], failures[i]) for i in range(3)]
    return np.argmax(samples)

def update(arm, reward):
    if reward == 1:
        successes[arm] += 1
    else:
        failures[arm] += 1

def animate(frame):
    # Avoid double-call for frame=0
    if frame in already_run:
        return
    already_run.add(frame)

    ax1.clear()
    ax2.clear()

    arm = select_arm_ts()
    reward = 1 if random.random() < true_rewards[arm] else 0
    update(arm, reward)

    all_views = 0

    # --- Top plot: View counts ---
    for i in range(3):
        total_views = successes[i] + failures[i] - 2
        all_views += total_views
        views_history[i].append(total_views)
        # print(f'iteration: {frame}, arm: {i}, views: {total_views}, all_views: {all_views}')
        ax1.plot(views_history[i], label=f'Arm {i} (views = {total_views})')

    ax1.set_xlim(0, iterations)
    ax1.set_ylim(0, max(sum(successes[i] + failures[i] - 2 for i in range(3)), 1))
    ax1.set_title(f"Thompson Sampling | Iteration {1 + frame}")
    ax1.legend()

    # --- Bottom plot: Beta distributions with variance ---
    for i in range(3):
        alpha, b = successes[i], failures[i]
        y_vals = beta.pdf(x_vals, alpha, b)

        mean = alpha / (alpha + b)
        var = (alpha * b) / ((alpha + b) ** 2 * (alpha + b + 1))
        std_dev = np.sqrt(var)

        ax2.plot(x_vals, y_vals, label=f'Arm {i} (mean = {mean:.2f}, var = {var:.4f})')
        ax2.axvline(mean, color=f'C{i}', linestyle='--', alpha=0.6)

    ax2.set_title("Beta Distributions (Posterior with Variance)")
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, None)
    ax2.legend()

ani = FuncAnimation(fig, animate, frames=iterations, repeat=False, interval=1)
plt.tight_layout()
ani.save("ts.mp4", writer="ffmpeg", fps=60)
plt.show()
