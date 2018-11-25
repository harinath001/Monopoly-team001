from GameState import Dice
import random
import pdb

class GameEngine(object):
    def __init__(self, game_state, player1, player2, bank, dice=None):
        self.game_state = game_state
        self.p1 = player1
        self.p2 = player2
        self.bank = bank
        self.dice = dice if dice is not None else Dice()

    def is_start_crossed(self, old_pos, new_pos):
        new_pos = new_pos%40
        if old_pos>new_pos:
            return True
        return False

    def get_players(self):
        return (self.p1, self.p2) if self.game_state.turn_number%2 == 0 else (self.p2, self.p1)

    def run(self):
        self.print_state()
        while True:
            curr, other = self.get_players()
            self.bmst()
            if curr.is_in_jail():
                self.jail_run()
            else:
                self.dice_roll()
                if self.game_state.double_count == 3:
                    print("3 times double detected !!")
                    self.double_run_penalty_run()
                else:
                    self.steps()
                self.decide_players_chance()
            print("player 0 money is ", self.p1.cash)
            print("player 1 money is ", self.p2.cash)
            print("one round is done PRESS ENTER to continue")
            self.print_state()
            raw_input()

    def steps(self):
        self.move_the_player()
        self.square_effect()
        self.bmst()

    def double_run_penalty_run(self):
        print("the player is moved to jail because of double run penalty")
        curr, other = self.get_players()
        curr.move_to_jail()

    def jail_run(self):
        curr, other = self.get_players()
        jail_decision = curr.agent.jailDecision(self.game_state.convert_to_state("jail", curr))
        # pdb.set_trace()
        final_decision = None
        card = None
        if str(jail_decision[0]).lower() == "r":
            final_decision = "r"
        elif str(jail_decision[0]).lower() == "p":
            final_decision = "p"
        elif str(jail_decision[0]).lower() == "c":
            final_decision = "c"
            try:
                card = int(jail_decision[1])
                if self.game_state.jail_cards[card-40] == curr.id:
                    final_decision = "c"
                else:
                    print(" Player do not own the jail card he is trying to use, so choosing the default move as R")
                    final_decision = "r"
            except Exception as ex:
                print("Player gave wrong decision in jail decision so choosing default move as R")
                final_decision = "r"
        else:
            final_decision = "r"
        skip_jail_double = False
        if final_decision == "c":
            print("Player successfully used the jail card ", card)
            card = int(jail_decision[1])
            self.game_state.jail_cards[card - 40] = -1
            curr.move_out_of_jail()
            self.dice_roll()
            self.steps()
        elif final_decision == "p":
            self.make_player_to_pay_money(curr, 50, " getting out of jail ", pay_to=0)
            curr.move_out_of_jail()
            self.dice_roll()
            self.steps()
        elif final_decision == "r":
            # handle jail card here
            curr.jail_turn_count += 1
            self.dice_roll()
            if self.game_state.dice_values[0] == self.game_state.dice_values[1]:
                print("the player got double so move out of jail !!")
                skip_jail_double = True
                curr.move_out_of_jail()
                self.steps()
            elif curr.jail_turn_count>=3:
                print("The player didnt get double...but this is third time..so now he has to pay 50 and move ahead")
                self.make_player_to_pay_money(curr, 50, "come out of jail after 3 unsuccessful turns", pay_to=0)
                curr.move_out_of_jail()
                self.steps()
            else:
                print("the player had to roll the dice and didnt get the double..so wait for next chance")
        self.decide_players_chance(skip_jail_double=skip_jail_double)


    # -------- states begin
    def decide_players_chance(self, skip_jail_double=False):
        if self.game_state.dice_values[0]==self.game_state.dice_values[1] and not skip_jail_double:
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
        if curr_box.is_special() and not curr_box.is_utility():
            print("current box is special box")
            if curr_box.is_tax_box():
                self.income_tax_state()
            if curr_box.is_chance():
                self.chance_state()
            elif curr_box.is_community_chest():
                self.community_chest_state()
            elif curr_box.display_name=="GO TO JAIL":
                curr.move_to_jail()
                # self.jail_state()
            elif curr_box.is_jail():
                print("the player is in jail for visiting state")
        else:
            # buying unowned property
            if curr_box.state==0:
                print("the current box is unowned by any one so the user can buy")
                self.bmst()
                self.buy_state(buy_not_happened_trigger=self.auction_state)
                #self.auction_state()
            # landed on already existing
            elif abs(curr_box.state)<7:
                if (curr.id==0 and curr_box.state>0) or (curr.id>0 and curr_box.state<0):
                    # Landed in your own property
                    print("the player landed in his own property..")
                    pass
                else:
                    print("the player landed in other players property..")
                    #rent_to_be_paid = curr_box.rent_to_be_paid()
                    rent_to_be_paid = self.game_state.get_rent_to_be_paid(other.id, curr_box.position)
                    self.make_player_to_pay_money(curr, rent_to_be_paid, " landed in "+curr_box.display_name, pay_to=other.id+1)
            else:
                print("the player landed in mortgaged property")

    def income_tax_state(self):
        print("this is income tax state...")
        curr, _ = self.get_players()
        curr_box = self.game_state.boxes[curr.get_position()]
        self.make_player_to_pay_money(curr, curr_box.tax, " paid tax because of tax box at "+str(curr.get_position()))

    def chance_state(self):
        curr, other = self.get_players()
        curr_box = self.game_state.boxes[curr.get_position()]
        print("this is the chance state")
        n = 16
        i = 4 #-1
        while i<1 or i>=n:
            # print("Enter the")
            i = random.randint(1, n)
            if self.game_state.jail_cards[1] != -1 and i==7:
                i = -1
        print("in chance the player got the card number ", i)
        if i == 1:
            # advance to go, collect 200
            print("advance to go, collect 200")
            curr.set_position(0)
            curr.add_cash(200)
            self.refresh_players_positions()
        elif i == 2:
            # advance to illinois avenue 24, if you pass go collet 200$
            print("advance to illinois avenue 24, if you pass go collect 200$")
            if self.is_start_crossed(curr.get_position(), 24):
                curr.add_cash(200)
            curr.set_position(24)
            self.refresh_players_positions()
            self.square_effect()

        elif i == 3:
            # advance to st.charles place, 11,  if you pass go collect 200$
            print("advance to st.charles place, 11,  if you pass go collect 200$")
            if self.is_start_crossed(curr.get_position(), 11):
                curr.add_cash(200)
            curr.set_position(11)
            self.refresh_players_positions()
            self.square_effect()

        elif i == 4:
            # advance token to nearest utility, if unowned u can buy, otherwise throw dice and pay 10 times the amount thrown of dice
            nearest_utility = curr_box.nearest_utility
            curr.set_position(nearest_utility)
            if self.game_state.boxes[nearest_utility].state == 0:
                self.refresh_players_positions()
                def pay_penalty():
                    p = sum(self.dice.roll())*10
                    self.make_player_to_pay_money(curr, p, "after community chest 4, the player didnt buy ", pay_to=0)
                self.buy_state(buy_not_happened_trigger=pay_penalty)
            else:
                self.square_effect()
        elif i == 5:
            # advance token to nearest rail road, if unowned u can buy, else pay double the normal rent
            nearest_railroad = curr_box.nearest_nearest_railroad
            curr.set_position(nearest_railroad)
            if self.game_state.boxes[nearest_railroad].state == 0:
                self.refresh_players_positions()
                def pay_penalty():
                    p = self.game_state.boxes[nearest_railroad].no_house_rent*2
                    self.make_player_to_pay_money(curr, p, "after community chest 5, the player didnt buy ", pay_to=0)
                self.buy_state(buy_not_happened_trigger=pay_penalty)
            else:
                self.square_effect()

        # elif i == 6:
        #     # advance token to nearest rail road, if unowned u can buy, else pay double the normal rent
        #     pass
        elif i == 6:
            # bank pays you 50$
            print("bank pays you 50$")
            curr.add_cash(50)
        elif i == 7:
            # get out of jail free
            print("get out of jail free")
            if self.game_state.jail_cards[1] == -1:
                self.game_state.jail_cards[1] = curr.id
            else:
                print("the card is taken already..so cannot allot this jail card again to the user.......")
                raise NotImplementedError("wrong card...")
        elif i == 8:
            # get back three spaces
            new_pos = (curr.get_position()-3)%40
            curr.set_position(new_pos)
            self.refresh_players_positions()
            self.square_effect()
        elif i == 9:
            # go to jail directly, dont collect 200$
            print("go to jail directly, dont collect 200$")
            curr.move_to_jail()
            self.refresh_players_positions()
        elif i == 10:
            # make general repairs, for each house pay 25, for hotel 100
            print("make general repairs, for each house pay 25, for hotel 100")
            houses_count = self.game_state.get_all_houses_boxes_indexes(curr.id)
            hotels_count = self.game_state.get_all_hotels_boxes_indexes(curr.id)
            self.make_player_to_pay_money(curr, 25*houses_count+100*hotels_count, " chance 10 ", pay_to=0)
        elif i == 11:
            # pay poor tax 15
            print("pay poor tax 15")
            self.make_player_to_pay_money(curr, 15, " chance 11 ", pay_to=0)
        elif i == 12:
            # take a trip to reading rail road, if you pass go collect 200
            print("take a trip to reading rail road, if you pass go collect 200")
            if self.is_start_crossed(curr.get_position(), 5):
                curr.add_cash(200)
            curr.set_position(5)
            self.refresh_players_positions()
            self.square_effect()
        elif i == 13:
            # advance token to boardwalk, 39
            print("advance token to boardwalk, 39")
            curr.set_position(39)
            self.refresh_players_positions()
            self.square_effect()
        elif i == 14:
            # You have been elected Chairman of the Board. Pay each player $50
            print("You have been elected Chairman of the Board. Pay each player $50")
            self.make_player_to_pay_money(curr, 50, " chance 14 ", pay_to=other.id+1)
        elif i == 15:
            # receive 150
            print("receive 150 from bank")
            curr.add_cash(150)
        elif i == 16:
            # collect 100, won crossword
            print("collect 100, won crossword")
            curr.add_cash(100)

    def community_chest_state(self):
        curr, other = self.get_players()
        print("this is community chest state")
        # total there are 17 cards
        n = 17
        i = -1
        while i<1 or i>=n:
            # print("Enter the")
            i = random.randint(1, n)
            if self.game_state.jail_cards[0] != -1 and i==5:
                i = -1
        print("in community chest the player got ", i)
        if i == 1:
            curr.set_position(0)
            self.refresh_players_positions()
        elif i==2:
            curr.add_cash(200)
        elif i==3:
            self.make_player_to_pay_money(curr, 50, " doctors fee (community chest 3)", pay_to=0)
        elif i==4:
            curr.add_cash(50)
        elif i==5:
            # get out of jail card
            print("get out of jail free...community chest 5")
            if self.game_state.jail_cards[0] == -1:
                self.game_state.jail_cards[0] = curr.id
            else:
                print("the card is taken already..so cannot allot this jail card again to the user.......")
                raise NotImplementedError("wrong card...")
        elif i==6:
            print("move the player to jail...community chest 6")
            curr.move_to_jail()
            # self.move_the_player(reward=False)
        elif i==7:
            curr.add_cash(50)
            self.make_player_to_pay_money(other, 50, "GRAND OPERA NIGHT (community chest 7 by other player)", pay_to=curr.id+1)
        if i == 8:
            print("community chest 8, adding 100")
            curr.add_cash(100)
        elif i==9:
            print("community chest 9, adding 20")
            curr.add_cash(20)
        # elif i==10:
        #     self.make_player_to_pay_money(other, 10, " other players birthday (chance 10 by other player)", curr.id+1)
        #     curr.add_cash(10)
        elif i==10:
            print("community chest 10, adding 100")
            curr.add_cash(100)
        elif i==11:
            print("community chest 11, adding pay 50 as hospital fee")
            self.make_player_to_pay_money(curr, 50, " hospital fee (community chest 12)", pay_to=0)
        elif i==12:
            print("community chest 12, deducting 50 for school fee")
            self.make_player_to_pay_money(curr, 50, "school fee (community chest 13)", pay_to=0)
        elif i==13:
            print("community chest 13, adding 25")
            curr.add_cash(25)
        elif i==14:
            # pay 40 per house and 115 per hotel
            print("community chest 14, pay 40 per house and 115 per hotel")
            money = len(self.game_state.get_all_houses_boxes_indexes(curr.id))*40 + len(self.game_state.get_all_hotels_boxes_indexes(curr.id))*115
            self.make_player_to_pay_money(curr, money, " community chest 14 ", pay_to=0)
        elif i==15:
            print(" added money to ", curr.id, " because of community chest 15")
            curr.add_cash(10)
        elif i==16:
            print(" added money to ", curr.id, " because of community chest 16")
            curr.add_cash(100)

    def move_the_player(self, reward=True):
        curr, _ = self.get_players()
        if self.game_state.double_count==3:
            print("3 times double count detected ")
            # jail_index = self.game_state.give_jail_box_index()
            # print("the index of jail box is ", jail_index)
            # curr.set_position(jail_index)
            curr.move_to_jail()
            self.game_state.double_count = 0
        else:
            prev = curr.get_position()
            curr.move_position(self.game_state.dice_values[0] + self.game_state.dice_values[1])
            if prev>curr.get_position() and reward:
                print("the player crossed START. So rewarding him with 200 $")
                curr.add_cash(200)
        print("PLAYER ", curr.id, " has been moved to box index ", curr.get_position())
        # if curr.id == self.p1.id:
        #     self.game_state.players_positions = [curr.get_position(), self.game_state.players_positions[1]]
        # else:
        #     self.game_state.players_positions = [self.game_state.players_positions[0], curr.get_position()]
        self.refresh_players_positions()

    def refresh_players_positions(self):
        curr, _ = self.get_players()
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
        if self.game_state.dice_values[0] == self.game_state.dice_values[1]:
            self.game_state.double_count += 1
        else:
            self.game_state.double_count = 0
        curr, _ = self.get_players()
        curr.agent.receiveState(self.game_state.convert_to_state("dice", curr))

    def bmst(self):
        # self.bank.houses_in_use = 0
        # self.bank.hotels_in_use = 2
        # td = {"cash_offer": 0, "properties_for_offer": [40],
        #      "cash_requesting": 200,
        #      "properties_requesting": [1,3]
        #      }
        # self.game_state.jail_cards[0] = 1
        # self.game_state.boxes[1].state = 2
        # self.game_state.boxes[3].state = 7
        # self.game_state.boxes[6].state = -1
        # self.trade_state(self.p2, td)
        # # self.sell_house(self.p1, [(1, 2), (3, 1)])
        # self.print_state()
        # print("----")
        # print(self.bank.houses_in_use)
        # print(self.bank.hotels_in_use)
        # raw_input()
        flag = True
        while flag:
            flag = False
            for each_player in self.get_players():
                action = each_player.agent.getBMSTDecision(self.game_state.convert_to_state("bmst", each_player))
                if action[0] == "B":
                    flag = True
                    self.build_house(each_player, action[1])
                    # for each_buy in action[1]:
                    #     for i in range(0, each_buy[1]):
                    #         self.build_house(each_player, each_buy[0])
                elif action[0] == "M":
                    flag = True
                    self.mortgage_state(each_player, action[1])
                    # for each_pos in action[1]:
                    #     self.mortgage_state(each_player, each_pos)
                elif action[0] == "S":
                    flag = True
                    self.sell_house(each_player, action[1])
                    # for each_sell in action[1]:
                    #     for i in range(0, each_sell[1]):
                    #         self.sell_house(each_player, each_sell[0])
                elif action[0] == "T":
                    d = {"cash_offer": int(action[1]), "properties_for_offer": [int(x) for x in action[2]],
                         "cash_requesting": int(action[3]),
                         "properties_requesting": [int(x) for x in action[4]]
                         }
                    self.trade_state(each_player, d)

    def trade_state(self, player, trade_dict):
        if len([x for x in trade_dict["properties_for_offer"]+trade_dict["properties_requesting"] if x<0 or x>41 or (x<40 and abs(self.game_state.boxes[x].state)!=1 and abs(self.game_state.boxes[x].state)!=7)]) > 0:
            print("Invalid properties given in trade state")
            return
        other_player = self.p1 if self.p2.id == player.id else self.p2
        if all(self.game_state.boxes[x].is_owned_by(player.id) for x in trade_dict["properties_for_offer"]):
            if all([self.game_state.boxes[x].is_owned_by(other_player.id) for x in trade_dict["properties_requesting"]]):
                first_player_mortgaged = []
                first_player_unmortgaged = []
                first_player_jail_cards = []
                for each in trade_dict["properties_for_offer"]:
                    if each<40:
                        if abs(self.game_state.boxes[each].state) <7:
                            first_player_unmortgaged += [each]
                        else:
                            first_player_mortgaged += [each]
                    elif each<42:
                        first_player_jail_cards += [each]

                second_player_mortgaged = []
                second_player_unmortgaged = []
                second_player_jail_cards = []
                for each in trade_dict["properties_requesting"]:
                    if each < 40:
                        if abs(self.game_state.boxes[each].state) < 7:
                            second_player_unmortgaged += [each]
                        else:
                            second_player_mortgaged += [each]
                    elif each < 42:
                        second_player_jail_cards += [each]
                res = other_player.agent.respondTrade(self.game_state.convert_to_state("bmst", other_player, **trade_dict))
                if res is True:
                    if (player.cash+trade_dict["cash_requesting"])>=trade_dict["cash_offer"] and (other_player.cash+trade_dict["cash_offer"])>=trade_dict["cash_requesting"]:
                        for each in first_player_jail_cards:
                            self.game_state.boxes[each].make_owner(other_player.id)
                        for each in first_player_mortgaged:
                            self.game_state.boxes[each].state = 7 if other_player.id==0 else -7
                        for each in first_player_unmortgaged:
                            self.game_state.boxes[each].state = 1 if other_player.id==0 else -1

                        for each in second_player_jail_cards:
                            self.game_state.boxes[each].make_owner(player.id)
                        for each in second_player_mortgaged:
                            self.game_state.boxes[each].state = 7 if player.id==0 else -7
                        for each in second_player_unmortgaged:
                            self.game_state.boxes[each].state = 1 if player.id==0 else -1
                        player.cash = player.cash+abs(trade_dict["cash_requesting"])- abs(trade_dict["cash_offer"])
                        other_player.cash = other_player.cash + abs(trade_dict["cash_offer"]) - abs(trade_dict["cash_requesting"])
                    else:
                        print("Trade cannot be done as the players have inconsistent cash..")
                else:
                    print("The other player declined the trade offer")
            else:
                print("Properties the player are requesting are not owned by other player")
        else:
            print("Properties the player are trying to trade are owned by the player")



        # boxes with properties are not tradable

    def mortgage_state(self, player, props):
        # box = self.game_state.boxes[box_index]
        # if not box.is_owned_by(player.id):
        #     print("This box is not owned by the player..so he cannot unmortgage/mortgage it")
        #     return
        # if abs(box.state) != 7:
        #     self.mortgage(player, box_index)
        # else:
        #     self.unmortgage(player, box_index)
        if all([self.game_state.boxes[x].is_owned_by(player.id) for x in props]):
            for each in props:
                box = self.game_state.boxes[each]
                if abs(box.state) != 7:
                    self.mortgage(player, each)
                else:
                    self.unmortgage(player, each)
        else:
            print("Some properties here are not owned by you..so cannot mortgage them")

    def buy_state(self, buy_not_happened_trigger=None):
        print("***** BUY STATE *****")
        curr, other = self.get_players()
        current_pos = self.game_state.players_positions[curr.id]
        current_box = self.game_state.boxes[current_pos]
        if current_box.is_buyable() and current_box.state==0:
            # if the given box is not special, then allow the user to buy the box
            if curr.agent.buyProperty(self.game_state.convert_to_state("buy", curr)):
                print("PLAYER ", curr.id, " is interested to buy the current box")
                # user is interested to buy the current box
                self.make_player_to_pay_money(curr, current_box.buy_cost, " buying the property "+current_box.display_name, pay_to=0)
                current_box.state = 1 if curr.id == self.p1.id else -1
            else:
                if buy_not_happened_trigger:
                    buy_not_happened_trigger()

        else:
            print("No one can buy this box because it is not in buyable state..")

    def auction_state(self):
        print("***** AUCTION STATE *****")
        curr, other = self.get_players()
        current_pos = self.game_state.players_positions[curr.id]
        current_box = self.game_state.boxes[current_pos]
        if current_box.state==0:
            p1_value = curr.agent.auctionProperty(self.game_state.convert_to_state("auction", curr))
            p2_value = other.agent.auctionProperty(self.game_state.convert_to_state("auction", other))
            try:
                p1_value = int(p1_value)
            except Exception as ex:
                p1_value = 0
            try:
                p2_value = int(p2_value)
            except Exception as ex:
                p2_value = 0
            if p1_value > p2_value and (p1_value or p2_value):
                self.make_player_to_pay_money(curr, p1_value, "buying auctioned property  "+current_box.display_name)
                current_box.state = 1 if curr.id == self.p1.id else -1
            elif p2_value >= p1_value and (p1_value or p2_value):
                self.make_player_to_pay_money(other, p2_value, "buying auctioned property  "+current_box.display_name)
                current_box.state = 1 if other.id == self.p1.id else -1
            else:
                print("BOTH THE PLAYERS RESPONDED WRONGLY....so unable to auction this property")
        else:
            print("UNABLE TO AUCTION THIS PROPERTY, BECAUSE THE PROPERTY IS NOT IN BUYABLE STATE")

    def build_house(self, player, new_builds):

        # box = self.game_state.boxes[box_pos]
        # if abs(box.state) >=1 and abs(box.state)<5 and self.game_state.is_player_eligible_to_build_house_at_box(player.id, box_pos):
        #     self.make_player_to_pay_money(player, box.buy_house_cost, "to build house at "+str(box.position), pay_to=0)
        #     box.state = box.state + (1 if box.state>0 else -1)
        # else:
        #     print("UNABLE TO BUILD THE HOUSE, current state is ", box.state)
        for each in new_builds:
            if not self.game_state.boxes[each[0]].is_normal():
                print("some of the boxes are not normal boxes to build houses..unable to build houses..")
                return
        new_builds.sort()
        groups = [[new_builds[0]]]
        for each in new_builds[1:]:
            flag = 1
            for each_member in self.game_state.boxes[each[0]].members_of_monopoly+[each[0]]:
                if each_member in [x[0] for x in groups[-1]]:
                    groups[-1] += [each]
                    flag = 0
                    break
            if flag==1:
                groups += [[each]]
        for group in groups:
            if not self.game_state.is_player_eligible_to_build_houses_at_color_group(player.id, [x[0] for x in group], [abs(x[1]) for x in group]):
                print(group, " is not eligible for building houses, because wrong configuration given")
                return
        # now its proved that the user gave correct configuration
        # check for number of houses available or not
        houses = 0
        hotels = 0
        total_money_required = 0
        for each in new_builds:
            each = (abs(each[0]), abs(each[1]))
            if each[1]+(abs(self.game_state.boxes[each[0]].state)-1)==5:
                existing_houses = abs(self.game_state.boxes[each[0]].state)-1
                hotels += 1
                houses -= existing_houses
                total_money_required += (4-existing_houses)*self.game_state.boxes[each[0]].buy_house_cost + self.game_state.boxes[each[0]].buy_hotel_cost
            else:
                houses += each[1]
                total_money_required += each[1]*self.game_state.boxes[each[0]].buy_house_cost

        if (houses+self.bank.houses_in_use) <= self.bank.total_houses and (hotels+self.bank.hotels_in_use)<=self.bank.total_hotels:
            self.bank.houses_in_use = houses + self.bank.houses_in_use
            self.bank.hotels_in_use = hotels + self.bank.hotels_in_use
            if player.remove_cash(total_money_required):
                for each in new_builds:
                    self.game_state.boxes[each[0]].state += each[1]
                print("Buy success..")
            else:
                print("The player do not have enough money to buy the houses/hotels")
        else:
            print("houses or hotels not available as of now...wait till someone sell them")


    def sell_house(self, player, new_builds):
        # if self.game_state.is_player_eligible_to_sell_house_at_box(player.id, box_pos):
        #     box = self.game_state.boxes[box_pos]
        #     # when the player sell the house, he will get money half of the money he bought the house
        #     print("for selling the house the player will be awarded half of the amount of house")
        #     player.add_cash(box.buy_house_cost/2)
        #     box.state = box.state - (1 if box.state>0 else -1)
        for each in new_builds:
            if not self.game_state.boxes[each[0]].is_normal():
                print("some of the boxes are not normal boxes to build houses..unable to build houses..")
                return
        new_builds.sort()
        groups = [[new_builds[0]]]
        for each in new_builds[1:]:
            flag = 1
            for each_member in self.game_state.boxes[each[0]].members_of_monopoly+[each[0]]:
                if each_member in [x[0] for x in groups[-1]]:
                    groups[-1] += [each]
                    flag = 0
                    break
            if flag==1:
                groups += [[each]]
        for group in groups:
            if not self.game_state.is_player_eligible_to_sell_houses_at_color_group(player.id, [x[0] for x in group], [abs(x[1]) for x in group]):
                print(group, " is not eligible for selling houses, because wrong configuration given")
                return
        houses = 0
        hotels = 0
        total_money_gained = 0

        for each in new_builds:
            hotel_sell_value = self.game_state.boxes[each[0]].sell_house_cost
            house_sell_value = self.game_state.boxes[each[0]].sell_hotel_cost
            each = (abs(each[0]), abs(each[1]))
            existing_houses = abs(self.game_state.boxes[each[0]].state) - 1
            if existing_houses == 5:
                hotels -= 1
                houses += 5 - each[1]
                total_money_gained += (each[1]-1)*house_sell_value + hotel_sell_value
            else:
                houses -= each[1]
                total_money_gained += each[1]*house_sell_value

        if (houses+self.bank.houses_in_use) <= self.bank.total_houses and (hotels+self.bank.hotels_in_use) <= self.bank.total_hotels:
            self.bank.houses_in_use = houses + self.bank.houses_in_use
            self.bank.hotels_in_use = hotels + self.bank.hotels_in_use
            print("Sell success..")
            player.add_cash(total_money_gained)
        else:
            print("houses or hotels not available as of now...wait till someone sell them")



    def mortgage(self, player, box_pos):
        box = self.game_state.boxes[box_pos]
        if box.is_owned_by(player.id):
            if not abs(box.state)==1:
                print("The property is not in mortagagable state. Remove the houses")
                return
            player.add_cash(box.mortgage_val)
            self.game_state.revoke_a_property_from_player(player.id, box_pos)
            # box.state = 7 if player.id==self.p1.id else -7
        else:
            print("The player is not the owner...he cannot mortgage it")

    def unmortgage(self, player, pos):
        box = self.game_state.boxes[pos]
        if not box.is_owned_by(player.id):
            print("the player is not owner of property..so unable to unmortgage it")
            return
        if abs(box.state) == 7:
            unmortgage_val = box.unmortgage_val
            self.make_player_to_pay_money(player, unmortgage_val, "unmortgae of "+str(box.display_name), pay_to=0)
            self.game_state.assign_a_property_to_player(player.id, pos)

    def make_player_to_pay_money(self, player, money, purpose, pay_to=0):
        rent_to_be_paid = money
        x, y = self.game_state.rent_to_be_paid
        x_to, y_to = self.game_state.rent_paid_to
        if player.id == self.p1.id:
            self.game_state.rent_to_be_paid = [rent_to_be_paid, y]
            self.game_state.rent_paid_to = [pay_to, y_to]
        else:
            self.game_state.rent_to_be_paid = [x, rent_to_be_paid]
            self.game_state.rent_paid_to = [x_to, pay_to]
        print("player ", player.id, " currently have ", player.cash, " before deduction")
        print("player ", player.id, " have to pay ", money)
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
        if player.id == self.p1.id:
            self.game_state.rent_to_be_paid = [0, y]
            self.game_state.rent_paid_to[0] = None
        else:
            self.game_state.rent_to_be_paid = [x, 0]
            self.game_state.rent_to_be_paid[1] = None
        print("player ", player.id, " currently have ", player.cash, " after deduction")


    def print_state(self):
        f = open("output.txt", "w")
        f.write("******* Players output ********\n")
        gap = "".join(["\t"]*6)
        f.write("Player 1\n")
        f.write("Cash:       %s\n"%(self.p1.cash))
        f.write("Position:   %s\n"%(self.p1.get_position()))
        f.write("Jail Cards: %s\n" % (",".join([str(40+i) for i,x in enumerate(self.game_state.jail_cards) if x==0]), ))
        f.write("ALL boxes:  %s\n" % (",".join([str(x) for x in self.game_state.get_all_owned_boxes(0)]), ))
        f.write("mort boxes: %s\n" % (",".join([str(x) for x in self.game_state.get_all_mortgaged_boxes(0)]),))
        f.write("ALL houses: %s\n" % (",".join([str(x) for x in self.game_state.get_all_houses_boxes_indexes(0)]),))
        f.write("ALL hotels: %s\n" % (",".join([str(x) for x in self.game_state.get_all_hotels_boxes_indexes(0)]),))
        f.write("\n"*3)
        f.write("Player 2\n")
        f.write("Cash:       %s\n" % (self.p2.cash))
        f.write("Position:   %s\n" % (self.p2.get_position()))
        f.write("Jail Cards: %s\n" % (",".join([str(40 + i) for i, x in enumerate(self.game_state.jail_cards) if x == 1]),))
        f.write("ALL boxes:  %s\n" % (",".join([str(x) for x in self.game_state.get_all_owned_boxes(1)]),))
        f.write("mort boxes: %s\n" % (",".join([str(x) for x in self.game_state.get_all_mortgaged_boxes(1)]),))
        f.write("ALL houses: %s\n" % (",".join([str(x) for x in self.game_state.get_all_houses_boxes_indexes(1)]),))
        f.write("ALL hotels: %s\n" % (",".join([str(x) for x in self.game_state.get_all_hotels_boxes_indexes(1)]),))
        f.close()