
import unittest
import players

class TestPlayers(unittest.TestCase):

	def setUp(self):
		print "setting up..."
		# run at start of each test

	def test_getPlayerYear(self):
		cases = [('Klay Thompson', 2013, 'per game'), ('Kobe Bryant', 2002, 'advanced'), ('Michael Jordan', 1996, 'total'), ('Player', 2013, 'per game'), ('Anthony Davis', 2000, 'per 36')]
		expected_success = [True, True, True, False, False]
		for n, case in enumerate(cases):
			print "Test case: " + case[0] + ', ' + str(case[1]) + ', ' + case[2]
			result = players.getPlayerYear(case[0], case[1], case[2])
			self.assertEqual(len(result) > 0, expected_success[n])

	def test_listPlayers(self):
		self.assertTrue(players.listPlayers(2013) != None)

if __name__ == '__main__':
    unittest.main()
