
import unittest
import players

class TestPlayers(unittest.TestCase):

	def setUp(self):
		print "setting up..."
		# run at start of each test

	def test_getPlayerYear(self):
		cases = [('Klay Thompson', 2013), ('Kobe Bryant', 2002), ('Michael Jordan', 1996), ('Player', 2013), ('Anthony Davis', 2000)]
		expected_success = [True, True, True, False, False]
		for n, case in enumerate(cases):
			print "Test case: " + case[0] + ',', case[1]
			result = players.getPlayerYear(case[0], case[1])
			self.assertEqual(len(result) > 0, expected_success[n])

	def test_listPlayers(self):
		self.assertTrue(players.listPlayers(2013) != None)

if __name__ == '__main__':
    unittest.main()
