# Yang Xu
# SD @ Uol
# danliangchen@gmail.com

import random
import copy

class PureStrategy (object):
	def __init__ (self, value):
		self.value = value

	def convertToMixed(self):
		ms = MixedStrategy()
		ms.values[value] = 1
		return ms

	def __str__(self): # override the default printing function
		return str(self.value)

	def __eq__(self, other): 
		return (self.value == other.value)

	def __hash__(self):
		return self.value


class  MixedStrategy (object):
	def __init__ (self):
		self.values = {}

	def assign(self, size):
		percentage = {}
		total = 0
		for i in range(size):
			self.values[i] = 0
		for i in range(size):
			strategy = random.randint(0,size-1)
			weight = random.randint(0,5)
			percentage[strategy] = weight
			total += weight
		for strategy in percentage.keys():
			self.values[strategy] = percentage[strategy]/total

	def support(self):
		l = set()
		for k in self.values.keys():
			if self.values[k] != 0:
				l.add(PureStrategy(value = k))
		return l

		
	def not_support(self):
		l = set()
		for k in self.values.keys():
			if self.values[k] == 0:
				l.add(PureStrategy(value = k))
		return l
