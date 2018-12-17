import Adjudicator

## TestCase 1- Player 1 does not respond in time. Player 2 should is winner.
class Agent1_1:
	def __init__(self, id):
		self.id = id

	def getBMSTDecision(self, state):
		time.sleep(5)
		pass
	
	def buyProperty(self, state):
		return True
	
	def auctionProperty(self, state):
		return 0
	
	def respondTrade(self, state):
		return True
		
	def jailDecision(self, state):
		return ("P")

	def receiveState(self, state):
		pass
		
		
class Agent1_2:
	def __init__(self, id):
		self.id = id

	def getBMSTDecision(self, state):
		pass
	
	def buyProperty(self, state):
		return True
	
	def auctionProperty(self, state):
		return 0
	
	def respondTrade(self, state):
		return True
		
	def jailDecision(self, state):
		return ("P")

	def receiveState(self, state):
		pass
		
def testTimeout(adjudicator):
	diceRolls = [[6,5], [1,2]]
	
	winner, currState = adjudicator.runGame(Agent1_1(1), Agent1_2(2), diceRolls, [], [])
	return winner == 2
 

## TestCase 2 : 100 turns, Player 1 only buys Baltic Av(@60), player 2 keeps giving rent(@4). No other action. After 7 full rounds(100+ moves). Player 2 is winner.
class Agent2:
	def __init__(self, id):
		self.id = id

	def getBMSTDecision(self, state):
		pass
	
	def buyProperty(self, state):
		if ((state[4] == 3) & (state[5][0] == 3) & (state[1][3] == 0)) :
			return True
		return False
	
	def auctionProperty(self, state):
		return 0
	
	def respondTrade(self, state):
		return False
		
	def jailDecision(self, state):
		return ("R")

	def receiveState(self, state):
		pass

def testWinnerAfter100turns(adjudicator):
#	diceRolls = [[(1, 2), (1, 2)], [(4, 2), (4, 2)], [(3,1), (3,1)], [(4,2),(4,2)], [(1,3), (1,3)] ,[(1,3), (1,3)], [(2,3), (2,3)], [(5,3), (5,3)],	
#				[(1, 2), (1, 2)], [(4, 2), (4, 2)], [(3,1), (3,1)], [(4,2),(4,2)], [(1,3), (1,3)] ,[(1,3), (1,3)], [(2,3), (2,3)], [(5,3), (5,3)],
#				[(1, 2), (1, 2)], [(4, 2), (4, 2)], [(3,1), (3,1)], [(4,2),(4,2)], [(1,3), (1,3)] ,[(1,3), (1,3)], [(2,3), (2,3)], [(5,3), (5,3)],
#				[(1, 2), (1, 2)], [(4, 2), (4, 2)], [(3,1), (3,1)], [(4,2),(4,2)], [(1,3), (1,3)] ,[(1,3), (1,3)], [(2,3), (2,3)], [(5,3), (5,3)],
#				[(1, 2), (1, 2)], [(4, 2), (4, 2)], [(3,1), (3,1)], [(4,2),(4,2)], [(1,3), (1,3)] ,[(1,3), (1,3)], [(2,3), (2,3)], [(5,3), (5,3)],
#				[(1, 2), (1, 2)], [(4, 2), (4, 2)], [(3,1), (3,1)], [(4,2),(4,2)], [(1,3), (1,3)] ,[(1,3), (1,3)], [(2,3), (2,3)], [(5,3), (5,3)],
#				[(1, 2), (1, 2)], [(4, 2), (4, 2)], [(3,1), (3,1)], [(4,2),(4,2)], [(1,3), (1,3)] ,[(1,3), (1,3)], [(2,3), (2,3)], [(5,3), (5,3)]]

#3,3
#9,9
#13,13
#19,19
#23,23
#27,27
#32, 32
#0,0

	diceRolls = [[1, 2], [1, 2], [4, 2], [4, 2], [3, 1], [3, 1], [4, 2], [4, 2], [1, 3], [1, 3] ,[1, 3], [1, 3], [2, 3], [2, 3], [5, 3], [5, 3],	
				[1, 2], [1, 2], [4, 2], [4, 2], [3, 1], [3, 1], [4, 2], [4, 2], [1, 3], [1, 3] ,[1, 3], [1, 3], [2, 3], [2, 3], [5, 3], [5, 3],
				[1, 2], [1, 2], [4, 2], [4, 2], [3, 1], [3, 1], [4, 2], [4, 2], [1, 3], [1, 3] ,[1, 3], [1, 3], [2, 3], [2, 3], [5, 3], [5, 3],
				[1, 2], [1, 2], [4, 2], [4, 2], [3, 1], [3, 1], [4, 2], [4, 2], [1, 3], [1, 3] ,[1, 3], [1, 3], [2, 3], [2, 3], [5, 3], [5, 3],
				[1, 2], [1, 2], [4, 2], [4, 2], [3, 1], [3, 1], [4, 2], [4, 2], [1, 3], [1, 3] ,[1, 3], [1, 3], [2, 3], [2, 3], [5, 3], [5, 3],
				[1, 2], [1, 2], [4, 2], [4, 2], [3, 1], [3, 1], [4, 2], [4, 2], [1, 3], [1, 3] ,[1, 3], [1, 3], [2, 3], [2, 3], [5, 3], [5, 3],
				[1, 2], [1, 2], [4, 2], [4, 2], [3, 1], [3, 1], [4, 2], [4, 2], [1, 3], [1, 3] ,[1, 3], [1, 3], [2, 3], [2, 3], [5, 3], [5, 3]]

	winner, currState = adjudicator.runGame(Agent2(1), Agent2(2), diceRolls, [], [])

	return winner == 2	

	
