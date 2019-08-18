#!/usr/bin/python3

import unittest
import collections as clt


log_level=1

def log( string, level=1):
	global log_level
	if log_level >= level:
		print(string)

class Vertex():
	""" A vertex definition."""

	# These constants can be referred to afterwards as follows:
	#	Vertex.WHITE, Vertex.GRAY...
	WHITE = 0
	GRAY = 1
	BLACK = 2
	INFTY = 2**15
	
	def __init__(self, label=''):
		"""
		Initialize a vertex
		
		:param index: position in the vertex array
		:param label: human-friendly label
		:type index: int
		:type label: str
		"""

		# a label (the index itself, or a letter)		
		self.label = label
		self.short_label = label[0]

		# distance = infinity by default
		self.distance = Vertex.INFTY
		self.pi = None
		self.color = Vertex.WHITE
		
		# for depth-first search
		self.discovery = 0
		self.finish = 0


	
	def __str__(self):
		to_return =  '({}:{})'.format(self.label, self.distance)
		if self.pi is not None:
			to_return += ':{}'.format(self.pi.label)
		return to_return

class Graph():
	""" A graph definition """

	def __init__(self,v=(),e=()):
		""" Create graph with given vertices 

		:param v: labels, i.e. integers, or alphabetical labels
		:param e: edges, i.e pairs of labels
		:type v: tuple
		:type e: tuple	
		"""
	
		# Reads the vertex labels and create corresponding Vertex objects in V
		# Note: this is an ordered dictionary: pairs (key, value) are listed
		# in the order they were inserted, which is convenient for testing
		self.V = clt.OrderedDict()

		for label in v:
			self.V[label] = Vertex( label ) 
			
		# List of adjacency lists:  list containg |V| lists
		self.Adj  =  { vertex: [] for label, vertex in self.V.items() }

		# For clarity, weights are more conveniently stored into a matrix
		self.Matrix = { v1: { v2: None for v2 in self.V.values() } for v1 in self.V.values() } 

		# Read the edges (pairs of labels) and create corresponding entries
		# in Adj
		for edge in e:
			v1, v2 = ( self.V[ edge[0] ], self.V[ edge[1] ])
			self.Adj[ v1 ].append( v2 )
			self.Matrix[ v1 ][ v2 ] = 1

			# storing weights in the matrix: 3rd element of an edge definition
			# tuple (u, v, w) is the weight
			if (len(edge)>2):
				self.Matrix[v1][v2] = edge[2]
		
		self.time = 0
		 

	def depth_first(self):
		""" Depth-First search 
		"""	
		log("Starting DFS...")
		time = 0

		def depth_first_visit(u, spacer=''): 
			""" Recursive procedure, for depth-first search

			:param u: the vertex under examination
			:param topo: an array of vertices, to be populated by a topological sort proc.
			:type u: Vertex
			"""
			nonlocal time
			time += 1	
			log(spacer+'depth_first_visit({}) at time {}:00'.format( u.label, time ),3)
			u.discovery = time
			u.color = Vertex.GRAY
			for v in self.Adj[ u ]:
				if v.color == Vertex.WHITE:
					v.pi = u
					depth_first_visit( v, spacer+'\t' )
			u.color == Vertex.BLACK
			time += 1
			u.finish = time
			log(spacer+'finish {} at time {}:00'.format( u.label, time ),3)

		for v in self.V.values():
			if v.color == Vertex.WHITE:
				depth_first_visit( v, '' )
	

	######################################################################
	def topo_sort(self):
		""" Topological sort: return a topologically sorted list of vertices (reference: CLRS3, p. 613)
		
		..note: large parts of the code for the depth_first() above function can be reused here, with a few modifications needed, in order to populate a list of vertices during the graph exploration.

		:return: a list of vertex objects, sorted in topological order.
		:rtype: list
		"""

		log("Starting DFS...")
		time = 0
		myList = []
		
		
		def depth_first_visit(u, spacer=''): 
			""" Recursive procedure, for depth-first search

			:param u: the vertex under examination
			:param topo: an array of vertices, to be populated by a topological sort proc.
			:type u: Vertex
			"""
			nonlocal time
			time += 1	
			log(spacer+'depth_first_visit({}) at time {}:00'.format( u.label, time ),3)
			u.discovery = time
			u.color = Vertex.GRAY
			for v in self.Adj[ u ]:
				if v.color == Vertex.WHITE:
					v.pi = u
					depth_first_visit( v, spacer+'\t' )
					
			u.color == Vertex.BLACK
			time += 1
			u.finish = time
			log(spacer+'finish {} at time {}:00'.format( u.label, time ),3)

		for v in self.V.values():
			if v.color == Vertex.WHITE:
				depth_first_visit( v, '' )
				myList.append[v]

		return myList
				
	def dag_shortest_path(self, source):
		""" DAG Shortest path: compute the shortest path tree (or: the predecessor subgraph) of a directed acyclic graph (DAG), from given source vertex.

		:param source: label of a source vertex
		:type source: str
		"""

		topo_sort(self)
		initialize_single_source(self, source)
		for v in self.V.values:
			for x in self.Adj[u]:
				relax(u, x, self.Matrix[u][v])
		    

	def relax(self, u, v):
		"""
		Relax vertex v through u: compare currenet value for v.distance and update if is strictly larger than u.distance + weight(u, v).
		
		..note: weight of a given edge (u,v) is stored in self.Matrix[u][v]

		:param u: vertex u
		:param v: vertex v
		:type u: Vertex
		:type v: Vertex
		"""

		if v.distance > u.distance + self.Matrix[u][v]:
		    v.distance = u.distance + self.Matrix[u][v]
		    v.pi = u
		    
	#####################################################################

	def initialize_single_source(self, s):
		""" Initialize the graph at the start of a shortest-path algorithm (BFS, DAG-shortest_path)

		:param s: source vertex
		:type s: Vertex
		"""
		for label, v in self.V.items():
			v.distance = Vertex.INFTY
			v.pi = None
		s.distance = 0


	def __str__(self):
		output = 'V=['
		for v in self.V:
			output += str(v)+','	
		output += ']\n'
		for u in self.Adj.keys():
			output += '{}: '.format(u)
			for v in self.Adj[u]:
				output += ' {}'.format(str(v))
			output += '\n'
		return output
	
		
