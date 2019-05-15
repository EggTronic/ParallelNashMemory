# ParallelNashMemory
Use coevolutionary algorithm to teach model how to play paper rock and scissor game.
## agent.py
Specifies the WMN sets where:
- M keeps the supportor (those models who are tend to win the game)
- N keeps the non-supportor (those models who are tend to lose the game)
- W keeps the current generation's winner

## main.py (import strategy.py)
Randomly gennerate 2 models with random stragey (probilities to play rock/paper/sicssor which sums to 1)
Let 2 models compete and update their stragey based on the other's until the Nash Equilibrium is reached.
And it will ends up with both models play a stragey of 1/3 paper, 1/3 rock and 1/3 sicssor.
