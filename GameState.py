import random
import json

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
        self.color = kwargs.get("color", None)
        self.display_name = kwargs["display_name"]
        self.no_house_rent = kwargs.get("no_house_rent", None)
        self.rent_with_color_set = kwargs.get("rent_with_color_set", None)
        self.rent_with_one_house = kwargs.get("rent_with_one_house", None)
        self.rent_with_two_house = kwargs.get("rent_with_two_house", None)
        self.rent_with_three_house = kwargs.get("rent_with_three_house", None)
        self.rent_with_four_house = kwargs.get("rent_with_four_house", None)
        self.rent_with_hotel = kwargs.get("rent_with_hotel", None)
        self.buy_house_cost = kwargs.get("buy_house_cost", None)
        self.buy_hotel_cost = kwargs.get("buy_hotel_cost", None)
        self.buy_cost = kwargs.get("buy_cost", 10000000)
        self.mortgage_val = kwargs.get("mortgage_val", -10000000)

    def is_valid_state(self, state):
        if state>7 or state<-7:
            return False
        return True

    def set_property_state(self, state):
        self.state = state

    def get_property_state(self):
        return self.state

    def is_jail(self):
        return self.special == "JAIL"

    def is_chance(self):
        return self.special == "CHANCE"

    def is_community_chest(self):
        return self.special == "COMMUNITY CHEST"

    def is_utility(self):
        return self.special=="UTILITY"

    def is_station(self):
        return self.special=="STATION"

    def is_start(self):
        return self.special=="START"

    def is_special(self):
        if self.special and self.special in ["COMMUNITY CHEST", "CHANCE", "JAIL", "INCOME TAX", "FREE PARKING"]:
            return True
        return False

    def rent_to_be_paid(self):
        """
        Based on the state of the property charge will be decided, for example if there are 2 houses then the rent
        to be paid = rent_with_two_house
        :return: cost to be paid by the opponent when he lands here
        """
        state = abs(self.state)
        if state==1:
            return self.no_house_rent
        elif state==2:
            return self.rent_with_one_house
        elif state==3:
            return self.rent_with_two_house
        elif state==4:
            return self.rent_with_three_house
        elif state==5:
            return self.rent_with_four_house
        elif state==6:
            return self.rent_with_hotel

class Player(object):
    def __init__(self, id, game_agent, inital_cash=0):
        self.id = id
        self.cash = inital_cash
        self.position = 0
        self.agent = game_agent

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
        self.position += val
        self.position = self.position % 40



class Bank(object):
    def __init__(self, initial_cash=100000):
        self.cash = initial_cash
        self.mortgages = []
        self.unsold_properties = range(0, 40)

    def want_to_make_auction(self, position, game_state):
        """
        :param position:
        :return: true of false saying whether the bank want to make a auction of property at given position
        """
        box = game_state.get_box(position)
        if box.is_special():
            return False
        # with some probability make a decision whether to return True or False

    def auction(self, position, game_state):
        pass


class Dice(object):
    def __init__(self):
        pass

    def roll(self):
        print("Enter the DICE values (comma seperated)")
        return [int(x.strip()) for x in str(raw_input()).strip().split(",")[:2]]
        #return (random.randint(1, 6), random.randint(1, 6))



class GameState(object):
    def __init__(self):
        super(GameState, self).__init__()
        self.turn_number = 0
        self.boxes = [None]*40
        self.dice_values = [None, None]
        self.players_positions = [None, None]
        self.players_cash = [None, None]
        self.double_count = 0
        self.rent_to_be_paid = [None, None]

    def load_state(self, file_name):
        print("loading GAME STATE from disk.....")
        f = open(file_name, "r")
        d = json.loads(f.read())
        f.close()
        for i in range(0, 40):
            self.boxes[i] = Box(**d[str(i)])

    def give_jail_box_index(self):
        for index, each_box in enumerate(self.boxes):
            if each_box.is_jail():
                return index
        return -1


# self.game_state.load_state("each_box_data.json")