## TestCase 3 : Player 1 goes to jail. After 3 failed rolls, he is released.
class Agent3:
	def __init__(self, id):
		self.id = id

	def getBMSTDecision(self, state):
		pass
	
	def buyProperty(self, state):
		return False
	
	def auctionProperty(self, state):
		return 0
	
	def respondTrade(self, state):
		return False
		
	def jailDecision(self, state):
		return ("R")

	def receiveState(self, state):
		pass

#10,3   18,9   24,13  30,19  -1,23,  -1,27,  13,33	
def testGetOutOfJailAfter3turns(adjudicator): 
	#diceRolls = [[(5, 5),(1, 2)], [(4, 4), (4, 2)], [(3, 3), (3,1)], [(1, 5), (4,2)] , [(1,3), (1,3)], [(1,3), (1,3)], [(1,3), (2,3)], [(1,2), (5,3)]]
	diceRolls = [[4, 6], [1, 2], [5, 3], [4, 2], [5, 1], [3,1], [1, 5], [4,2], [1,3], [1,3], [1,3], [1,3], [1,2], [5,3]]
	
	_, currState = adjudicator.runGame(Agent3(1), Agent3(2), diceRolls, None, None)

	return currState[2][0] == 13
	

## TestCase 4 : Player 1 has to pay 50 to player 2 by chance card.
class Agent4:
	def __init__(self, id):
		self.id = id

	def getBMSTDecision(self, state):
		pass
	
	def buyProperty(self, state):
		return False
	
	def auctionProperty(self, state):
		return 0
	
	def respondTrade(self, state):
		return False
		
	def jailDecision(self, state):
		return ("R")

	def receiveState(self, state):
		pass
		
def testChairmanoftheBoard(adjudicator):
	diceRolls = [[3, 4],[1, 2]]
	chance = [14, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15]
	
	_, currState = adjudicator.runGame(Agent4(1), Agent4(2), diceRolls, chance, [])

	return (currState[3][1] - currState[3][0]) == 100
	
	
## TestCase 5 : Player 1 has to go back 3 spaces by chance card.
class Agent5:
	def __init__(self, id):
		self.id = id

	def getBMSTDecision(self, state):
		pass
	
	def buyProperty(self, state):
		return False
	
	def auctionProperty(self, state):
		return 0
	
	def respondTrade(self, state):
		return False
		
	def jailDecision(self, state):
		return ("R")

	def receiveState(self, state):
		pass
		
def testGoBack3Spaces(adjudicator):
	diceRolls = [[5, 6], [1, 2], [5,6], [2,1]]
	chance = [8, 13, 0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 14, 15]
	
	_, currState = adjudicator.runGame(Agent5(1), Agent5(2), diceRolls, chance, [])
	return currState[2][0] == 19	


## TestCase 6 : Player 1 tries to build house without owning all colors.
class Agent6_1:
	def __init__(self, id):
		self.id = id

	def getBMSTDecision(self, state):
		if (state[1][3] == 1) :
			return ('B', [(3, 1)])
	
	def buyProperty(self, state):
		if ((state[4] == 3) & (state[5][0] == 3) & (state[1][3] == 0)) :
			return True
		return False
	
	def auctionProperty(self, state):
		return 0
	
	def respondTrade(self, state):
		return False
		
	def jailDecision(self, state):
		return ("R")

	def receiveState(self, state):
		pass
		
class Agent6_2:
	def __init__(self, id):
		self.id = id

	def getBMSTDecision(self, state):
		pass
	
	def buyProperty(self, state):
		return False
	
	def auctionProperty(self, state):
		return 0
	
	def respondTrade(self, state):
		return False
		
	def jailDecision(self, state):
		return ("R")

	def receiveState(self, state):
		pass
		
def testBuildPropertyWithoutMonopoly(adjudicator):

	diceRolls = [[1, 2], [5, 3], [1, 2], [2, 1]]
	
	_, currState = adjudicator.runGame(Agent6_1(1), Agent6_1(2), diceRolls, [], [])
	return currState[1][3] == 1


tests = [
	testTimeout,
	testWinnerAfter100turns,
	testGetOutOfJailAfter3turns,
	testChairmanoftheBoard,
	testGoBack3Spaces,
	testBuildPropertyWithoutMonopoly	
]

def runTests():
    allPassed = True
    for test in tests:
        adjudicator = Adjudicator()
        result = test(adjudicator)
        if not result:
            print(test.__name__+ " failed!")
            allPassed = False
		else :
			print(test.__name__+ " passed!")
    if allPassed: print("All tests passed!")

runTests()
