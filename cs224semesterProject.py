import unittest
class EditDistance:

	def editDistance (strx, stry, m, n):
	"""
	:param strx: the original word
	:param stry: the word you are transforming the original word into
	:param m: length of strx
	:param n: length of stry
	:type strx: string
	:type stry: string
	:type m: int
	:type n: int
	:rtype: int
	"""
			for i in range (m+1):
				for j in range (n+1):

							if i == 0:
‘				table[i][j] = j

							elif j == 0:
				table[i][j] = i

							elif strx[i-1] == stry[j] && strx[i] == stry[j-1]:
				table[i][j] = stry[j-1]
				table[i+1][j+1] = strx[i-1]
				i = i + 2
				j = j + 2

							elif strx[i-1] == stry [j-1]:
				table[i][j] = newWord[i-1][j-1]

							else:
				table[i][j] = 1 + min(table[i][j-1]
							 table[i-1][j]
							 table[i-1][j-1])

			return table[m][n]


class Tests(unittest.TestCase):

			def testEmptyStrings(self):
				a = self.editDistance('','',0,0)
				self.assertEqual(a, 0)

			def testEmptyStringX(self):
				a = self.editDistance('','words',0,5)
				self.assertEqual(a, 5)

			def testEmptyStringX(self):
				a = self.editDistance('words','',5,0)
				self.assertEqual(a, 5)

			def testTwoStrings(self):
				a = self.editDistance('although','together', 5, 6)
				self.assertEquals(a, 8)

