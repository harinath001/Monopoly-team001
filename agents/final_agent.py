from constants import board as board
from config import log as log


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

    def get_rent(self, prop, state):
        flag = (self.id * 2) - 3
        status = state[self.PROPERTIES_STATUS_INDEX][prop]
        if (flag * status) == -1:
            return board[prop]['price'], False
        elif (flag * status) == -2:
            return board[prop]['rent_house_1'], True
        elif (flag * status) == -3:
            return board[prop]['rent_house_2'], True
        elif (flag * status) == -4:
            return board[prop]['rent_house_3'], True
        elif (flag * status) == -5:
            return board[prop]['rent_house_4'], True
        elif (flag * status) == -6:
            return board[prop]['rent_hotel'], True
        elif (flag * status) == -7:
            return 0, False
        elif (flag * status) == 0:
            return 0, False
        else:
            return -1, False

    def get_owned_prop(self, state, max_t):
        props = []
        for p in list(range(1, 40)):
            if ((state[self.PROPERTIES_STATUS_INDEX][p] >= 1) and (state[self.PROPERTIES_STATUS_INDEX][p] <= max_t) & (
                    self.id == 1)):
                props.append(p)
            elif ((state[self.PROPERTIES_STATUS_INDEX][p] >= -1 * max_t) and (
                    state[self.PROPERTIES_STATUS_INDEX][p] <= -1) and (self.id == 2)):
                props.append(p)
        return props

    def get_opp_owned(self, state, max_t):
        props = []
        for p in list(range(1, 40)):
            if ((state[self.PROPERTIES_STATUS_INDEX][p] >= 1) and (state[self.PROPERTIES_STATUS_INDEX][p] <= max_t) & (
                    self.id == 2)):
                props.append(p)
            elif ((state[self.PROPERTIES_STATUS_INDEX][p] >= -1 * max_t) and (
                    state[self.PROPERTIES_STATUS_INDEX][p] <= -1) and (self.id == 1)):
                props.append(p)
        return props

    def get_missing_monopoly(self, p, state, op_owned):
        other_props = board[p]['monopoly_group_elements']

        found_1_missing = False
        idx = -1

        for other in other_props:
            if self.get_rent(other, state)[0] == 0:
                return False, -1
            if other in op_owned:
                if found_1_missing:
                    return False, -1
                else:
                    idx = other
                    found_1_missing = True

        return found_1_missing, idx

    def get_complete_monopolies(self, props, state):

        ans = []

        for p in props:
            other_props = board[p]['monopoly_group_elements']
            own_all = True
            for other in other_props:
                if board[other]["rent_house_1"] == 0:
                    own_all = False
                if (self.get_rent(other, state)[0] == 0) or (self.get_rent(other, state)[0] == -1):
                    own_all = False
            if own_all:
                ans.append(p)

        return ans

    def get_next_to_build(self, props, state):

        min_st = 1000
        ans = -1
        for prop in props:
            st = abs(state[self.PROPERTIES_STATUS_INDEX][prop])
            if st < min_st and abs(st) != 6:
                min_st = st
                ans = prop
        return ans

    def __init__(self, id):
        self.id = id
        self.game_state = GameState(id)
        self.TURN_NUMBER_INDEX = 0
        self.PROPERTIES_STATUS_INDEX = 1
        self.PLAYER_POSITIONS_INDEX = 2
        self.PLAYERS_CASH_BALANCE_INDEX = 3
        self.CURRENT_PHASE_INDEX = 4
        self.ADDITIONAL_INDEX = 5
        self.DEBT_INDEX = 6
        self.HISTORY_INDEX = 7

    def getBSMTDecision(self, state):
        self.game_state.update(state)
        # build from starting when passing go.
        # mortgage if have to, from bottom
        # sell from least when can.
        # trade when monopoly missing.

        debt_data = state[self.DEBT_INDEX]
        if self.id == 1:
            debt = debt_data[1]
        else:
            debt = debt_data[3]

        debt_copy = debt
        if state[self.CURRENT_PHASE_INDEX] != 3 and debt_copy > state[self.PLAYERS_CASH_BALANCE_INDEX][self.id - 1]:
            min_inx_sell = {}
            min_inx_mort = []
            while debt_copy > state[self.PLAYERS_CASH_BALANCE_INDEX][self.id - 1]:

                min_rent = 1000
                prop = -1

                props = self.get_owned_prop(state, 6)

                for p in props:
                    if p in min_inx_sell or p in min_inx_mort:
                        continue
                    if self.get_rent(p, state)[0] < min_rent:
                        min_rent, _ = self.get_rent(p, state)
                        prop = p

                if prop == -1:
                    break

                _, flag = self.get_rent(prop, state)

                if flag:
                    if prop in min_inx_sell:
                        min_inx_sell[prop] = min_inx_sell[prop] + 1
                    else:
                        min_inx_sell[prop] = 1
                    debt_copy -= board[prop]['build_cost']/2
                else:
                    min_inx_mort.append(prop)
                    debt_copy -= board[prop]['price'] / 2

            if len(min_inx_sell) > 0:
                return ('S', [(k, v) for k, v in min_inx_sell.items()])
            if len(min_inx_mort) > 0:
                return ('M', min_inx_mort)

        props = self.get_owned_prop(state, 6)
        mpolic = self.get_complete_monopolies(props, state)
        p = self.get_next_to_build(mpolic, state)
        if p != -1 and board[p]['build_cost'] < state[self.PLAYERS_CASH_BALANCE_INDEX][self.id - 1]:
            return ('B', [(p, 1)])

        props_owned = self.get_owned_prop(state, 7)
        op_owned = self.get_opp_owned(state, 6)
        for prop in props_owned:
            flag, mm = self.get_missing_monopoly(prop, state, op_owned)
            if flag:
                return ('T', min(0.7 * state[self.PLAYERS_CASH_BALANCE_INDEX][self.id - 1], 1.5 * board[mm]['price']), [], 0, [mm])

    pass

    def buyProperty(self, state):
        self.game_state.update(state)
        # Buy always when possible

        prop_index = state[self.ADDITIONAL_INDEX]
        if type(prop_index) is not int:
            return
        try:
            price = board[prop_index]['price']
        except Exception as ex:
            print(state[self.CURRENT_PHASE_INDEX])
            print(prop_index)
            raise(ex)

        cur_cash = state[self.PLAYERS_CASH_BALANCE_INDEX][self.id - 1]

        other_props = board[prop_index]['monopoly_group_elements']
        props_owned = self.get_owned_prop(state, 7)

        all_owned = True
        for op in other_props:
            if not(op in props_owned):
                all_owned = False

        if all_owned:
            return True

        return cur_cash > price and cur_cash > 400

    def auctionProperty(self, state):
        self.game_state.update(state)
        # Always bid 10%
        return int(state[self.PLAYERS_CASH_BALANCE_INDEX][self.id - 1] / 5)

    def respondTrade(self, state):
        self.game_state.update(state)
        # if increases rent amount, do it.

        if state[self.CURRENT_PHASE_INDEX] == 1:
            tt = state[self.ADDITIONAL_INDEX]
            cash_offer = tt[-4]
            properties_offered = tt[-3]
            cash_req = tt[-2]
            properties_requested = tt[-1]
        else:
            return False

        total_money_lost = 0

        for prop_requested in properties_requested:
            other_props = board[prop_requested]['monopoly_group_elements']
            own_all = True
            for other_p in other_props:
                if ((state[self.PROPERTIES_STATUS_INDEX][other_p] >= 1) & (
                        state[self.PROPERTIES_STATUS_INDEX][other_p] <= 7) & (self.id == 1)):
                    continue
                elif ((state[self.PROPERTIES_STATUS_INDEX][other_p] >= -7) & (
                        state[self.PROPERTIES_STATUS_INDEX][other_p] <= -1) & (self.id == 2)):
                    continue
                own_all = False

            if own_all:
                total_money_lost += board[prop_requested]['rent'] * 4 + board[prop_requested]['price']
            else:
                total_money_lost += board[prop_requested]['rent'] + board[prop_requested]['price']

        total_money_lost += cash_req

        total_money_gained = 0
        for prop_offered in properties_offered:
            other_props = board[prop_offered]['monopoly_group_elements']
            own_others = True
            for other_p in other_props:
                if ((state[self.PROPERTIES_STATUS_INDEX][other_p] >= 1) & (
                        state[self.PROPERTIES_STATUS_INDEX][other_p] <= 7) & (self.id == 1)):
                    continue
                elif ((state[self.PROPERTIES_STATUS_INDEX][other_p] >= -7) & (
                        state[self.PROPERTIES_STATUS_INDEX][other_p] <= -1) & (self.id == 2)):
                    continue

                own_others = False

            if own_others:
                total_money_gained = board[prop_offered]['rent'] * 4 + board[prop_offered]['price']
            else:
                total_money_gained = board[prop_offered]['rent'] + board[prop_offered]['price']
        total_money_gained += cash_offer

        return total_money_gained > (1.2 * total_money_lost)

    def jailDecision(self, state):
        self.game_state.update(state)

        if state[self.PLAYERS_CASH_BALANCE_INDEX][self.id - 1] > 1000:
            return "P"

        # Roll always
        return "R"

    def receiveState(self, state):
        self.game_state.update(state)
        pass
