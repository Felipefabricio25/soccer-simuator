import math
import random
import json
import operator
import functions, matches
from re import I
import pandas as pd

class Camp(object):
    def __init__(self):

        print("Starting!")

        # creating empty lists
        self.teams = []
        self.teams_group = []
        self.listofteams = []
        self.seed = []
        self.actual_bracket = []
        self.next_bracket = []
        self.groups = []
        self.seededjson = []
        self.seededjson_extra = []
        self.finalists_first = []
        self.finalists_second = []
        self.datajson = {}
        
        #variables to determine number of byes
        self.multwo = 0
        self.multj = 1 

        #variables to define the group stages
        self.grps = 0
        self.per_group = 0
        self.classified = 0

        # Number of turns in group stage
        self.t = 2

        #variable to determine if seeding is set or not
        seed_set = 0

        with open("Ranking_Libertadores.json", "r+") as fi:
            self.datajson = json.load(fi)

        with open("Groups_Libertadores_2023.json", "r+") as fi:
            self.grp_lib = json.load(fi)



        self.firststage = self.grp_lib["First Stage"]

        self.secondstage = self.grp_lib["Second Stage"]

        self.pot_surprise()


        self.pots = self.potone + self.pottwo + self.potthree + self.potfour
        self.countrylist = self.firststage + self.secondstage + self.pots

        for things in self.countrylist:
            if "bye" in things:
                self.countrylist.remove(things)

        for things in self.pots:
            if "bye" in things:
                self.pots.remove(things)

        zeroes = []

        for things in self.countrylist:
            zeroes.append(0)

        # number of elements as input
        self.n = len(self.countrylist)
        self.nn = self.n

        d = {'Countries': self.countrylist, 'Second Round': zeroes, 'Third Round': zeroes, 'Groups': zeroes, 'Ro16': zeroes, 
        'Quarterfinals':zeroes, 'Semifinals': zeroes, 'Finals': zeroes, 'Champion': zeroes}
        self.number_placements = pd.DataFrame(data=d)

        # iterating till the range
        for i in range(0, self.n):
            #country = input()
            country = self.countrylist[i]
        
            self.teams.append(country) # adding the element

    def pot_surprise(self):

        self.potone = list(self.grp_lib["Pot One"])

        self.pottwo = list(self.grp_lib["Pot Two"])

        self.potthree = list(self.grp_lib["Pot Three"])

        self.potfour = list(self.grp_lib["Pot Four"])


    #making the pre-libertadores stage happen

    def prelibertadores(self):
               
        self.pot_surprise()
        
        #first stage
        self.next_bracket, self.number_placements = matches.knock_onlyphase(
                self.firststage, self.next_bracket, self.datajson, self.number_placements)

        for teams in self.next_bracket:
            self.number_placements.loc[self.number_placements[f'Countries'] == f'{(teams)}','Second Round'] += 1

        print("----")

        #second stage
        for things in self.secondstage:
            if "bye" in things:

                x = int(things.split("bye")[1]) - 1
                self.secondstage[self.secondstage.index(things)] = self.next_bracket[x]

        self.next_bracket = []

        self.next_bracket, self.number_placements = matches.knock_onlyphase(
                self.secondstage, self.next_bracket, self.datajson, self.number_placements)

        for teams in self.next_bracket:
            self.number_placements.loc[self.number_placements[f'Countries'] == f'{(teams)}','Third Round'] += 1

        print("----")

        #third stage
        self.next_bracket, self.number_placements = matches.knock_onlyphase(
                self.next_bracket, self.next_bracket, self.datajson, self.number_placements)

        for teams in self.next_bracket:
            self.number_placements.loc[self.number_placements[f'Countries'] == f'{(teams)}','Groups'] += 1

        for teams in self.pots:
            self.number_placements.loc[self.number_placements[f'Countries'] == f'{(teams)}','Groups'] += 1

        print(self.next_bracket)

        for things in self.potfour:
            # print(things)
            if "bye" in things:

                x = (int(things.split("bye")[1])) * -1
                self.potfour[self.potfour.index(things)] = self.next_bracket[x]

        self.next_bracket = []

        print("----")



    #drawing the random groups

    def group_draw(self):

        one = list(self.potone)
        two = list(self.pottwo)
        three = list(self.potthree)
        four = list(self.potfour)
        
        self.teams = []

        for i in range(8):

            print(f"potone - {four}")

            ch1 = random.choice(one)
            self.teams.append(ch1)
            one.remove(ch1)

            ch2 = random.choice(two)
            self.teams.append(ch2)
            two.remove(ch2)

            ch3 = random.choice(three)
            self.teams.append(ch3)
            three.remove(ch3)

            ch4 = random.choice(four)
            self.teams.append(ch4)
            four.remove(ch4)



    #execute the group stage
    
    def groupstage_execute(self):
        variable = 0
        for i in range(self.grps):
            self.teams_group.append(self.teams[variable])
            self.teams_group.append(self.teams[variable+1])
            self.teams_group.append(self.teams[variable+2])
            self.teams_group.append(self.teams[variable+3])

            variable += 4

            # self.orderedBattles()
            champ1,champ2 = self.groups_init()

            self.number_placements.loc[self.number_placements[f'Countries'] == f'{(champ1)}','Ro16'] += 1
            self.number_placements.loc[self.number_placements[f'Countries'] == f'{(champ2)}','Ro16'] += 1

            self.finalists_first.append(champ1)
            self.finalists_second.append(champ2)

            self.teams_group = []



    #the knockout draw

    def ro16_draw(self):

        print(self.finalists_first)
        print(self.finalists_second)

        self.knockstage = []

        for i in range(8):

            ch1 = random.choice(self.finalists_first)
            self.knockstage.append(ch1)
            self.finalists_first.remove(ch1)

            ch2 = random.choice(self.finalists_second)
            self.knockstage.append(ch2)
            self.finalists_second.remove(ch2)

    def knock_init(self):

        #control variables
        self.score = 0
        self.round = 0

        self.knock_2n()
        self.knock_callMatches()

    def knock_2n(self):

        self.n = len(self.knockstage)

        multn = 0

        while multn != 1:
            if self.n <= math.pow(2,self.multwo):
                multn = 1
            else:
                self.multwo += 1

    def knock_callMatches(self):

        while len(self.knockstage) != 1:
            self.next_bracket = []

            self.next_bracket, self.number_placements = matches.knock_round_of(
                self.multwo, self.knockstage, self.next_bracket, self.datajson, self.round, self.number_placements)

            print(self.next_bracket)
            print("---")
            self.round+= 1
            self.knockstage = self.next_bracket

        print(f"The champion is {self.knockstage[0]}!")

    #groupstage

    def groups_init(self):

        totalgroups = {}
        finalstand = []

        totalgroups = functions.groups_draws(self.teams_group, self.nn)
        totalgroups = matches.groups_matches(self.datajson, self.t, self.nn, self.teams_group, totalgroups)

        finalresults = totalgroups.sort_values(by=['Points', 'Victories', 'Goals'], ascending=False)
        finalresults = finalresults.reset_index(drop=True)
        

        print(finalresults)

        classified = 2

        for j in range(0, classified):

            finalstand.append(finalresults['Countries'][j])

        print(finalstand)

        return finalstand[0], finalstand[1]
    
        #self.groups_toknock()



    def wc_percent_results(self):

        print("Results:")
        self.number_placements = self.number_placements.sort_values(by=['Champion', 'Finals', 'Semifinals', 'Quarterfinals'], ascending=False)
        print(self.number_placements)

    def libertadores_init(self):

        self.grps = 8

        for i in range(40232):
            self.prelibertadores()
            self.group_draw()
            self.groupstage_execute()
            self.ro16_draw()
            self.knock_init()
            
            self.next_bracket = []
            self.finalists_first = []
            self.finalists_second = []
            self.teams_group = []



        self.wc_percent_results()



champ = Camp()

champ.libertadores_init()