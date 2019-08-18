#!/usr/bin/python3
import unittest


def recursive_length( x, y ):
	"""
	A naive, recursive solution to the LCS problem: return the length of an LCS of x and y.

	:param x: the X sequence, as a list of characters
	:param y: the y sequence, as a list of characters
	:type x: list
	:type y: list
	:rtype: int
	"""
	if len(x) == 0 or len(y) == 0:
		return 0
	if x[-1] == y[-1]:
		return recursive_length( x[0:-1], y[0:-1]) + 1
	if x[-1] != y[-1]:
		max_length = recursive_length( x[0:-1],y)
		length2 = recursive_length( x,y[0:-1])
		if length2 > max_length:
			max_length = length2
		return max_length

def recursive_length_memoized(x, y):
	"""
	A naive, recursive solution to the LCS problem: return the length of an LCS of x and y.

	:param x: the X sequence, as a list of characters
	:param y: the y sequence, as a list of characters
	:type x: list
	:type y: list
	:rtype: int
	"""
	## YOUR CODE HERE

	# Use the code of recursive_length() function (above) as the basis of a inner, recursive procedure.
	# Then call it with the proper parameters - and do not forget to return the result.
	#
	# You will typically have to initialize a matrix of subresults, that you can then pass
	# to the recursive procedure, that will in turn update and read it. You can look at the
	# cutrod() code for inspiration.

	if len(x) >= len(y):
		r = [ -2**14 for i in range(0,x+1) ]
	else:
		r = [ -2**14 for i in range(0,y+1) ]

	result = recursive_length_memoizedAUX(x, y, r)

	return result
	

def recursive_length_memoizedAUX(x, y, r): 
	if len(x) == 0 or len(y) == 0:
		return 0
	if x[-1] == y[-1]:
		return recursive_length_memoizedAUX( x[0:-1], y[0:-1], r) + 1
	if x[-1] != y[-1]:
		max_length = recursive_length_memoizedAUX( x[0:-1],y, r)
		length2 = recursive_length_memoizedAUX( x,y[0:-1], r)
		if length2 > max_length:
			max_length = length2
		return max_length

	
class LCS_Test( unittest.TestCase ):


	X1=['A','B','C','B','D','A','B']
	Y1=['B','D','C','A','B','A']

	X2= ['C','G','G','A','A','T','G','C','C','G']
	Y2= ['C','G','G','T','C','G','A','G']

	X3= ['A','A','G','A','A','T','G','C','G','A']
	Y3= ['C','G','G','A','C','G','A','G']


	def test_recursive_length_1( self ):
		self.assertEqual( recursive_length(self.X1, self.Y1), 4 )
		
	def test_recursive_length_2( self ):
		self.assertEqual( recursive_length(self.X2, self.Y2), 6 )

	def test_recursive_length_3( self ):
		self.assertEqual( recursive_length(self.X3, self.Y3), 5 )


	def test_recursive_length_memoized_1( self ):
		self.assertEqual( recursive_length_memoized(self.X1, self.Y1), 4 )
		
	def test_recursive_length_memoized_2( self ):
		self.assertEqual( recursive_length_memoized(self.X2, self.Y2), 6 )

	def test_recursive_length_memoized_3( self ):
		self.assertEqual( recursive_length_memoized(self.X3, self.Y3), 5 )



def main():
	unittest.main()

if __name__ == '__main__':
	main()


