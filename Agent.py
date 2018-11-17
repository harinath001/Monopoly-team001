class Agent(object):
    def __init__(self, id):
        self.id = id

    def wanna_build_house(self, game_state):
        print("Player ", self.id, " wanna build house? Press Y to yes and N to no")
        return True if str(raw_input()).lower()=="y" else False

    def wanna_build_hotel(self, game_state):
        print("Player ", self.id, " wanna build hotel? Press Y to yes and N to no")
        return True if str(raw_input()).lower()=="y" else False

    def wanna_trade(self, game_state):
        print("Player ", self.id, " wanna trade? Press Y to yes and N to no")
        # print("assuming NO here..and moving forward")
        return True if str(raw_input()).lower()=="y" else False
        # return False

    def wanna_mortgage(self, game_state):
        print("Player ", self.id, " wanna mortgage? Press Y to yes and N to no")
        print("assuming NO here..and moving forward")
        return True if str(raw_input()).lower() == "y" else False
        # return False

    def build_house(self, game_state):
        """
        return the box number where you wanna build house
        :param game_state:
        :return:
        """
        print("Player %s give the position of the box where you wanna build house "%(self.id, ))
        return int(raw_input())

    def wanna_sell_house(self, game_state):
        print("Player ", self.id, " wanna sell house? Press Y to yes and N to no")
        return True if str(raw_input()).lower()=="y" else False
        # print("assuming NO here..and moving forward")
        # return False

    def sell_house(self, game_state):
        """
        return the box number where you wanna SELL house
        :param game_state:
        :return:
        """
        print("Player %s give the position of the box where you wanna SELL house "%(self.id, ))
        return int(raw_input())

    def mortgage(self, game_state):
        """
        return the box number which you wanna mortgage
        :param game_state:
        :return: box_number
        """
        print("Player %s give the position of the box which you wanna mortgage " % (self.id,))
        return int(raw_input())


    def wanna_buy(self, game_state, current_box):
        print("Player %s , do u wanna buy your current box %s. Press Y to confirm" % (self.id, current_box.display_name))
        return True if str(raw_input()).lower() == "y" else False

    def wanna_use_jail_card(self, game_state):
        print("Player %s , do u wanna use jail card here. Press Y to confirm")
        return True if str(raw_input()).lower() == "y" else False

    def wanna_pay_for_jail(self, game_state):
        print("Player do u wanna pay money to get out of the jail. Press Y to confirm")
        return True if str(raw_input()).lower() == "y" else False

    def respond_auction(self, game_state, box_index):
        """
        this is blind auction
        :param game_state:
        :param box_index:
        :return: the integer value price
        """
        box = game_state.boxes[box_index]
        print("Enter the price with which you wanna buy this property...")
        return int(raw_input())

    def respond_trade(self, game_state, box):
        pass