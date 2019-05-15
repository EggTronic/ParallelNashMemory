# ParallelNashMemory
Use coevolutionary algorithm to teach model how to play paper rock and scissor game.
## agent.py
Specifies the WMN sets that will be used to solve the Nash Equilibrium problem from generation to generation:
- M keeps the supportor (models tend to win the game)
- N keeps the non-supportor (models tend to lose the game)
- W keeps the current generation's winner

## main.py (import strategy.py)
Randomly gennerate 2 models with random stragey (probilities to play rock/paper/sicssor which sums to 1)

Then let 2 models compete and update their stragey to beat the each other suntil the final Nash Equilibrium is reached.
And it will ends up with both models play a stragey of 1/3 paper, 1/3 rock and 1/3 sicssor.
