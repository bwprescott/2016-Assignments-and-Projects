#!/usr/bin/python

import unittest
import time

"""
CLRS, exercise 10.2-3

Implementing a Queue using a singly-linked list, with all operations running in O(1)

10/12 - Added 2 extra functions in the SinglyLinkedList class, to be used by the Queue class.
10/12 - Deleting from an empty list raises an UnderFlowException, instead of returning None (tests updated accordingly)
10/12 - Adding mass dequeuing tests, for experimental verification of the constant time

"""


class UnderFlowException( Exception ): pass

class Node():
	
	def __init__(self, key=None,prev_ptr=None, next_ptr=None):
		self.key=key
		self.prev_ptr=prev_ptr
		self.next_ptr=next_ptr

	def __str__(self):
		return str(self.key)

class SinglyLinkedList():

	def __init__(self):
		self.head = None 
		self.tail = None
		self.length = 0

	def is_empty(self):
		return not self.head

	def insert(self, node):
		node.next_ptr = self.head
		self.head = node	
		self.length += 1

	def search(self,k):
		node = self.head
		while node is not None and node.key != k:
			node = node.next_ptr
		return node

	def delete(self, node):
		if node is None:
			raise(UnderFlowException)
		# case 1: delete lone head
		if node == self.head:
			self.head = self.head.next_ptr
			self.length -= 1
			return
			
		# case 2: seach until n.next = node
		current_node = self.head
		while current_node.next_ptr is not None and current_node.next_ptr is not node:
			current_node = current_node.next_ptr
		# update next pointer
		if current_node.next_ptr is not None:
			current_node.next_ptr = current_node.next_ptr.next_ptr	

		self.length -= 1
	
	
	######################### TODO for constant time Queue impl. ###
	def insert_tail(self, node):
		""" Insert a new node at the _tail_ of the list

		:param node: a node object
		:type node: Node
		"""
		node.next_ptr = self.tail
		self.tail = node	
		self.length += 1

	def delete_head(self):
		""" Delete the head of the list (simply pass the head reference to
		the delete() function
		"""
		
		self.head = self.head.next_ptr
		self.length -= 1
			
			
	#################################################################

	def __str__(self):
		output = ''
		el = self.head
		while el is not None:
			output += ( ', {}'.format(el) )
			el = el.next_ptr
		return output

class Queue():
	def __init__(self, size):
		self.ll = SinglyLinkedList()
		self.tail=0
		self.head=0
		self.array=[None]*size
	
	#################### TODO: implement the Queue operations #####
	def is_empty(self):
		return self.head==self.tail
				
	def enqueue(self, k):
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
		if self.head == len(self.array)-1:
			self.head=0
		else:
			self.head = self.head+1

		return x

	def __str__(self):
		return str(self.ll)
	################################################################

class sglll_unittest( unittest.TestCase ):

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

	def test_search(self):
		ll = SinglyLinkedList()
		for i in range(1,11):
			ll.insert( Node(i))
		found = ll.search(5)
		self.assertFalse( found is None )
		self.assertEqual( found.key, 5 )

	
	def test_delete_at_head(self):
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
		""" Running time for this test should be about half the time for the next test
		(because Delete(n) = O(n))
		"""
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
		""" Running time for this test should be about twice the time for the previous test
		(because Delete(n) = O(n))
		"""
		ll = SinglyLinkedList()
		for i in range(1,400):
			ll.insert( Node(i))
		found = ll.search(5)
		start=time.time()
		ll.delete( found )
		cost= time.time()-start
		print ('\nSingly-linked list: deleting from 400 elements: {}'.format(cost))
		self.assertEqual( ll.length, 398 )

	## Testing extra functions required for Queue implementation

	def test_delete_head(self):
		""" Delete the head """
		ll = SinglyLinkedList()
		ll.insert(Node(1))
		ll.insert(Node(2))
		ll.delete_head()
		self.assertEqual( ll.head.key, 1 )
	
	def test_insert_tail(self):
		ll = SinglyLinkedList()
		ll.insert_tail( Node(1) )
		ll.insert_tail( Node(2) )
		self.assertEqual( ll.tail.key, 2 )
		


class queue_unittest( unittest.TestCase):

	def test_empty_queue(self):
		q = Queue()
		self.assertEqual(q.is_empty(), True)

	def test_enqueue_1(self):
		q = Queue()
		q.enqueue( 1 )
		self.assertEqual(q.is_empty(), False)

	def test_enqueue_2(self):
		q = Queue()
		q.enqueue( 1 )
		q.enqueue( 2 )
		q.enqueue( 3 )
		self.assertEqual(q.is_empty(), False)

	def test_dequeue_from_empty(self):
		q = Queue()
		raisedException = False

		try:
			q.dequeue()
		except UnderFlowException as e:
			raisedException = True

		self.assertTrue( raisedException )
	
	def test_dequeue_1(self):
		q = Queue()

		q.enqueue( 1 )
		q.enqueue( 2 )
		q.enqueue( 3 )
		
		print(q)

		self.assertEqual(q.dequeue().key, 1 )
		self.assertEqual(q.dequeue().key, 2 )
		self.assertEqual(q.dequeue().key, 3 )

		print(q)
		self.assertEqual(q.is_empty(), True )


	def test_massive_dequeuing_500(self):
		""" Running time for this test should be about the same as for next test 
		(because dequeue() uses delete_head(), which is O(1) )
		"""
		q = Queue()
		print(q)
		for i in range(0,500):
			q.enqueue(i)
		start = time.time()
		for i in range(0,500):
			q.dequeue()
		cost = time.time()-start
		print ('\nSLL-based (constant time) queue: deleting from 500 elements: {}'.format(cost))
		self.assertTrue( q.is_empty() )

	def test_massive_dequeuing_1000(self):
		""" Running time for this test should be about the same as for next test 
		(because dequeue() uses delete_head(), which is O(1) )
		"""
		q = Queue()
		print(q)
		for i in range(0,1000):
			q.enqueue(i)
		start = time.time()
		for i in range(0,1000):
			q.dequeue()
		cost = time.time()-start
		print ('\nSLL-based (constant time) queue: deleting from 1000 elements: {}'.format(cost))
		self.assertTrue( q.is_empty() )


def main():
	unittest.main()

if __name__ == '__main__':
	main()




