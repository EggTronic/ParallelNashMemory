# Yang Xu
# SD @ Uol
# danliangchen@gmail.com

import random
import sys
from pulp import *
from strategy import *
from pulp import *
import uuid

class Agent:
	def __init__ (self, size, name):
		self.size = size
		self.name = name
		self.piN = MixedStrategy()
		self.piN.assign(self.size)
		self.N = set()	
		self.M = set()
		self.W = None
		self.WMN = set()

	def updateWMN(self):
		self.WMN = set()
		self.N = self.piN.support()
		self.M = self.piN.not_support()
		self.WMN |= self.N
		self.WMN |= self.M 
		if self.W != None:
			self.WMN |= self.W.support()
		
	def random_generate(self):
		ms = MixedStrategy()
		ms.assign(self.size)
		return ms


