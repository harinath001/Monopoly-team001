import random
import json
from Box import Box, JailBox
import pdb


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
        self.boxes += [JailBox(self, 40), JailBox(self, 41)]


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
            if "rail" in str(box.display_name).lower() or box.position in [5, 15, 25, 35]:
                count = 0
                for each in owned_boxes:
                    if "rail" in str(self.boxes[each].display_name).lower() or self.boxes[each].position in [5, 15, 25, 35]:
                        count+=1
                r = (2**(count-1))*r
            elif "tap" in str(box.display_name).lower() or "water works" in str(box.display_name).lower():
                r = (self.dice_values[0]+self.dice_values[1]) * r
            elif "bulb" in str(box.display_name).lower() or "electric company" in str(box.display_name).lower():
                r = (self.dice_values[0] + self.dice_values[1]) * r
        elif abs(box.state)==1:
            if self.is_colour_group_owned(box_index, owner_id,ignore_mortgaged=True):
                r = 2*r
        return r

    def is_player_eligible_to_build_houses_at_color_group(self, player_id, new_positions, new_counts):
        if not new_positions:
            return False

        at = int(new_positions[0])
        if self.is_colour_group_owned(at, player_id, ignore_mortgaged=False):
            color_group = self.boxes[at].members_of_monopoly + [at]
            existing_vals = {}
            # pdb.set_trace()
            for each in color_group:
                existing_vals[each] = abs(self.boxes[each].state)-1

            for i,each in enumerate(new_positions):
                existing_vals[each] += new_counts[i]
            a = []
            for each in existing_vals.keys():
                a += [existing_vals[each]]
            a.sort()
            a = list(set(a))
            for each in a:
                if each > 5:
                    print("cannot build more than 5 houses")
                    return False
            if len(a) <= 2:
                if len(a)==2:
                    if max(a)-min(a)==1:
                        return True
                    else:
                        return False
                else:
                    return True
        return False

    def is_player_eligible_to_sell_houses_at_color_group(self, player_id, new_positions, new_counts):
        if not new_positions:
            return False

        at = int(new_positions[0])
        if self.is_colour_group_owned(at, player_id):
            color_group = self.boxes[at].members_of_monopoly + [at]
            existing_vals = {}
            for each in color_group:
                existing_vals[each] = abs(self.boxes[each].state)-1
                if existing_vals[each] == 6:
                    existing_vals[each] = 0
            for i,each in enumerate(new_positions):
                existing_vals[each] -= new_counts[i]
            a = []
            for each in existing_vals.keys():
                a += [existing_vals[each]]
            a.sort()
            a = list(set(a))
            for each in a:
                if each < 0 or each>5:
                    print("cannot sell more than houses than present number of houses")
                    return False
            if len(a) <= 2:
                if len(a)==2:
                    if max(a)-min(a)==1:
                        return True
                    else:
                        return False
                else:
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


    def is_colour_group_owned(self, box_pos, player_id, ignore_mortgaged = True):
        all_boxes = [box_pos] + self.boxes[box_pos].members_of_monopoly
        for each in all_boxes:
            if not self.boxes[each].is_owned_by(player_id, ignore_mortgaged=ignore_mortgaged):
                return False
        return True

