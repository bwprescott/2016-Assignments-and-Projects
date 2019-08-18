#!/usr/bin/python3

import unittest
import math
from queue import *

class Node():

	def __init__(self, key=None, left=None, right=None, parent=None,depth=0):
		""" Initializes a new node """
		self.key = key
		self.left = left
		self.right = right
		self.parent = parent
		self.depth=depth

	
	def add_left(self, left ):
		""" Helper function: create a L child  """
		self.left = left
		left.parent = self
		left.depth = self.depth + 1

	def add_right(self, right ):
		""" Helper function: create a R child  """
		self.right = right
		right.parent = self
		right.depth = self.depth + 1

	def __str__(self):
		return str(self.key)


class BinaryTree():
	
	def __init__(self, root=None, array=None):
		""" Initializes an empty tree 
		
		:param root: the root node reference
		:type root: Node
		:param array: (optional) if provided, a tree, in the form of nested lists
		:type array:  tuple
		"""
		self.root = root
		self.height=-1

		if array is not None:
			self.update_from_array( array )

	################## TODO #####################################
	def is_bst( self ):
		""" Check for BST property, recursively

		1. Design an inner, recursive procedure that takes a node n as a parameter,
		and returns True if the tree rooted at n verifies the BST property. Before
		you start coding, take a piece of paper and think about the problem:
		- what is/are the base case(s): what should I return if the node reference
		 is None? if the node is a leaf?
		- what should I return otherwise?
		- ...

		2. Call the inner procedure, passing the root of this BinaryTree object
		 (self.root) as a parameter
		"""
		def is_bst_recursive(node):
			"""return true if the subtree at the given node is a bst,
return false otherwise
:param node:Node object
:type node:Node
:rtype: Boolean
"""
			if node is None:
			    return True
			#what happens when only one node has children and the other doesn't?
			    is_bst_recursive(node.left)
			    is_bst_recursive(node.right)
			return is_bst_recursive(self.root)
	#############################################################

	## NON-ESSENTIAL FUNCTIONS: FOR TEACHING/TESTING PURPOSE

	def update_from_array(self, array  ):
		""" Build a binary tree from nested tuples 
		
		Ex. BinaryTree().update_from_array( ( 1,(2,3,4),(5,None,6) ) yields the following tree:

				1
			 __________/\________
			2                   5
		  _/\                    \
		 3   4                    6

		:param array: a list of the form ( key, ( left subtree ), (right subtree ))
		:type array: tuple
		"""
	
		def read_rec( triplet ):
			""" Inner function: build a (node,depth) pair from a triplet (parnet,left,right) """
			# base case: a leaf
			if triplet is None:
				return None
			if type(triplet) is not list and type(triplet) is not tuple:
				return (Node(triplet), 0)
			# parent node
			n = Node( triplet[0] )
			# children
			data_left = read_rec( triplet[1] )
			data_right = read_rec( triplet[2] )
			if data_left is not None: n.add_left ( data_left[0])
			if data_right is not None: n.add_right ( data_right[0])
			# returning a pair:
			# - current node pointer
			# - height, as computed from children's heights
			if data_left is None:
				if data_right is None:
					return (n,0)
				return (n,data_right[1]+1)
			elif data_right is None:
				return (n,data_left[1]+1)
			return (n, max(data_left[1],data_right[1])+1)

		data = read_rec( array )
		self.root, self.height = data
		self.update_depth( self.root, 0)

		return self
		
	def update_depth(self, node, depth):
		""" Update the depth attribute on the given node, and all its
		descendants

		:param node: root of the subtree to be updated
		:param depth: value of the new depth attribute
		:type node: Node
		:type depth: int
		"""
		if node is not None:
			node.depth=depth
			self.update_depth(node.left, depth+1)
			self.update_depth(node.right, depth+1)

	def display(self):
		"""
		Breadth-first tree-walking, displaying the nodes on the console
		"""
		if self.root is None:
			return
		q = Queue(200)
		
		# overall width is function of the height of the tree
		root_pos = ((1<<(self.height+1))-1)
		
		prev_depth=0
		prev_pos=0
		edge_def=[]
		label_offset=0
		consumed=0
		q.enqueue((self.root,root_pos))
		while not q.is_empty():
			(n, n_pos) = q.dequeue()

			# starting a row: using absolute position for offset
			if n.depth != prev_depth or n is self.root:
				print('')
				prev_depth=n.depth
				offset = n_pos-1
				label_offset=0

				# converting edge boundaries into a string
				print( self.edge_string(edge_def) )
				edge_def=[]

			# in a row: computing an offset from last position
			# -2 takes care of label already entered
			else:
				offset = n_pos - prev_pos - label_offset

			prev_pos = n_pos
			label_offset=len(str(n.key))

			# display the node
			print('{}{}'.format(offset*' ',n.key),end="")

			
			# enqueue children, computing edge boundaries at the same time
			edge_length = int(math.ceil(root_pos/(2**(n.depth+1))))
			if n.left is not None:
				q.enqueue( (n.left, int(n_pos - edge_length)) )
				edge_def.append( ('L', int(n_pos - edge_length),n_pos) )
			if n.right is not None:
				q.enqueue( (n.right, int(n_pos + edge_length)) )
				edge_def.append(  ('R', n_pos+1,int(n_pos + edge_length)) )
		print('')                       
		
	def edge_string( self, definition ):
		""" Build a string according to edge specs """
		last = 0
		string_arr = []
		for pair in definition:

			string_arr.append(' '*(pair[1]-last-1))
			if pair[0]=='L':
				string_arr.append(' ')
			else:
				string_arr.append( '\\' )
			string_arr.append( '_'*(pair[2]-pair[1]-1))
			if pair[0]=='L':
				string_arr.append( '/' )
			else:
				string_arr.append( ' ' )
			last = pair[2]
		return ''.join( string_arr )
			
					
class BinaryTree_UnitTest(unittest.TestCase):

	def test_bst_true_1(self):
		""" Test BST property """
		bst=BinaryTree( array = (15, (7, (3,2,4), (10,8,(14,12,None))), (21, 19 ,(24,None,67))))
		print("test BST true")
		bst.display()
		self.assertTrue( bst.is_bst() )

	
	def test_bst_true_2(self):
		""" Test BST property: leaf """
		bst=BinaryTree( array = (15,None,None))
		print("test BST true: testing leaf")
		bst.display()
		self.assertTrue( bst.is_bst() )
		

	def test_bst_false(self):
		bst=BinaryTree( array = (15, (7, (3,2,4), (10,8,(12,14,None))), (21, 19 ,(24,None,23))))
		print("test BST false")
		bst.display()
		self.assertFalse( bst.is_bst() )


def main():
	unittest.main()

if __name__ == '__main__':
	main()


	
