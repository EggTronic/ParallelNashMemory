# Yang Xu
# SD @ Uol
# danliangchen@gmail.com

from agent import *
from strategy import *
import random
import sys
import numpy as np
import matplotlib.pyplot as plt
import datetime
from pulp import *
import uuid

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

	while count < termi_num:
		T2 = player1.random_generate()
		T1 = player2.random_generate()

		E = payoff(T2,player2.piN) + payoff(T1,player1.piN)

		if E > 0:
			player1.W = T2
			player2.W = T1

			player1.updateWMN()
			player2.updateWMN()

			sub_matrix = []
			for i in player1.WMN:
				row = []
				for j in player2.WMN:
					row.append(payoff_matrix[i.value][j.value])
				sub_matrix.append(row)

			print('Sub Matrix')
			print(sub_matrix)

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
					total += M[i][j] * player1_probabilities[i] 
				lpProb += v <= total 

			# solve lp
			GLPK().solve(lpProb)

			for v in lpProb.Variables():
				for i in player1.WMN:
					if v.name == 'x'+ str(i.value):
						player1.piN.values[i.value] = v.varValue

			player1.updateWMN()

			# objective
			lpProb2 = LpProblem("solve" + str(uuid.uuid4()), LpMaximize)
			v2 = LpVariable("v", -100)
			lpProb2 += v2 

			# init - player1's probabilities as lp variables
			player2_probabilities = []
			for i in player2.WMN:
				y = LpVariable('y'+str(i.value), 0, 1)
				player2_probabilities.append(y)

			# constrain - probabilities sum to 1
			total = 0
			for y in player1_probabilities: 
				total += y
			lpProb2 += total == 1

			# constrain - player1 try to maximize the payoff of it self
			for i in range(len(player1.WMN)):
				total = 0
				for j in range(len(player2.WMN)):
					total += M[i][j] * player2_probabilities[j] 
				lpProb2 += v2 >= total 

			# solve lp
			GLPK().solve(lpProb2)

			for v2 in lpProb2.Variables():
				for i in player1.WMN:
					if v2.name == 'x'+ str(i.value):
						player1.piN.values[i.value] = v2.varValue

			player2.updateWMN()


		else:
			count += 1

	print (payoff_matrix)
	print ('P1 :', player1.piN)
	print ('P2 :', player2.piN)
			

	

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