from Agent import Agent
from GameState import *



p1 = Player(0, game_agent=Agent(id=0))
p2 = Player(1, game_agent=Agent(id=1))
p1.add_cash(2000)
p2.add_cash(2000)
b = Bank()
game_state = GameState()
game_state.load_state("each_box_data.json")
engine = GameEngine(game_state, p1, p2, b)
engine.run()
