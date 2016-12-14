# Yang Xu
# SD @ Uol
# danliangchen@gmail.com

from agent import *
from strategy import *
from pulp import *
import random
import sys
import uuid
#import numpy as np
#import matplotlib.pyplot as plt
#import datetime

def play(payoff_matrix, player1, player2, termi_num):

	def payoff(p1,p2):
		payoff=0
		for s1 in p1.support():
		    payoffRow=0
		    for s2 in p2.support():
		    	payoffRow += payoff_matrix[s1.value][s2.value]*p2.values[s2.value]
		    payoff += p1.values[s1.value]*payoffRow
		return payoff

	count = 0
	iteration = 1

	while count < termi_num:
		print('----------------Iteration ',iteration,'----------------')

		T2 = player1.random_generate()
		T1 = player2.random_generate()

		print('p1: \n'+str(player1.piN)+'p2: \n'+str(player2.piN))

		E = payoff(T2,player2.piN) - payoff(player1.piN,T1)

		if E > 0:
			print('Find winning Strategy at this iteration\n\n')
			player1.W = T2
			player2.W = T1

			player1.updateWMN()
			player2.updateWMN()

			#--------------------------------------- Solve Player1 -------------------------------------
			# objective
			lpProb = LpProblem("solve" + str(uuid.uuid4()), LpMaximize)
			v = LpVariable("v", -100)
			lpProb += v 

			# init - player1's probabilities as lp variables
			player1_probabilities = []
			for i in player1.WMN:
				x = LpVariable('x'+str(i.value), 0, 1)
				player1_probabilities.append(x)

			# constrain - probabilities sum to 1
			total = 0
			for x in player1_probabilities: 
				total += x
			lpProb += total == 1

			# constrain - player2 try to minimise the payoff of player1
			for j in range(len(player2.WMN)):
				total = 0
				for i in range(len(player1.WMN)):
					total += payoff_matrix[i][j] * player1_probabilities[i] 
				lpProb += v <= total 

			# solve lp
			GLPK().solve(lpProb)

			for v in lpProb.variables():
				print('v: '+str(v)+'- '+str(v.varValue))
				for i in player1.WMN:
					if v.name == 'x'+ str(i.value):
						player1.piN.values[i.value] = v.varValue

			player1.updateWMN()

			#--------------------------------------- Solve Player1 -------------------------------------
			# objective
			lpProb2 = LpProblem("solve2" + str(uuid.uuid4()), LpMinimize)
			v2 = LpVariable("v2", -100)
			lpProb2 += v2 

			# init - player1's probabilities as lp variables
			player2_probabilities = []
			for i in player2.WMN:
				y = LpVariable('y'+str(i.value), 0, 1)
				player2_probabilities.append(y)

			# constrain - probabilities sum to 1
			total = 0
			for y in player2_probabilities: 
				total += y
			lpProb2 += total == 1

			# constrain - player1 try to maximize the payoff of it self
			for i in range(len(player1.WMN)):
				total = 0
				for j in range(len(player2.WMN)):
					total += payoff_matrix[i][j] * player2_probabilities[j] 
				lpProb2 += v2 >= total 

			# solve lp
			GLPK().solve(lpProb2)

			for v2 in lpProb2.variables():
				print('v2: '+str(v2)+'- '+str(v2.varValue))
				for i in player2.WMN:
					if v2.name == 'y'+ str(i.value):
						player2.piN.values[i.value] = v2.varValue

			player2.updateWMN()	
			
			#--------------------------------- Go Next Iteration -------------------------------
			iteration += 1

		else:
			print('No Winning Strategy at this iteration\n')
			iteration += 1
			count += 1

	print ('--------------Final solution---------------\n')
	print ('Payoff Matrix:')
	print (payoff_matrix,'\n')
	print('Player1: \n'+str(player1.piN)+'Player2: \n'+str(player2.piN))

def main():

	termi = 3
	m = 2
	n = 3

	payoff_matrix = []
	for i in range (m):
		r = []
		for j in range (n):
			r.append(random.randint(-10, 10))
		payoff_matrix.append(r)

	print ('the payoff matrix is')
	print (payoff_matrix)

	player1 = Agent(m, 'rowPlayer')
	player2 = Agent(n, 'colPlayer')

	play(payoff_matrix, player1, player2, termi)


if __name__ == "__main__":
		main()