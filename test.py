d = {
        "color": None,
        "display_name": None,
        "buy_cost": None,
        "mortgage_val": None,
        "no_house_rent": None,
        "buy_house_cost": None,
        "rent_with_one_house": None,
        "rent_with_two_house": None,
        "rent_with_three_house": None,
        "rent_with_four_house": None,
        "rent_with_hotel": None,
        "buy_hotel_cost": None,
        "special": None
    }

from copy import deepcopy
import json

names = ["START", "P1", "COMMUNITY CHEST", "P2", "INCOME TAX", "TRAIN", "B1", "CHANCE", "B2", "B3", "JAIL", "PK1",
         "BULB", "PK2", "PK3", "TRAIN", "OR1", "COMMUNITY CHEST", "OR2", "OR3", "FREE PARKING", "R1", "CHANCE", "R2", "R3", "TRAIN", "Y1", "Y2",
         "TAP", "Y3", "GO TO JAIL", "G1", "G2", "COMMUNITY CHEST", "G3", "TRAIN", "CHANCE", "V1", "LUXURY TAX", "V2"]
tp = [1,0,1,0,1,1,0,1,0,0,1,0,1,0,0,1,0,1,0,0,1,0,1,0,0,1,0,0,1,0,1,0,0,1,0,1,1,0,1,0]
tp[5] = 2
tp[12] = 2
tp[15] = 2
tp[25] = 2
tp[28] = 2
tp[35] = 2
blue = "blue"
pink = "pink"
orange = "orange"
red ="red"
yellow = "yellow"
green = "green"
violet = "violet"
none = None
colors = [None, "purple", None, "purple", None, None, "blue", None, "blue", blue, none, pink, none, pink, pink, none, orange, none, orange, orange, none, red, none, red, red, none, yellow, yellow, none, yellow, none, green, green, none, green, none, none, violet, none, violet]

import random
ans = {}
for i, each in enumerate(names):
    ans[i] = deepcopy(d)
    if tp[i]==0:
        p = random.randint(10,30)*10
        ans[i]["color"] = colors[i]
        ans[i]["display_name"] = names[i] + " (%s)"%(i,)
        ans[i]["buy_cost"] = p
        ans[i]["mortgage_val"] = p/2
        ans[i]["no_house_rent"] = random.randint(5, 10)*10+(p/100)*10
        ans[i]["buy_house_cost"] = random.randint(15, 20)*10+ (p/100)*20
        ans[i]["rent_with_one_house"] = random.randint(7, 10)*10+ans[i]["no_house_rent"]
        ans[i]["rent_with_two_house"] = random.randint(7, 10) * 10 + ans[i]["rent_with_one_house"]
        ans[i]["rent_with_three_house"] = random.randint(7, 10) * 10 + ans[i]["rent_with_two_house"]
        ans[i]["rent_with_four_house"] = random.randint(7, 10) * 10 + ans[i]["rent_with_three_house"]
        ans[i]["rent_with_hotel"] = random.randint(8, 10) * 10 + ans[i]["rent_with_four_house"]
        ans[i]["buy_hotel_cost"] = ans[i]["buy_house_cost"] + random.randint(15, 20)*10
    elif tp[i]==2:
        ans[i]["color"] = colors[i]
        ans[i]["display_name"] = names[i] + " (%s)" % (i,)
        ans[i]["special"] = None
        p = random.randint(10, 30) * 10
        ans[i]["buy_cost"] = p
        ans[i]["mortgage_val"] = p / 2
        ans[i]["no_house_rent"] = random.randint(5, 10) * 10 + (p / 100) * 10
    else:
        ans[i]["special"] = names[i]
        ans[i]["display_name"] = names[i]
f = open("each_box_data.json", "w")
f.write(json.dumps(ans, indent=4))
f.close()

