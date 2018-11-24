class Bank(object):
    def __init__(self, total_houses= 32, total_hotels=12):
        self.total_houses = total_houses
        self.total_hotels = total_hotels
        self.houses_in_use = 0
        self.hotels_in_use = 0

    def give_houses(self, count):
        pass

    def give_hotels(self, count):
        pass





class Player(object):
    def __init__(self, id, game_agent, inital_cash=0):
        self.id = id
        self.cash = inital_cash
        self.position = 0
        self.agent = game_agent
        self.jail_cards = 0
        self.jail_turn_count = 0

    def add_cash(self, cash):
        self.cash += cash
        return True

    def remove_cash(self, cash):
        if self.cash - cash < 0:
            print("UNABLE TO REMOVE CASH FROM THE PLAYER ", self.id)
            return False
        self.cash -= cash
        return True

    def set_position(self, position):
        self.position = position

    def get_position(self):
        return self.position

    def move_position(self, val):
        """
        :param val:
        :return:
        """
        if not self.is_in_jail():
            self.position += val
            self.position = self.position % 40
        else:
            print("THIS PLAYER is in JAIL, unable to move out of jail")

    def move_to_jail(self):
        self.position = -1
        self.jail_turn_count = 0

    def is_in_jail(self):
        if self.position == -1:
            return True
        return False

    def use_jail_card(self):
        if self.jail_cards>0:
            self.jail_cards -= 1
            self.move_out_of_jail()
            self.jail_turn_count = 0
            return True
        return False

    def move_out_of_jail(self):
        if self.position==-1:
            self.jail_turn_count = 0
            self.position = 10