<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>N - Arm Bandits using Reinforcement Learning</title>
  <style>
    body { font-family: Arial, sans-serif; line-height: 1.6; max-width: 900px; margin: auto; padding: 20px; }
    h1, h2, h3 { color: #2c3e50; }
    img { max-width: 100%; height: auto; margin: 10px 0; }
    code, pre { background: #f4f4f4; padding: 4px; border-radius: 4px; }
    p.center { text-align: center; }
  </style>
</head>
<body>
  <h1>Solving N - Arm Bandits Problem Using Reinforcement Learning</h1>
  <p>This article primarily follows the ideas and tries to replicate results from <strong>Reinforcement Learning: An Introduction</strong>, book by Andrew Barto and Richard S. Sutton. The objective here is to further simplify the concepts by showing code implementations which can make the learning a lot easier. There might also be some additional concepts which are not covered in the said book.</p>

  <p>Before solving multi-arm bandits problem or n-bandits problem, let us familiarize ourselves with some of the basic RL foundations. </p>

  <h2>The Reinforcement Learning Problem</h2>
  <p>Reinforcement Learning (RL) in simple sense is a problem where an agent interacts with the environment and takes actions that affect the state that agent is currently in inorder to achieve an objective or goal (Maximizing reward signals). In essense, if a problem includes <strong>sensation</strong>, <strong>action</strong> and <strong>goal</strong> then it can be formulated as a reinforcement problem.</p>

<p><strong>RL</strong> is a different paradigm that either <strong>supervised</strong> or <strong>unsupervised</strong> learning. Supervised Learning is learning from data that has already been categorized; Unsupervised Learning is finding hidden structures in the data that has no labels. Though both of these are important types of learning, they are not enough to learn through interation and to maximize <strong>reward signal</strong>. Hence, reinforcement learning is often considered as the third paradigm of <strong>Machine Learning</strong>. </p>

  <img src="./images/RL_paradigm.png" alt="RL Paradigm">

  <h3>Exploration and Exploitation</h3>

  <p>One of the trade-offs and challenges in reinforcement learning is <strong>Exploration</strong> and <strong>Exploitation</strong>. As mentioned before, the agent tries to reach the goal by taking actions that provide maximum reward. But to discover such actions, it has to explore other possible actions. One might wonder, why not try all actions and choose the one that is the best. This is often computationally not feasible because of the vast number of states and actions (Backgammon approximately has 10<sup>20</sup> states). Even if the agent has tried all the actions applicable in a state in the past and has the knowledge of the best action, it still has to try other actions if the environment is non stationary (environment changes with time)</p>
  
  <p>Hence, the dilemma; to explore or to exploit. In simple terms, exploit is to take decisions based on known knowledge and explore is to go down other path even when it is known the other action at this particular state might not yield the best possible reward in order to get better reward in the future. So, look out for exploration and exploitation in all the algorithms of reinforcement learning to better understand balancing of the trade-offs. One thumb rule is to have more weightage in favor of exploration if uncertainty is high (initially, when the action values are unknown) and exploit otherwise. This is shown in the following image. The blue arrows represent the actions explored and orange represents the action with the highest value.</p>

  <img src="./images/exploration_v_exploitation.png" alt="exprn vs expltn">

  <h3>Elements of Reinforcement Learning</h3>
  <ul>
    <li><strong>Policy:</strong> Mapping of perceived states to actions that are taken in those states.</li>
    <li><strong>Reward Signal:</strong> Environment sends rewards to an RL agent upon taking action in a state at different time steps. This is usually a real number. The agent's objective is to maximize the total reward it gets in the long haul.</li>
    <li><strong>Value Function:</strong> Reward is usually immediate, i.e, the agent gets the reward after taking an action in a particular state at a particular time. Value Function, however, tells what is the expected rewards an agent can achieve from the said state in the long run. Based on values, decisions are made, i.e, an agent takes actions that produce highest value.</li>
    <li><strong>Model (optional):</strong> The model imitates the environment, i.e, given an action in a state, the model predicts the next state and reward. This learning that uses <strong>planning</strong> and <strong>models</strong> is called model-based learning where future states or situations are considered without even experiencing it. In contast, model-free methods are usually considered opposite of planning, where an agent learns explicitly by trial-and-error.</li>
  </ul>

  <h2>Tabular Solution Methods</h2>
  <p>In the case where state and action spaces are relatively small, they can be represented in an array or a table. This gives an opportunity to understand the core ideas of RL algortihms, atleast in their simplest forms.</p>
  <p>One more feature that distinguishes RL from other learnings is that it learns on training information that <strong>evaluates</strong> the actions rather than <strong>instruct</strong> the action in a particular state at a specific time. This creates the need for active exploration.</p>
  <p>In this problem, evaluative feedback is presented in the simple setting, where the agent has to learn to act only in one situation (non-associate setting), i.e, N-armed bandits problem.</p>
  <p>While not a full reinforcement learning problem (no states or transitions), the N-armed bandit problem forms a foundational case for understanding action selection and exploration strategies in RL.</p>

  <h2>N - Armed Bandit Problem</h2>
  <p>N - arm bandits originally refers to a <strong>casino slot machine</strong> where instead of one lever, there are n levers (actions). After each action selection, there is a reward according to the stationary probability distribution. The agent's goal is to maximize total reward over m steps. In this case, 1000 steps, and thereby selecting 1000 actions.</p>
  <p>  Here casino slot is referred, however, there are many applications of the same. For instance, the same problem can be formulated for online advertising;</p>
 
- **n-arm or actions:** n-ads.
- **rewards:** clicks, purchases, etc. 
- **goal:** Maximize total engagement over time.

 <p>Python is used to implement the solution. In the below image, the bandit class is initialized with <strong>k</strong> arms or actions. The <strong>k</strong> actions are assigned normally distributed rewards with mean 0 and variance 1. It also has <strong>pull</strong> method that takes an action and returns the reward that has some additional noise. This is due to the fact that real-world actions often have uncertainty. In this instance, pulling a casino lever may not give same payout every time. Note that this is just the casino slot set-up, how the action is selected, is taken care by the agent algorithm.</p>

  <img src="./images/bandit_class.png" alt="Bandit class initialization">

  <p>There are multiple solutions to this problem. In this articles, three of them will be discussed; <strong>ε-greedy</strong>, <strong>Upper Confidence Bound</strong>, <strong>Gradient Bandits</strong>. These are also known as action selection methods as the agent is choosing different actions with unknwon rewards.</p>

  <h2><strong>&epsilon;-greedy</strong></h2>
  <p>The agent estimates the value of actions with sample averages. It selects the best action most of the time but randomly explores others with a probability &epsilon;.</p>
  <p>Let <strong>q(a)</strong> represent true value, and <strong>Q(a)</strong> for estimated value. Simple way to estimate <strong>Q(a)</strong> is to average the rewards when that particular action is selected. If action <strong>a</strong> has been chosen <strong>N<sub>t(a)</sub></strong>, getting rewards <strong>R<sub>1</sub>, R<sub>2</sub>, R<sub>2</sub>, ...., R<sub>Nt(a)</sub></strong>, then</p>

  <p class="center">
    <img src="https://latex.codecogs.com/svg.image?Q_{t}(a)=\frac{R_1+R_2+\cdots+R_{N_t(a)}}{N_t(a)}" alt="Q(a)"><br>
    <strong>Equation (1):</strong> Sample average estimate of action value
  </p>
  
  <p>If N<sub>t(a)</sub> = 0, then Q<sub>t(a)</sub> is defined as some default value. In this problem we define it as 0. If N<sub>t(a)</sub> tends to ∞, then by law of large numbers, Q<sub>t(a)</sub> converges to its true value <sub>q(a)</sub>.

The obvious choice to select action is the one with the highest Q<sub>t(a)</sub>, this is also known as <em>greedy</em> action selection. As it was made clear in the earlier sections, the algorithm has to balance exploration and exploitation. Hence, the agent selects one of the actions randomly with equal probability regardless of the estimate. This is done with probability ε, and with probability 1-ε, the action with the highest estimate is selected.

To have incremental update to the simple average estimate, modifying the above formula, we have</p>
  
  <p class="center">
    <img src="https://latex.codecogs.com/svg.image?Q_{t+1}(a)=Q_t(a)+\alpha(R_t-Q_t(a))" alt="Incremental Update Rule"><br>
    <strong>Equation (2):</strong> Incremental update rule
  </p>

  <p class = "center"> 
  <img src="https://latex.codecogs.com/svg.image?In\ Eq\ 2,\  \alpha = \frac{1}{N_{t(a)}}" alt="unbiased alpha">

<p>Notice that it is <em>R<sub>t</sub></em> and not <em>R<sub>t+1</sub></em> as <em>Q<sub>1</sub>=0</em>. Alpha(𝛼) is the step size parameter that is equal to N<sub>t(a)</sub>. Below is the image of implementation details in python.</p>

  <img src="./images/epsilon_greedy_agent.png" alt="Epsilon Greedy Agent">

  <p>Now that we have the set-up, let us simulate the experiment. One more thing to note here is that, the experiment is carried out 2000 times, with 1000 steps or iterations each time. These are then averaged out to get the better approximate. This set up will help in visualizing the performance much better (A single run can be extremely noisy and can lead to misleading conclusions especially since the problem has inherent randomness and the agent can get lucky or unlucky based on initial estimates. So, many runs are performed and then averaged to get clear picture). Find the implementation in the picture below.</p>

  <img src="./images/simulate.png" alt="Simulate">

  <p>Lets run the algorithm</p>
  <img src="./images/setup.png" alt="Setup">

  <h3>&epsilon;-greedy Results</h3>
  <p>Now that the algorithm and the problem set-up is familiarized, let us look into results.</p>
  <img src="./images/eps_greedy_avg_reward_overtime.png" alt="Avg Reward">
  <img src="./images/eps_greedy_per_opt_action_chosen.png" alt="Opt Action">
  <p>The above plots give a lot of information as to the performance of greedy and ε-greedy methods. As seen, greedy implementation (ε=0) gets stuck at about 1, when the best reward is around 1.55. This however, depends on the task, if the reward had 0 variance instead of 1, then greedy would instantly after trying that action. On the contrary, it would perform extremely poor if the variance was higher as it needs more exploration. One more thing to note here is that the ε=0.01 eventually performs better than ε=0.1 in both metrics.</p>

  <h3>Tracking Non - Stationary Problem</h3>
  <p>The above implementation works well when the problem is stationary, however, if the environment changes over time, i.e, there is new best action after <strong>t</strong> steps, then, even ε-greedy would take a lot of steps to correct the course as the sample-average method implemented above is unbiased; it considers all rewards as equally important. In non-stationary problem, we need an agent that gives more <em>weightage</em> to recent rewards than the earlier ones. This can be achieved simply by having constant alpha in Equation 2. Here 𝛼 belongs to (0, 1]. 

If 𝛼 is near 0, then the new rewards have very little influence marking slow learning. If it is near 1, then new rewards have very high influence in updating the estimates.</p>

  <h3>Optimistic Initial Values</h3>
  <p>The above formulations have bias to the initial estimate, although for sample-average methods the bias disappears early, for constant <em>step-size (𝛼)</em>, the bias decreases very slowly over time and it will be permanent if very few steps are in each run. 

This is not bad all the times, as it might lead to natural exploration without the need for ε. If the initial values are higher (optimistic), then when the agent starts getting reward that is lower (true rewards), the agent looks for other actions as the other action still have higher value, thanks to the optimistic start.

With the below plots, it can be seen that even if ε=0, the agent manages to get much closer to true reward and even has much higher optimal action selection percentage than before. This set up was done with constant alpha of value 0.1. The results can also be verified for sample-average methods as well i.e, 𝛼 = 1/N (the plots might not be the same, but the performance is still far better than without optimistic initialization).</p>
  <img src="./images/opm_avg_reward.png" alt="Optimistic Avg Reward">
  <img src="./images/opm_opt_sel.png" alt="Optimistic Opt Action">

  <h2>Upper Confidence Bound (UCB)</h2>
  <p>Exploration is essential when the action value estimates have uncertainty. While ε-greedy mitigates this problem to a great extent as seen previously, it does so, randomly, without considering the promising nature of the action, i.e, we would like to explore actions that have high chance of being closer to optimal or have higher uncertainty as they might potentially be the optimal or best choice.</p>

  <p class="center">
    <img src="https://latex.codecogs.com/svg.image?A_t%20=%20\arg\max_a\left[Q_t(a)%20+%20c%20\cdot%20\sqrt{\frac{\ln%20t}{N_t(a)}}\right]" alt="UCB Equation"><br>
    <strong>Equation (3):</strong> UCB Action Selection
  </p>

<p>UCB is an effective way of doing this. This is the action selection rule used in UCB algorithms, where:</p>

<ul>
  <li>Q<sub>t(a)</sub> is the estimated value of action 𝑎 at time <em>t</em></li>
  <li>N<sub>t(a)</sub> is the number of times action a has been selected up to time 𝑡, same as before.</li>
  <li>c is a hyperparameter controlling the level of exploration.</li>
</ul>

<p><em>Square root</em> term is the measure of uncertainty and decides exploration (along with c). If N<sub>t(a)</sub> is small then square root term is big, making the agent <strong>explore</strong> this action. Smaller c means more exploitation, larger c makes the agent explorer. This might, however, shrink overtime as enough information about action is known. This can also be considered as <em>uncertainty bonus</em>.</p>

<p>From below graphs, it can be seem UCB performs better than &epsilon;-greedy for both metrics.</p>


  <img src="./images/ucb_avg_reward.png" alt="UCB Avg Reward">
  <img src="./images/ucb_opt_sel.png" alt="UCB Opt Action">

  <p>One thing to note here is that the equation 3 is for action selection, the update rule even for UCB is same as equation 2.</p>

<p>Even though UCB performs better than ε-greedy, the difficulty arises in non-stationary problem and it is more complex to implement in this case than the techniques mentioned before (regardless of the fact that α is constant, the exploration bonus still decays irreversibly with N<sub>t</sub>(a)). In functional approximation methods with advanced settings, there is no known implementation of UCB action selection.</p>


  <h2>Gradient Bandits</h2>
<p><strong>Gradient Bandits</strong> are a class of algorithms in reinforcement learning that take a different approach from estimating action values (like Q-values). Instead of learning the expected reward of each action, they learn preferences H<sub>t</sub>(a) for actions, and use these preferences to form a probability distribution over actions. The probability of selection is proportional to the preference.</p>

<p>Here, the numerical value of preferences do not hold much meaning, only its relative value to other actions.</p>

<p>The preferences are converted to probabilities using softmax function.</p>


  <p class="center">
    <img src="https://latex.codecogs.com/svg.image?\pi_t(a)&space;=&space;\frac{e^{H_t(a)}}{\sum_b&space;e^{H_t(b)}}" alt="Softmax Policy"><br>
    <strong>Equation (4):</strong> Softmax Policy
  </p>

  <p>Initially, all probabilities are same so that all actions have an equal probability of being selected, i.e, H(a) = 0 for all actions.</p>

<p><em>Stochastic Gradient Ascent</em> is used to update the preferences (stochastic gradient descent as in most supervised learning algorithms so as to minimize the loss, here we are trying to maximize the expected reward).</p>

  <p class="center">
    <img src="https://latex.codecogs.com/svg.image?H_{t+1}(A_t)%20=%20H_t(A_t)%20+%20\alpha%20(R_t%20-%20\bar{R}_t)(1%20-%20\pi_t(A_t))" alt="Update Selected"><br>
    <strong>Equation (5):</strong> Update for selected action
  </p>

  <p class="center">
    <img src="https://latex.codecogs.com/svg.image?H_{t+1}(a)%20=%20H_t(a)%20-%20\alpha%20(R_t%20-%20\bar{R}_t)%20\pi_t(a),\quad\text{for }a\ne A_t" alt="Update Non-selected"><br>
    <strong>Equation (6):</strong> Update for non-selected actions
  </p>

<p>Typically α is constant in gradient bandits implementation. One more thing to pay attention here is that the average reward &#772;R<sub>t</sub> , is the average of all rewards received up to time t, regardless of which action was taken. &#772;R<sub>t</sub> is also the <strong>baseline</strong>. Baseline is a reference value used to reduce the variance of the updates to the preference values.</p>

<p>With mathematical calulations, it can be shown that gradient bandits solution has robust convergence properties.</p>
</body>
</html>