class GraphUnitTest( unittest.TestCase ):


	def test_depth_first_1(self):
		"""" Discovery time """
		g = self.make_sample_undirected_graph()

		g.depth_first()

		self.assertEqual(g.V['a'].discovery, 1)
		self.assertEqual(g.V['b'].discovery, 2)
		self.assertEqual(g.V['c'].discovery, 3)
		self.assertEqual(g.V['d'].discovery, 4)
		self.assertEqual(g.V['e'].discovery, 5)
		self.assertEqual(g.V['f'].discovery, 11)
		self.assertEqual(g.V['g'].discovery, 7)
		self.assertEqual(g.V['h'].discovery, 6)

	def test_depth_first_2(self):
		"""" Finish time """
		g = self.make_sample_undirected_graph()

		g.depth_first()

		self.assertEqual(g.V['a'].finish, 16)
		self.assertEqual(g.V['b'].finish, 15)
		self.assertEqual(g.V['c'].finish, 14)
		self.assertEqual(g.V['d'].finish, 13)
		self.assertEqual(g.V['e'].finish, 10)
		self.assertEqual(g.V['f'].finish, 12)
		self.assertEqual(g.V['g'].finish, 8)
		self.assertEqual(g.V['h'].finish, 9)


	def test_depth_first_3(self):
		"""" Digraph: discovery time """
		g = self.make_sample_digraph_2()

		g.depth_first()

		self.assertEqual(g.V['a'].discovery, 1)
		self.assertEqual(g.V['b'].discovery, 2)
		self.assertEqual(g.V['c'].discovery, 3)
		self.assertEqual(g.V['d'].discovery, 4)
		self.assertEqual(g.V['e'].discovery, 9)
		self.assertEqual(g.V['f'].discovery, 13)
		self.assertEqual(g.V['g'].discovery, 5)
		self.assertEqual(g.V['h'].discovery, 10)
		self.assertEqual(g.V['i'].discovery, 17)
		self.assertEqual(g.V['j'].discovery, 18)

	def test_depth_first_4(self):
		"""" Digraph: finish time """
		g = self.make_sample_digraph_2()

		g.depth_first()

		self.assertEqual(g.V['a'].finish, 16)
		self.assertEqual(g.V['b'].finish, 15)
		self.assertEqual(g.V['c'].finish, 8)
		self.assertEqual(g.V['d'].finish, 7)
		self.assertEqual(g.V['e'].finish, 12)
		self.assertEqual(g.V['f'].finish, 14)
		self.assertEqual(g.V['g'].finish, 6)
		self.assertEqual(g.V['h'].finish, 11)
		self.assertEqual(g.V['i'].finish, 20)
		self.assertEqual(g.V['j'].finish, 19)


	def test_topological_1(self):
		g = self.make_dag()

		sorted_vertices = [ vertex.label for vertex in g.topo_sort() ]
	
		self.assertEqual( sorted_vertices, ['shirt','tie','watch','socks','undershorts','pants','shoes','belt','jacket'])


	def test_topological_2(self):
		g = self.make_dag_22_4_1()

		sorted_vertices = [ vertex.label for vertex in g.topo_sort() ]
	
		self.assertEqual( sorted_vertices, ['p', 'n', 'o', 's', 'm', 'r', 'y', 'v', 'x', 'w', 'z', 'u', 'q', 't'])


	def test_relax_1(self):
		""" Relax with update"""
		g = self.make_weighted_dag()
		x = g.V['x']
		y = g.V['y']
		z = g.V['z']
		y.distance = 5
		z.distance = 4
		z.pi = x

		g.relax( y, z) # weight(y,z) = -2
		self.assertEqual( z.distance, 3)
		self.assertEqual( z.pi, y)

	def test_relax_2(self):
		""" Relax with no change (equality) """
		g = self.make_weighted_dag()
		x = g.V['x']
		y = g.V['y']
		z = g.V['z']
		y.distance = 5
		z.distance = 3
		z.pi = x

		g.relax( y, z) # weight(y,z) = -2
		self.assertEqual( z.distance, 3)
		self.assertEqual( z.pi, x)

	def test_relax_3(self):
		""" Relax with no change (new path has larger weight) """
		g = self.make_weighted_dag()
		x = g.V['x']
		y = g.V['y']
		z = g.V['z']
		y.distance = 6
		z.distance = 3
		z.pi = x

		g.relax( y, z) # weight(y,z) = -2
		self.assertEqual( z.distance, 3)
		self.assertEqual( z.pi, x)


	def test_dag_shortest_path_1(self):
		""" Cormen Figure 24.5, p. 656 """
		g = self.make_weighted_dag()
		g.dag_shortest_path('s') 

		self.assertEqual( g.V['z'].pi, g.V['y'])
		self.assertEqual( g.V['y'].pi, g.V['x'])
		self.assertEqual( g.V['x'].pi, g.V['s'])
		self.assertEqual( g.V['t'].pi, g.V['s'])


	def test_dag_shortest_path_2(self):
		""" Cormen Figure 24.5, p. 656 """
		g = self.make_weighted_dag()
		g.dag_shortest_path('s') 

		self.assertEqual( g.V['z'].distance, 3)
		self.assertEqual( g.V['y'].distance, 5)
		self.assertEqual( g.V['x'].distance, 6)
		self.assertEqual( g.V['t'].distance, 2)
		self.assertEqual( g.V['s'].distance, 0)
		self.assertEqual( g.V['r'].distance, Vertex.INFTY)

	def test_dag_shortest_path_3(self):
		g = self.make_weighted_dag_2()
		g.dag_shortest_path('b') 

		self.assertEqual( g.V['g'].pi, g.V['f'])
		self.assertEqual( g.V['f'].pi, g.V['d'])
		self.assertEqual( g.V['e'].pi, g.V['c'])
		self.assertEqual( g.V['d'].pi, g.V['b'])
		self.assertEqual( g.V['c'].pi, g.V['b'])

	def test_dag_shortest_path_4(self):
		g = self.make_weighted_dag_2()
		g.dag_shortest_path('b') 

		self.assertEqual( g.V['g'].distance, 2)
		self.assertEqual( g.V['f'].distance, 1)
		self.assertEqual( g.V['e'].distance, 3)
		self.assertEqual( g.V['d'].distance, 3)
		self.assertEqual( g.V['c'].distance, 4)
		self.assertEqual( g.V['b'].distance, 0)
		self.assertEqual( g.V['a'].distance, Vertex.INFTY)


	#### AUXILIARY FUNCTIONS ####

	def make_sample_undirected_graph(self):
		
		g = Graph( 
			('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'), 
			(	('a','b'), ('a','c'), ('a','d'), 
				('b','a'),('b','c'),('b','e'),('b','f'), 
				('c','a'),('c','b'),('c','d'),('c','f'), 
				('d','a',),('d','c'),('d','e'),('d','f'),('d','g'), 
				('e','b'),('e','d'),('e','h'), 
				('f','b'),('f','c'),('f','d'), 
				('g','d'),('g','h'), 
				('h','d'),('h','g')))
		return g

	def make_sample_digraph(self):
		
		g = Graph( 
			('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'), 
			(	('a','b'), ('a','d'), 
				('b','c'),('b','e'),('b','f'), 
				('c','a'),('c','d'),
				('d','g'), 
				('e','d'),('e','h'), 
				('f','c'),('f','d'), 
				('h','g')))
		return g

	def make_sample_digraph_2(self):
		
		g = Graph( 
			('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'), 
			(	('a','b'), ('a','d'), 
				('b','c'),('b','e'),('b','f'), 
				('c','a'),('c','d'),
				('d','g'), 
				('e','d'),('e','h'), 
				('f','c'),('f','d'), 
				('h','g'),
				('i','g'),('i','j'),
				('j','j')))
		return g

	def make_dag(self):
		g = Graph(
			('undershorts', 'pants','belt','socks','shoes','watch','shirt','tie','jacket'),
			( 	('undershorts','pants'),
				('undershorts','shoes'),
				('pants','belt'),
				('pants','shoes'),
				('belt','jacket'),
				('shirt','belt'),
				('shirt','tie'),
				('socks','shoes')))
		return g

	def make_dag_22_4_1(self):
		""" Exercise 22.4-1 """
		g  = Graph(
			('m','n','o','p','q','r','s','t','u','v','w','x','y','z'),
			(	('m','q'),('m','r'),('m','x'),
				('n','o'),('n','q'),('n','u'),
				('o','r'),('o','s'),('o','v'),
				('p','o'),('p','s'),('p','z'),
				('q','t'),
				('r','u'),('r','y'),
				('s','r'),
				('u','t'),
				('v','w'),('v','x'),
				('w','z'),
				('y','v')))	
		return g	
			

	def make_weighted_dag(self):
		""" Cormen Figure 24.5, p. 656 """
		g = Graph(
			('r', 's', 't', 'x', 'y', 'z'),
			(	('r','s',5),('r','t',3),
				('s','t',2),('s','x',6),
				('t','x',7),('t','y',4),('t','z',2),
				('x','y',-1),('x','z',1),
				('y','z',-2)
			)
		)
		return g
	
	def make_weighted_dag_2(self):
		g = Graph(
			('a', 'b', 'c', 'd', 'e', 'f', 'g'),
			(	('a','b',8),('a','d',1),
				('b','c',4),('b','d',3),
				('c','d',5),('c','e',-1),('c','f',2),
				('d','e',6),('d','f',-2),
				('e','f',1),('e','g',3),
				('f','g',1)
			)
		)
		return g
	
def main():
	unittest.main()

if __name__ == '__main__':
	main()


