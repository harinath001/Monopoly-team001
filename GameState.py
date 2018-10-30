class PropertyStateEnum:
    NO_ONE = 0
    PLAYER1 = 1
    PLAYER1_1_HOUSE = 2
    PLAYER1_2_HOUSE = 3
    PLAYER1_3_HOUSE = 4
    PLAYER1_4_HOUSE = 5
    PLAYER1_HOTEL = 6
    PLAYER1_MORTGAGED = 7
    PLAYER2 = -1
    PLAYER2_1_HOUSE = -2
    PLAYER2_2_HOUSE = -3
    PLAYER2_3_HOUSE = -4
    PLAYER2_4_HOUSE = -5
    PLAYER2_HOTEL = -6
    PLAYER2_MORTGAGED = -7

class Box:

    def __init__(self, **kwargs):
        """
        :param position_number: index of the box from start position
        :param kwargs: it contain all other information about the box like color, name etc
        """
        self.state = 0
        self.position = kwargs.get("position_number", None)
        self.special = kwargs.get("special", None)
        self.color = kwargs["color"]
        self.display_name = kwargs["name"]

    def is_valid_state(self, state):
        if state>7 or state<-7:
            return False
        return True

    def set_property_state(self, state):
        self.state = state

    def get_property_state(self, state):
        pass

    def is_jail(self):
        return self.special == "JAIL"

    def is_chance(self):
        return self.special == "CHANCE"

    def is_community_chest(self):
        return self.special == "COMMUNITY_CHEST"

    def is_utility(self):
        return self.special=="UTILITY"

    def is_station(self):
        return self.special=="STATION"

class GameState(object):
    def __init__(self):
        super(self, GameState).__init__()
        self.turn_number = 0
        self.property_status = []