class GameEngine(object):
    def __init__(self, game_state, player1, player2, bank):
        self.game_state = game_state
        self.p1 = player1
        self.p2 = player2
        self.bank = bank
        self.dice = Dice()

    def get_players(self):
        return (self.p1, self.p2) if self.game_state.turn_number%2 == 0 else (self.p2, self.p1)

    def run(self):
        while True:
            self.bmst()
            self.dice_roll()
            self.move_the_player()
            self.square_effect()
            self.bmst()
            self.decide_players_chance()
            print("one round is done PRESS ENTER to continue")
            raw_input()



    # -------- states begin
    def decide_players_chance(self):
        if list(self.game_state.dice_values)==[1,1]:
            print("the current player got a double so  he gets another chance")
            if self.game_state.double_count >= 3:
                print("the current player got a double more than 3 times so now give chance to other player")
                self.game_state.double_count = 0
                self.game_state.turn_number += 1
        else:
            print("The current user chance is done, now we will give chance to other player")
            self.game_state.turn_number += 1

    def square_effect(self):
        curr, other = self.get_players()
        curr_pos = curr.get_position()
        curr_box = self.game_state.boxes[curr_pos]
        if curr_box.is_special():
            print("current box is special box")
            if curr_box.is_chance():
                self.chance_state()
            elif curr_box.is_community_chest():
                self.community_chest_state()
            elif curr_box.is_jail():
                self.jail_state()
        else:
            # buying unowned property
            if curr_box.state==0:
                print("the current box is unowned by any one so the user can buy")
                self.bmst()
                self.buy_state()
                self.auction_state()
            # landed on already existing
            elif abs(curr_box.state)<7:
                if (curr.id==0 and curr_box.state>0) or (curr.id>0 and curr_box.state<0):
                    # Landed in your own property
                    print("the player landed in his own property..")
                    pass
                else:
                    print("the player landed in other players property..")
                    rent_to_be_paid = curr_box.rent_to_be_paid()
                    self.make_player_to_pay_money(curr, rent_to_be_paid, " landed in "+curr_box.display_name)
                    # print("the rent to be paid is ", rent_to_be_paid)
                    # x, y = self.game_state.rent_to_be_paid
                    # if curr.id==self.p1.id:
                    #     self.game_state.rent_to_be_paid = [rent_to_be_paid, y]
                    # else:
                    #     self.game_state.rent_to_be_paid = [x, rent_to_be_paid]
                    # if curr.remove_cash(rent_to_be_paid):
                    #     print("rent paid successfully")
                    #     other.add_cash(rent_to_be_paid)
                    # else:
                    #     print("the player dont have cash...so lets do BMST")
                    #     self.bmst()
                    #     if curr.remove_cash(rent_to_be_paid):
                    #         print("AFTER BMST the player got some money to pay")
                    #         other.add_cash(rent_to_be_paid)
                    #     else:
                    #         print("THE PLAYER ", curr.id, " lost the game...unable to pay the money")
                    #         print("player ", other.id, " won the game")
                    #         exit()
            # landed in mortgaged property
            else:
                print("the player landed in mortgaged property")

    def chance_state(self):
        curr, other = self.get_players()
        print("this is the chance state")
        n = 16
        i = random.randint(1, n)
        if i == 1:
            pass
        elif i == 2:
            pass
        elif i == 3:
            pass
        elif i == 4:
            pass
        elif i == 5:
            pass
        elif i == 6:
            pass
        elif i == 7:
            pass
        if i == 8:
            pass
        elif i == 9:
            pass
        elif i == 10:
            pass
        elif i == 11:
            pass
        elif i == 12:
            pass
        elif i == 13:
            pass
        elif i == 14:
            pass
        elif i == 15:
            pass
        elif i == 16:
            pass

    def community_chest_state(self):
        curr, other = self.get_players()
        print("this is community chest state")
        # total there are 17 cards
        n = 17
        i = random.randint(1, n)
        print("in community chest the player got ", i)
        if i == 1:
            curr.set_position(0)
            self.move_the_player()
        elif i==2:
            curr.add_cash(200)
        elif i==3:
            self.make_player_to_pay_money(curr, 50, " doctors fee (chance 3)")
        elif i==4:
            curr.add_cash(50)
        elif i==5:
            pass
        elif i==6:
            curr.set_position(self.game_state.give_jail_box_index())
            self.move_the_player(reward=False)
        elif i==7:
            curr.add_cash(50)
            self.make_player_to_pay_money(other, 50, "GRAND OPERA NIGHT (chance 7 by other player)")
        if i == 8:
            curr.add_cash(100)
        elif i==9:
            curr.add_cash(20)
        elif i==10:
            self.make_player_to_pay_money(other, 10, " other players birthday (chance 10 by other player)")
        elif i==11:
            curr.add_cash(100)
        elif i==12:
            self.make_player_to_pay_money(curr, 50, " hospital fee (chance 12)")
        elif i==13:
            self.make_player_to_pay_money(curr, 50, "school fee (chance 13)")
        elif i==14:
            curr.add_cash(25)
        elif i==15:
            pass
        elif i==16:
            curr.add_cash(10)
        elif i==17:
            curr.add_cash(100)

    def jail_state(self):
        print("this is jail state")
        curr, _ = self.get_players()
        rent_to_be_paid = 500
        self.make_player_to_pay_money(curr, rent_to_be_paid, " jail rent ")


    def auction_state(self):
        print("Auction has to happen now... but not yet implemented")

    def move_the_player(self, reward=True):
        curr, _ = self.get_players()
        if self.game_state.double_count==3:
            print("3 times double count detected ")
            jail_index = self.game_state.give_jail_box_index()
            print("the index of jail box is ", jail_index)
            curr.set_position(jail_index)
            # self.game_state.double_count = 0
        else:
            prev = curr.get_position()
            curr.move_position(self.game_state.dice_values[0] + self.game_state.dice_values[1])
            if prev>curr.get_position() and reward:
                print("the player crossed START. So rewarding him with 200 $")
                curr.add_cash(200)
        print("PLAYER ", curr.id, " has been moved to box index ", curr.get_position())
        if curr.id == self.p1.id:
            self.game_state.players_positions = [curr.get_position(), self.game_state.players_positions[1]]
        else:
            self.game_state.players_positions = [self.game_state.players_positions[0], curr.get_position()]

    def dice_roll(self):
        if self.game_state.turn_number%2==0:
            print("PLAYER 0 is Rolling the dice ")
        else:
            print("PLAYER 1 is Rolling the dice ")
        self.game_state.dice_values = self.dice.roll()
        print("Dice Values are %s , %s"%tuple(self.game_state.dice_values))
        if self.game_state.dice_values == [1,1]:
            self.game_state.double_count += 1
        # else:
        #     self.game_state.double_count = 0


    def bmst(self):
        # print("assume BSMT is done with no player want to do any buy or sell or trade .....")
        # return
        while True:
            build_house_1, build_house_2 = self.build_house_state()
            sell_house_1, sell_house_2 = self.sell_house_state()
            trade_1, trade_2 = self.trade_state()
            mort_1, mort_2 = self.mortgage_state()
            if not build_house_1 and not build_house_2 and not sell_house_1 and not sell_house_2 \
                and not trade_1 and not trade_2 and not mort_1 and not mort_2:
                break

    def build_house_state(self):
        curr, other = self.get_players()
        bh_1 = curr.agent.wanna_build_house(self.game_state)
        if bh_1:
            self.build_house(curr)
        bh_2 = other.agent.wanna_build_house(self.game_state)
        if bh_2:
            self.build_house(other)
        return (bh_1, bh_2)

    def sell_house_state(self):
        curr, other = self.get_players()
        sh_1 = curr.agent.wanna_sell_house(self.game_state)
        if sh_1:
            self.sell_house(curr)
        sh_2 = other.agent.wanna_sell_house(self.game_state)
        if sh_2:
            self.sell_house(other)
        return (sh_1, sh_2)

    def trade_state(self):
        curr, other = self.get_players()
        t_1 = curr.agent.wanna_trade(self.game_state)
        if t_1:
            self.trade(curr)
        t_2 = other.agent.wanna_trade(self.game_state)
        if t_2:
            self.trade(other)
        return (t_1, t_2)

    def mortgage_state(self):
        curr, other = self.get_players()
        m_1 = curr.agent.wanna_mortgage(self.game_state)
        if m_1:
            self.mortgage(curr)
        m_2 = other.agent.wanna_mortgage(self.game_state)
        if m_2:
            self.mortgage(other)
        return (m_1, m_2)

    def buy_state(self):
        curr, other = self.get_players()
        current_pos = self.game_state.players_positions[curr.id]
        current_box = self.game_state.boxes[current_pos]
        if not current_box.is_start() and not current_box.is_community_chest() and not current_box.is_chance() and current_box.state==0:
            # if the given box is not special, then allow the user to buy the box
            if curr.agent.wanna_buy(self.game_state, current_box) :
                print("PLAYER ", curr.id, " is interested to buy the current box")
                # user is interested to buy the current box
                if curr.remove_cash(current_box.buy_cost):
                    current_box.state = 1 if curr.id==self.p1.id else -1
        else:
            print("No one can buy this box because it is not in buyable state..")


    # -------------- states end

    # UTILITY FUNCTIONS START

    def build_house(self, player):
        box_pos = player.agent.build_house(self.game_state)
        box = self.game_state.boxes[box_pos]
        if abs(box.state) >=1 and abs(box.state)<5:
            box.state = box.state + (1 if box.state>0 else -1)
        else:
            print("UNABLE TO BUILD THE HOUSE, current state is ", box.state)

    def sell_house(self, player):
        box_pos = player.agent.sell_house(self.game_state)
        box = self.game_state.boxes[box_pos]
        # when the player sell the house, he will get money half of the money he bought the house
        player.add_cash(box.buy_house_cost/2)
        box.state = box.state - (1 if box.state>0 else -1)

    def trade(self, player):
        pass

    def mortgage(self, player):
        box_pos = player.agent.mortgage(self.game_state)
        box = self.game_state.boxes[box_pos]
        player.add_cash(box.mortgage_val)
        box.state = 7 if player.id==self.p1.id else -7

    def make_player_to_pay_money(self, player, money, purpose):
        rent_to_be_paid = money
        x, y = self.game_state.rent_to_be_paid
        if player.id == self.p1.id:
            self.game_state.rent_to_be_paid = [rent_to_be_paid, y]
        else:
            self.game_state.rent_to_be_paid = [x, rent_to_be_paid]
        print("player ", player.id, " currently have ", player.cash, " before deduction")
        if player.remove_cash(rent_to_be_paid):
            print("money deducted from player ", player.id, " for the purpose ", purpose)
        else:
            print("the player dont have cash...so lets do BMST")
            self.bmst()
            if player.remove_cash(rent_to_be_paid):
                print("AFTER BMST the player got some money to pay  for the purpose ", purpose)
            else:
                print("THE PLAYER ", player.id, " lost the game...unable to pay the money for the purpose ", purpose)
                exit()
        print("player ", player.id, " currently have ", player.cash, " after deduction")

    def get_player_houses(self, player):
        if player.id ==0:
            pass
        else:
            pass


