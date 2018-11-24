
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



class Box(object):

    def __init__(self, **kwargs):
        """
        :param position_number: index of the box from start position
        :param kwargs: it contain all other information about the box like color, name etc
        """
        self.state = kwargs.get("state", 0)
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
        self.buy_hotel_cost = kwargs.get("buy_hotel_cost", self.buy_house_cost)
        self.sell_house_cost = kwargs.get("sell_house_cost", None)
        if self.buy_house_cost is not None:
            self.sell_house_cost = self.buy_house_cost/2
        self.sell_hotel_cost = kwargs.get("sell_hotel_cost", None)
        if self.buy_hotel_cost is not None:
            self.sell_hotel_cost = self.buy_hotel_cost/2
        self.buy_cost = kwargs.get("buy_cost", 10000000)
        self.mortgage_val = kwargs.get("mortgage_val", -10000000)
        self.unmortgage_val = kwargs.get("unmortgage_val", self.mortgage_val)
        if self.mortgage_val:
            self.unmortgage_val = self.mortgage_val + self.mortgage_val/10
        self.tax = kwargs.get("tax", None)
        self.nearest_railroad = kwargs.get("nearest_railroad", None)
        self.nearest_utility = kwargs.get("nearest_utility", None)
        self.members_of_monopoly = kwargs.get("members_of_monopoly", [])


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

    def is_normal(self):
        return self.special is None


    def is_start(self):
        return self.special=="START"

    def is_special(self):
        return not self.is_normal()

    def is_tax_box(self):
        if self.tax:
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

    def is_owned_by(self, player_id, ignore_mortgaged=True):
        if self.state==0:
            return False
        if self.state>0 and player_id==0:
            if abs(self.state)<7:
                return True
            elif ignore_mortgaged:
                return True
        if self.state<0 and player_id==1:
            if abs(self.state)<7:
                return True
            elif ignore_mortgaged:
                return True
        return False

    def number_of_houses(self, player_id):
        if (player_id == 0 and self.state>0) or (player_id >0 and self.state<0):
            if abs(self.state)==7:
                return -1
            else:
                return abs(self.state)-1
        return -1

    def is_buyable(self):
        if self.special is None or self.special == "UTILITY":
            return True
        return False

class JailBox:
    def __init__(self, game_state, position):
        self.game_state = game_state
        self.position = position
        self.state = 0

    def is_owned_by(self, player_id):
        return self.game_state.jail_cards[self.position-40] == player_id

    def get_state(self):
        pass

    def is_unowned(self):
        return self.game_state.jail_cards[self.position-40]==-1

    def make_owner(self, player_id):
        self.game_state.jail_cards[self.position-40] = player_id

    def give_back_to_bank(self):
        self.game_state.jail_cards[self.position-40] = -1
    