from constants import board as board
from config import log as log
import random


class GameState:
    def __init__(self, my_id):
        self.p1 = {"id": 1, "position": -1, "jail_cards": [], "houses": [], "cash": 0, "debt": 0, "to_whom": 0}
        self.p2 = {"id": 2, "position": -1, "jail_cards": [], "houses": [], "cash": 0, "debt": 0, "to_whom": 0}
        self.active_player = self.p1
        self.inactive_player = self.p2
        self.status = [0]*42
        self.phases = ["BMST", "TRADE", "DICE", "BUY", "AUCTION", "PAY", "JAIL", "CHANCE", "COMMUNITY_CHEST"]
        self.additional_info = None
        self.current_position = 0
        self.my_id = my_id
        self.stats = []

    def update(self, state):
        turn_number = state[0]

        self.p1["position"] = state[2][0]
        self.p2["position"] = state[2][1]
        self.status = list(state[1])
        self.p1["jail_cards"] = [x for x in [40, 41] if x == self.p1["id"]]
        self.p2["jail_cards"] = [x for x in [40, 41] if x == self.p2["id"]]
        self.p1["cash"] = state[3][0]
        self.p2["cash"] = state[3][1]
        self.current_phase = self.phases[state[4]]
        self.additional_info = state[5]

        if self.current_phase == "BMST":
            self.p1["debt"] = state[6][0]
            self.p1['to_whom'] = state[6][1]
            self.p2["debt"] = state[6][2]
            self.p2['to_whom'] = state[6][3]

        if turn_number % 2 == 0:
            self.active_player = self.p1
            self.inactive_player = self.p2
            self.current_position = self.p1["position"]
        else:
            self.active_player = self.p2
            self.inactive_player = self.p1
            self.current_position = self.p2["position"]

        d = {}
        d["p1_how_many_houses"] = self.get_houses_count(self.p1)
        d["p1_cash"] = self.p1["cash"]
        d["p1_how_many_properties"] = self.get_props_count(self.p1)
        d["p1_how_many_mortgaged"] = self.get_mortgaged_count(self.p1)
        d["p2_how_many_houses"] = self.get_houses_count(self.p2)
        d["p2_cash"] = self.p2["cash"]
        d["p2_how_many_properties"] = self.get_props_count(self.p2)
        d["p2_how_many_mortgaged"] = self.get_mortgaged_count(self.p2)

        self.stats += [d]


    def get_houses_count(self, person=None):
        compare_with = 1 if person["id"] == self.p1["id"] else -1
        ans = []
        for i, each in enumerate(self.status):
            if each*compare_with > 0 and abs(each)>1 and abs(each)<7 and i<40:
                ans += [(i, abs(each)-1)]
        return len(ans)

    def get_props_count(self, person=None):

        compare_with = 1 if person["id"] == self.p1["id"] else -1
        ans = []
        for i, each in enumerate(self.status):
            if each * compare_with > 0 and abs(each) >= 1 and abs(each) < 7 and i < 40:
                ans += [i]
        return len(ans)

    def get_mortgaged_count(self, person=None):
        compare_with = 1 if person["id"] == self.p1["id"] else -1
        ans = []
        for i, each in enumerate(self.status):
            if each * compare_with > 0 and abs(each) == 7 and i < 40:
                ans += [i]
        return len(ans)



class Agent:
    def __init__(self, id):
        self.id = id
        self.game_state = GameState(id)
        self.me = self.game_state.p1 if self.game_state.p1["id"] == id else self.game_state.p2
        self.other = self.game_state.p2 if self.game_state.p1["id"] == id else self.game_state.p1


    def getBSMTDecision(self, state):
        self.game_state.update(state)
        # if current property state is unsold substract the debt
        if self.me["id"] == self.game_state.active_player["id"] and self.game_state.status[self.game_state.active_player["position"]]==0:
            self.me["debt"] -= board[self.game_state.active_player["position"]]["price"]

        if self.me["debt"] > self.me["cash"]:
            # this is emergency phase, sell as much as you can to make money
            return self.emergency_phase()
        elif self.game_state.active_player["id"] == self.id:
            return self.bmst_my_turn()
            # bsmt in my turn
        else:
            # bmst in other player turn
            return self.bmst_other_player_turn()

    def buyProperty(self, state):
        self.game_state.update(state)
        # never buy utility, always buy railroad
        # late game and early game
        if self.me["cash"] >= board[self.game_state.current_position]["price"]:
            # choose the buying decision with some probability
            if random.randint(0, 1) == 1:
                return True
        return False


    def auctionProperty(self, state):
        self.game_state.update(state)
        auction_price = int(board[self.game_state.current_position]["price"]*random.uniform(0, 1))
        if self.me["cash"]>=auction_price:
            return auction_price
        return 0

    def respondTrade(self, state):
        self.game_state.update(state)
        tt = self.game_state.additional_info
        cash_offer = int(tt[-4])
        properties_offered = tt[-3]
        cash_req = int(tt[-2])
        properties_requested = tt[-1]
        if self.me["cash"] + cash_offer >= cash_req:
            if random.randint(0, 1)==1:
                return True
        return False


    def jailDecision(self, state):
        # based on early and late game
        self.game_state.update(state)
        if self.me["jail_cards"]:
            return ("C", self.me["jail_cards"][0])
        if self.me["cash"]>=50:
            if random.randint(0, 1)==1:
                return ("P" ,)
        return ("R", )

    def receiveState(self, state):
        self.game_state.update(state)
        pass

    # utility functions

    def get_all_houses(self, person=None):
        if person is None:
            person = self.me
        compare_with = 1 if person["id"] == self.game_state.p1["id"] else -1
        ans = []
        for i, each in enumerate(self.game_state.status):
            if each*compare_with > 0 and abs(each)>1 and abs(each)<7 and i<40:
                ans += [(i, abs(each)-1)]
        return ans

    def get_all_owned(self, person=None):
        if person is None:
            person = self.me
        compare_with = 1 if person["id"] == self.game_state.p1["id"] else -1
        ans = []
        for i, each in enumerate(self.game_state.status):
            if each * compare_with > 0 and abs(each) >= 1 and abs(each) < 7 and i < 40:
                ans += [i]
        return ans

    def emergency_phase(self):
        all_houses = self.get_all_houses(person=self.me)
        money_req = self.me["debt"] - self.me["cash"]
        houses_to_sell = []
        for index,count in all_houses:
            if money_req > 0:
                houses_to_sell += [(index, 1)]
                money_req -= int(board[index]["build_cost"]/2)
        if houses_to_sell:
            return ("S", houses_to_sell)

        props_owned = self.get_all_owned(person=self.me)
        props_to_sell = []
        for index in props_owned:
            if money_req > 0:
                props_to_sell += [index]
                money_req -= int(board[index]["price"]/2)
        if props_to_sell:
            return ("M", props_to_sell)


    def bmst_my_turn(self):
        build_house_locations = []
        total_budget = self.me["cash"]
        for each in self.get_all_owned():
            monopoly = [each] + board[each]["monopoly_group_elements"]
            if all(x in monopoly for x in self.get_all_owned(person=self.me)):
                if total_budget-board[each]["build_cost"] >=0:
                    total_budget -= board[each]["build_cost"]
                    build_house_locations += [(each, 1)]
                    break
        if build_house_locations and total_budget >= 0 and random.randint(0, 1)==1:
            return ("B", build_house_locations)


    def bmst_other_player_turn(self):
        return self.bmst_my_turn()







