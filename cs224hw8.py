#!/usr/bin/python3
import sys
import unittest


def max(x, y):
	"""An auxiliary function that returns the maximum of 2 values.

	:rtype: int
	"""
	if x >= y:
		return x
	return y



def cut_rod( p, n ):
	""" Cutting rod problem: the naive, recursive solution that returns the maximum price.
	
	:param p: the array of prices, with $0 in position 0, and p_i in position i.
	:param n: length of rod for which a solution is to be computed (n < p.length)
	:type p: list
	:type n: int
	:rtype: int
	"""
	if n==0:
		return 0

	q = -(2**14)

	for i in range(1,n+1):
		q = max(q, p[i] + cut_rod(p, n-i ))
	return q




def memoized_cut_rod( p, n):
	""" Cutting rod problem: the memoized, recursive solution that returns the maximum price.
	
	:param p: the array of prices, with $0 in position 0, and p_i in position i.
	:param n: length of rod for which a solution is to be computed (n < p.length)
	:type p: list
	:type n: int
	:rtype: int
	"""
	# initializing the array of subresults with infinite negative values
	r = [ -2**14 for i in range(0,n+1) ]

	result = memoized_cut_rod_aux(p, n, r)

	return result



def memoized_cut_rod_aux(p, n, r):
	""" Cutting rod problem: the recursive part of the memoized, recursive solution that returns the maximum price.
	
	:param p: the array of prices, with $0 in position 0, and p_i in position i.
	:param n: length of rod for which a solution is to be computed (n < p.length)
	:param r: the memo, that stores the optimal price for length i at position i
	:type p: list
	:type n: int
	:type r: list
	:rtype: int
	"""
	
	if r[n] >= 0:
		return r[n]
	if n==0:
		q = 0
	else:
		q = -(2**14)
		for i in range(1, n+1):
			q = max(q, p[i] + memoized_cut_rod_aux(p, n-i, r))
	r[n] = q
	return q

def memoized_cut_rod_extended( p, n):
	""" Cutting rod problem: the memoized, recursive solution that returns the maximum price, as well at the solution array.

	The function returns a pair, i.e. a 2-tuple (price, s) where price is the optimal price for the given length n, and s is a list where an element at position i is the length of the optimal first cut for total rod length i.
	
	:param p: the array of prices, with $0 in position 0, and p_i in position i.
	:param n: length of rod for which a solution is to be computed (n < p.length)
	:type p: list
	:type n: int
	:rtype: tuple
	"""
	# initializing the array of subresults with infinite negative values
	r = [ -2**14 for i in range(0,n+1) ]

	# The solution array will store the optimal first cut for all 
	# lengths: by default, it associates to each length (indices 1 to 10)
	# the length itself, i.e. no cut at all
	s = list(range(0,(n+1)))

	price = memoized_cut_rod_extended_aux(p, n, r,s)

	return (price, s)


########### TODO: modify memoized_cut_rod_aux()  ########################
def memoized_cut_rod_extended_aux(p, n, r, s):
	""" Cutting rod problem: the recursive part of the memoized, recursive solution that returns the maximum price,
	and the solution array.

	This recursive subprocedure just returns the price, and maintains the solution array that is passed in as a parameter.

	:param p: the array of prices, with $0 in position 0, and p_i in position i.
	:param n: length of rod for which a solution is to be computed (n < p.length)
	:param r: the memo, that stores the optimal price for length i at position i
	:param s: the solution array, where an element at position i is the length of the optimal first cut for total rod length i
	:type p: list
	:type n: int
	:type r: list
	:type s: list
	:rtype: tuple
	"""

	
	if r[n] >= 0:
		return r[n]
	if n==0:
		q = 0
	else:
		q = -(2**14)
		for i in range(1, n+1):
			q = max(q, p[i] + memoized_cut_rod_aux(p, n-i, r))
			
	r[n] = q
	return q
	    
#####################################################

