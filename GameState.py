import random
import json
from Box import Box


class Dice(object):
    def __init__(self):
        pass

    def roll(self):
        print("Enter the DICE values (comma seperated)")
        # return [int(x.strip()) for x in str(raw_input()).strip().split(",")[:2]]
        return [random.randint(1, 6), random.randint(1, 6)]



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
        self.rent_paid_to = [None, None]
        self.jail_cards = [-1, -1] # first index is for first card owner and 2nd index is for 2nd card owner

    def load_state(self, file_name):
        print("loading GAME STATE from disk.....")
        f = open(file_name, "r")
        d = json.loads(f.read())
        f.close()
        for i in range(0, 40):
            k = d[str(i)]
            k["position_number"]= i
            self.boxes[i] = Box(**k)


    def give_jail_box_index(self):
        for index, each_box in enumerate(self.boxes):
            if each_box.is_jail():
                return index
        return -1

    def get_all_houses_boxes_indexes(self, player_id):
        ans = []
        for i, each in enumerate(self.boxes):
            if player_id==0:
                if each.state >1 and each.state<6:
                    ans += [i]
            else:
                if each.state <-1 and abs(each.state)<6:
                    ans += [i]
        return ans

    def get_all_hotels_boxes_indexes(self, player_id):
        ans = []
        for i, each in enumerate(self.boxes):
            if player_id==0:
                if each.state == 6:
                    ans += [i]
            else:
                if each.state <-1 and abs(each.state)==6:
                    ans += [i]
        return ans

    def get_all_owned_boxes(self, player_id):
        ans = []
        for i, each in enumerate(self.boxes):
            if player_id==0:
                if each.state >0 and each.state<7:
                    ans += [i]
            else:
                if each.state <0 and abs(each.state)<7:
                    ans += [i]
        return ans

    def get_all_mortgaged_boxes(self, player_id):
        ans = []
        for i, each in enumerate(self.boxes):
            if player_id == 0:
                if each.state > 0 and each.state == 7:
                    ans += [i]
            else:
                if each.state < 0 and abs(each.state) == 7:
                    ans += [i]
        return ans

    def get_all_owned_same_colored_boxes(self, player_id, color):
        ans = []
        temp = self.get_all_owned_boxes(player_id)
        for each in temp:
            if self.boxes[each].color == color:
                ans += [each]
        return ans

    def get_rent_to_be_paid(self, owner_id, box_index):
        box = self.boxes[box_index]
        r = box.rent_to_be_paid()
        if not r:
            print("rent has to be something..")
            raise NotImplementedError("rent cannot be null")
            return None
        if box.special == "UTILITY":
            owned_boxes = self.get_all_owned_boxes(owner_id)
            if "train" in str(box.display_name).lower():
                count = 0
                for each in owned_boxes:
                    if "train" in str(self.boxes[each].display_name).lower():
                        count+=1
                r = (2**(count-1))*r
            elif "tap" in str(box.display_name).lower():
                r = (self.dice_values[0]+self.dice_values[1]) * r
            elif "bulb" in str(box.display_name).lower():
                r = (self.dice_values[0] + self.dice_values[1]) * r
        elif abs(box.state)==1:
            all_same_coloured_boxes = self.get_all_owned_same_colored_boxes(owner_id, box.color)
            if len(all_same_coloured_boxes)>=3:
                r = r*2
        return r

    def is_player_eligible_to_build_house_at_box(self, player_id, at):
        box = self.boxes[at]
        if (player_id==0 and box.state>0 and abs(box.state)<=5) or (player_id==1 and box.state<0 and abs(box.state)<=5):
            color = box.color
            same_color_boxes = [x for x in self.boxes if x.is_owned_by(player_id) and x.color==color]
            if len(same_color_boxes)>=3:
                return True
        return False

    def is_player_eligible_to_sell_house_at_box(self, player_id, at):
        box = self.boxes[at]
        if box.is_owned_by(player_id) and abs(box.state)<7 and abs(box.state)>1:
            return True
        return False

    def assign_a_property_to_player(self, player_id, box_index):
        self.boxes[box_index].state = 1 if player_id==0 else -1

    def revoke_a_property_from_player(self, player_id, box_index):
        self.boxes[box_index].state = 7 if player_id==0 else -7

    def convert_to_state(self, phase, to_player, **kwargs):
        phase_to_number = {"bmst": 0, "trade": 1, "dice": 2, "buy": 3, "auction": 4, "pay": 5, "jail": 6, "chance": 7, "community_chest": 8}
        turn_number = self.turn_number
        status_of_each_property = []
        for each_box in self.boxes:
            status_of_each_property += [each_box.state]
        # add status of jail cards
        status_of_each_property += [(self.jail_cards[0]+1 if self.jail_cards[0]<1 else -1), (self.jail_cards[0]+1 if self.jail_cards[1]<1 else -1)]
        status_of_each_property = tuple(status_of_each_property)
        positions = tuple(self.players_positions)
        cash_holdings = tuple(self.players_cash)
        current_phase = phase_to_number[phase]
        additional_field = None
        if phase=="bmst":
            "contains debt value"
            to_whom_debt = self.rent_paid_to[to_player.id]#0 or 1 or 2
            debt_value = self.rent_to_be_paid[to_player.id] # some debt value
            additional_field = (to_whom_debt, debt_value)
        elif phase == "dice":
            "additional phase contains dice values"
            additional_field = tuple(self.dice_values)
        elif phase == "buy":
            "additional field contains property number"
            additional_field = self.players_positions[to_player.id]
        elif phase =="auction":
            "additional field contains property value"
        elif phase =="trade":
            "additional field contains other players offer"
        elif phase == "pay":
            "additonal field contains the property number"
        elif phase == "jail":
            ""
        elif phase == "chance":
            "additional field contains 0 to 15"
        elif phase == "community_chest":
            "additonal field contains 0 to 16"
        return (turn_number, status_of_each_property, positions, cash_holdings, current_phase, additional_field)



