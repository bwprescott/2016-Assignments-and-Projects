#!/usr/bin/python3
class OverflowException( Exception): pass
class UnderflowException( Exception): pass

class Queue():

	def __init__(self,size):
		self.tail=0
		self.head=0
		self.array=[None]*size


	def is_empty(self):
		return self.head==self.tail
		

	def enqueue(self, x):
		if (self.head==1 and self.tail==len(self.array)) or (self.tail+1==self.head):
			raise OverflowException()
			
		self.array[self.tail] = x
		if self.tail == len(self.array)-1:
			self.tail = 0
		else:
			self.tail = self.tail + 1

	def dequeue(self):
		if (self.head==self.tail):
			raise UnderflowException()
		x = self.array[self.head]
		# just for clarity
		if self.head == len( self.array)-1:
			self.head=0
		else:
			self.head = self.head+1

		return x

	def __str__(self):
		output = ''
		# no wrap-around
		print( 'H:{} T:{}'.format(self.head, self.tail))
		if self.tail is self.head:
			return ''
		if self.tail==0 or self.head < self.tail:
			for el in self.array[self.head:self.tail]:
				output += (','+ str(el))
			return output
		# wrap-around
		for el in self.array[self.head:]:
			output += (','+str(el))
		for el in self.array[0:self.tail]:
			output += (','+str(el))
		return output