def bottom_up_cut_rod(p, n):
	""" Cutting rod problem: the bottom-up solution that returns the maximum price.
	
	:param p: the array of prices, with $0 in position 0, and p_i in position i.
	:param n: length of rod for which a solution is to be computed (n < p.length)
	:type p: list
	:type n: int
	:rtype: int
	"""
	r = [ None for i in range(0,n+1) ]
	r[0]=0
	
	for j in range(1, n+1):
		q = -(2**14)
		for i in range(1, j+1):
			q = max(q, p[i] + r[j-i])
		r[j] = q
	return r[n]

def extended_bottom_up_cut_rod(p, n):
	""" Cutting rod problem: the bottom-up solution that returns the maximum price, as well as the solution array.

	The function returns a pair, i.e. a 2-tuple (price, s) where price is the optimal price for the given length n, and s is a list where an element at position i is the length of the optimal first cut for total rod length i.
	
	:param p: the array of prices, with $0 in position 0, and p_i in position i.
	:param n: length of rod for which a solution is to be computed (n < p.length)
	:type p: list
	:type n: int
	:rtype: tuple
	"""
	r = [ None for i in range(0,n+1) ]
	r[0]=0
	s = [ None for i in range(0,n+1) ]
	
	for j in range(1, n+1):
		q = -(2**14)
		for i in range(1, j+1):
			if q < ( p[i] + r[j-i]):
				q = ( p[i] + r[j-i])
				s[j]=i
		r[j] = q
	index_table=list(range(0,n+1))
	index_table[0]=None
	return (r[n],s[n])

##### TODO ##########################################
def read_solution_array(s, n):
	""" Read a solution array, i.e. return the lengths of rod the pieces that make an optimal cut for length n, as a list.

	:param s: the solution array, a list where an element at position i is the length of the optimal first cut for total rod length i. 
	:param n: the length of rod for which a solution is to be read
	:rtype: list
	"""
	pass

############################################################

class Cut_Rod_Test( unittest.TestCase ):

	# a class attribute
	prices = [0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30]
	
	def test_cut_rod_naive_1(self):

		self.assertEqual( cut_rod(self.prices, 5), 13 )


	def test_cut_rod_naive_2(self):
			
		self.assertEqual( cut_rod(self.prices, 9), 25 )


	def test_memoized_cut_rod_1(self):
		
		self.assertEqual( memoized_cut_rod(self.prices, 5), 13 )
		
	def test_memoized_cut_rod_2(self):
		
		self.assertEqual( memoized_cut_rod(self.prices, 9), 25 )
		
	
	def test_bottom_up_cut_rod_1(self):
		
		self.assertEqual( bottom_up_cut_rod(self.prices, 5), 13 )
		
	def test_bottom_up_cut_rod_2(self):
		
		self.assertEqual( bottom_up_cut_rod(self.prices, 9), 25 )
		

	def test_memoized_cut_rod_extended_1(self):
		
		max_price, solution_array = memoized_cut_rod_extended(self.prices, 1)	
		self.assertEqual( max_price, 1 )
		self.assertEqual( solution_array, [0, 1])

	def test_memoized_cut_rod_extended_2(self):
		
		max_price, solution_array = memoized_cut_rod_extended(self.prices, 5)	
		self.assertEqual( max_price, 13 )
		self.assertEqual( solution_array, [0, 1, 2, 3, 2, 2 ])
		
	def test_memoized_cut_rod_extended_3(self):
		
		max_price, solution_array = memoized_cut_rod_extended(self.prices, 9)	
		self.assertEqual( max_price, 25 )
		self.assertEqual( solution_array, [0, 1, 2, 3, 2, 2, 6, 1, 2, 3] )
	
	def test_read_solution_array_1(self):
		
		max_price, solution_array = memoized_cut_rod_extended(self.prices, 9)	
		self.assertEqual( read_solution_array( solution_array, 1), [1])

	def test_read_solution_array_9(self):
		
		max_price, solution_array = memoized_cut_rod_extended(self.prices, 9)	
		self.assertEqual( read_solution_array( solution_array, 9), [3,6])



def main():
	unittest.main()

if __name__ == '__main__':
	main()


