#!/usr/bin/python

import unittest
import time


class Node():
	""" A node representation, to be used as a brick for building linked lists """
	
	def __init__(self, key=None,prev_ptr=None, next_ptr=None):
		self.key=key
		self.prev_ptr=prev_ptr
		self.next_ptr=next_ptr

	def __str__(self):
		return str(self.key)

class SinglyLinkedList():

	def __init__(self):
		self.head = None 
		self.length = 0

	def is_empty(self):
		""" Return T if the list is empty, F otherwise.

		:rtype: bool
		"""
		return self.head == None

	def insert(self, node):
		""" Insert a new node at the start of the list.

		:param node: a node object
		:type node: Node
		"""
		node.next_ptr = self.head
		if self.head != None:
			self.head.prev_ptr = node
					
		self.head = node
		node.prev_ptr = None

	def search(self,k):
		""" Search the list for the node with the given key k. Return the node if it has been found, None otherwise.
		
		:param k: a value
		:type k: int
		:rtype: Node
		"""
		x = self.head
		while (x != None and x.key != k):
			x = x.next_ptr
		return x


	def delete(self, node):
		""" Delete the node that matches the given pointer, splicing it out of the list.

		:param node: a node reference
		:type node: Node
		"""
		if (node.prev_ptr != None):
			node.prev_ptr.next_ptr = node.next_ptr
		else:
			self.head = node.next_ptr
		if (node.next_ptr != None):
			node.next_ptr.prev_ptr = node.prev_ptr

	def __str__(self):
		""" Return a string representation of the list, that allows for a list object to be passed
		as a parameter to the built-in print() function.
		
		:rtype: str
		"""

		output = ''
		el = self.head
		output = 'LL['
		while el is not None:
			if output != 'LL[': output += ', '
			output += ( ', {}'.format(el) )
			el = el.next_ptr
		output += ']'
		return output

class ll_node_unittest( unittest.TestCase ):
	""" This test class shows how to create new Node objects """
	
	def test_node_creation1(self):
		node = Node()
		self.assertEqual(node.key, None)

	def test_node_creation2(self):
		node = Node()
		self.assertEqual(node.prev_ptr, None)

	def test_node_creation3(self):
		node = Node()
		self.assertEqual(node.next_ptr, None)
	
	def test_node_creation4(self):
		node = Node(2)
		self.assertEqual(node.key, 2)

	def test_node_creation5(self):
		node = Node('eusebius')
		self.assertEqual(node.key,'eusebius')

class sglll_unittest( unittest.TestCase ):
	""" Your Singly Linked List implementation should pass all the following tests"""

	def test_empty_list(self):
		ll = SinglyLinkedList()
		self.assertEqual(ll.head, None)

	def test_insert1(self):
		ll = SinglyLinkedList()
		ll.insert(Node(3) )
		self.assertEqual(ll.head.key,3)

	def test_insert2(self):
		ll = SinglyLinkedList()
		ll.insert(Node('abc'))
		self.assertEqual(ll.head.key,'abc')
		
	def test_insert3(self):
		ll = SinglyLinkedList()
		for i in range(1,11):
			ll.insert( Node(i))
		self.assertEqual( ll.length, 10 )

	
	def test_insert4(self):
		ll = SinglyLinkedList()
		for i in range(1,11):
			ll.insert( Node(i))
		self.assertEqual( ll.head.key, 10 )

	def test_search_1(self):
		""" Successful search """
		ll = SinglyLinkedList()
		for i in range(1,11):
			ll.insert( Node(i))
		found = ll.search(5)
		self.assertFalse( found is None )
		self.assertEqual( found.key, 5 )

	def test_search_2(self):
		""" Unsuccessful search """
		ll = SinglyLinkedList()
		for i in range(1,11):
			ll.insert( Node(i))
		found = ll.search(12)
		self.assertTrue( found is None )

	def test_delete_head(self):
		""" Special case for deletion: the head """
		ll = SinglyLinkedList()
		ll.insert(Node(1))
		ll.insert(Node(2))
		ll.delete( ll.head )
		self.assertEqual( ll.head.key, 1 )

	def test_delete(self):
		""" Test correct splicing of the list """
		ll = SinglyLinkedList()
		for i in range(1,200):
			ll.insert( Node(i))

		before = ll.search(12)
		found = ll.search(11)
		after = ll.search(10)
		ll.delete( found )
		
		self.assertEqual( before.next_ptr, after )

	def test_delete_from_single_element_list(self):
		""" A special case: list with 1 element """
		ll = SinglyLinkedList()
		ll.insert(Node(1))
		ll.delete( ll.search(1))
		self.assertEqual( ll.is_empty(), True)

	def test_massive_deletion_1(self):
		ll = SinglyLinkedList()
		for i in range(1,200):
			ll.insert( Node(i))
		found = ll.search(5)
		start=time.time()
		ll.delete( found )
		cost= time.time()-start
		print ('\nSingly-linked list: deleting from 200 elements: {}'.format(cost))
		self.assertEqual( ll.length, 198 )

	def test_massive_deletion_2(self):
		ll = SinglyLinkedList()
		for i in range(1,400):
			ll.insert( Node(i))
		found = ll.search(5)
		start=time.time()
		ll.delete( found )
		cost= time.time()-start
		print ('\nSingly-linked list: deleting from 400 elements: {}'.format(cost))
		self.assertEqual( ll.length, 398 )




def main():
	unittest.main()

if __name__ == '__main__':
	main()




