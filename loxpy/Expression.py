"""
Abstract class Expression
Generated automatically at 12:10AM NZDT on Jan 25 2018
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from loxpy import Token


class Expression(object):
	def accept(self, visitor):
		raise NotImplementedError("This method should be called on dervied classes")


class Binary(Expression):
	def ___init__(self, left, op, right):
		if type(op) is not Token.Token:
			raise ValueError("op must be a token")
		self.left = left
		self.op = op
		self.right = right

	def __str__(self):
		s = []
		s.append("%s, %s, %s\n" % (str(self.left), str(self.op), str(self.right)))

		return "".join(s)

	def __repr__(self):
		return self.__str__()

	def __eq__(self, other):
		return self.__dict__ == other.__dict__

	def accept(self, visitor):
		visitor.visit(self)


class Grouping(Expression):
	def ___init__(self, expression):
		self.expression = expression

	def __str__(self):
		s = []
		s.append("%s\n" % (str(self.expression)))

		return "".join(s)

	def __repr__(self):
		return self.__str__()

	def __eq__(self, other):
		return self.__dict__ == other.__dict__

	def accept(self, visitor):
		visitor.visit(self)


class Literal(Expression):
	def ___init__(self, value):
		self.value = value

	def __str__(self):
		s = []
		s.append("%s\n" % (str(self.value)))

		return "".join(s)

	def __repr__(self):
		return self.__str__()

	def __eq__(self, other):
		return self.__dict__ == other.__dict__

	def accept(self, visitor):
		visitor.visit(self)


class Unary(Expression):
	def ___init__(self, op, right):
		if type(op) is not Token.Token:
			raise ValueError("op must be a token")
		self.op = op
		self.right = right

	def __str__(self):
		s = []
		s.append("%s, %s\n" % (str(self.op), str(self.right)))

		return "".join(s)

	def __repr__(self):
		return self.__str__()

	def __eq__(self, other):
		return self.__dict__ == other.__dict__

	def accept(self, visitor):
		visitor.visit(self)


