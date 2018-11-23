from Agent import Agent
from GameState import *
from Player import Player, Bank
from GameEngine import GameEngine



p1 = Player(0, game_agent=Agent(id=0))
p2 = Player(1, game_agent=Agent(id=1))
p1.add_cash(2000)
p2.add_cash(2000)
# p1.set_position(31)
b = Bank()
game_state = GameState()
game_state.load_state("each_box_data.json")
# game_state.boxes[5].state = -1
# game_state.boxes[15].state = -1
# game_state.boxes[25].state = -1
# game_state.boxes[35].state = -1
# game_state.boxes[31].state = -3
# game_state.boxes[32].state = -3
# game_state.boxes[34].state = -3
# game_state.boxes[6].state = 4
# game_state.boxes[8].state = 1
# game_state.boxes[9].state = 2
# game_state.boxes[9].state = 1
# game_state.boxes[11].state = -3
# game_state.boxes[13].state = -1
# game_state.boxes[14].state = -1
engine = GameEngine(game_state, p1, p2, b)
engine.run()
