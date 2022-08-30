import math
import random
import json
import operator
from re import I

class Camp(object):
    def __init__(self):
        '''creating empty lists'''
        self.teams = [] #list to contain all the teams, ordered by when added
        self.teams_group = [] #list to contain all the teams, ordered by game order
        self.listofteams = [] #list to contain all the teams, ordered by seed

        self.actual_bracket = [] #list of the current teams being used in a group
        self.next_bracket = [] #list of teams that classified to a next stage

        self.seed = [] #initial base list to declare all seed levels present
        self.seededjson = [] #list with the seed levels from the FIFA ranking
        self.seededjson_extra = [] #a copy of this list above so I can work with both at the same time

        self.finalists = [] #list to append all the teams that are classified to knockout stage

        self.datajson = {} #reading of the world cup ranking json

        #dicts to save the amount of times each teams have passed to each of these rounds
        self.rosixteen = {}
        self.quarterfinals = {}
        self.semifinals = {}
        self.finals = {}
        self.champion = {}
        
        #variables to determine number of byes
        self.multwo = 0 #2^n number of participants
        self.multj = 1 

        #variables to define the group stages
        self.grps = 0
        self.per_group = 0
        self.classified = 0

        #variable to determine if seeding is set or not
        seed_set = 0

        #choose year the year you want to use for the bracket (2022, 2018)
        years = 2022

        #open the json
        with open("Ranking.json", "r+") as fi:
            self.datajson = json.load(fi)

        # number of countries being used
        self.n = 32
        self.nn = self.n

        #2022
        self.countrylist = ["Catar","Equador","Senegal","Holanda",
        "Inglaterra","Ira","Estados Unidos","Gales",
        "Argentina","Arabia Saudita","Mexico","Polonia",
        "Franca","Australia","Dinamarca","Tunisia",
        "Espanha","Costa Rica","Alemanha","Japao",
        "Belgica","Canada","Marrocos","Croacia",
        "Brasil","Servia","Suica","Camaroes",
        "Portugal","Gana","Uruguai","Coreia do Sul"]

        #2018
        # self.countrylist = ["Uruguai","Russia","Arabia Saudita","Egito",
        # "Espanha","Ira","Portugal","Marrocos",
        # "Franca","Dinamarca","Peru","Australia",
        # "Croacia","Argentina","Nigeria","Islandia",
        # "Brasil","Suica","Servia","Costa Rica",
        # "Suecia","Mexico","Coreia do Sul","Alemanha",
        # "Belgica","Inglaterra","Tunisia","Panama",
        # "Colombia","Japao","Senegal","Polonia"]

        # putting all the countries present in their right lists
        for i in range(0, self.n):
            country = self.countrylist[i]
        
            self.teams.append(country)
            self.teams_group.append(country)
            self.listofteams.append(country)

            self.rosixteen[country] = [0]
            self.rosixteen[country] = [0]
            self.quarterfinals[country] = [0]
            self.semifinals[country] = [0]
            self.finals[country] = [0]
            self.champion[country] = [0]

            self.seededjson.append(self.datajson[country][str(years)]["Seed"])
            self.seededjson_extra.append(self.datajson[country][str(years)]["Seed"])

        #sorting the ranking seed in the original list
        self.seededjson.sort()
        self.listofteams = []

        #sorting listofteams by seed order
        for things in self.seededjson:
            position = self.seededjson_extra.index(things)

            self.listofteams.append(self.countrylist[position])

        seed_set = 1

        '''How does the seeding work?
        It's always in groups of ten.
        Imagine you have 40 teams. Dividing that by 10, you have 10 groups of 4.
        If that's the case, each 4 groups will have a seed.
        The first 4 teams will be "seed 1", and they'll always be equal in power.
        The same will go subsequently for each group, until all teams will be seeded.
        So the first four are stronger than the second four, that are stronger than the third four...'''

        #applying that explained above
        if self.n >= 10:
            seed_value = 10 #numbers of groups of seeds
            sed = int(self.n/seed_value)

            #loop filling the seed list with [10, 10, 10, 10, 9...]
            for i in range(0,self.n):
                if seed_set == 1:
                    if i > sed:
                        seed_value -= 1
                        sed += int(self.n/seed_value)
                    self.seed.append(seed_value)
                if seed_set == 0:
                    self.seed.append(0)

        #optional case if there are less than ten teams: not used here
        else:
            sed = int(10/self.n)
            seed_value = 10

            for i in range (0,self.n):
                if seed_set == 1:
                    self.seed.append(seed_value)
                    seed_value -= sed
                if seed_set == 0:
                    self.seed.append(0)

    
    #Defining the orders each team face each other in the knockout stage
    def wcBattles(self):

        self.actual_bracket.append(self.teams[0])
        self.actual_bracket.append(self.teams[3])
        self.actual_bracket.append(self.teams[4])
        self.actual_bracket.append(self.teams[7])
        self.actual_bracket.append(self.teams[8])
        self.actual_bracket.append(self.teams[11])
        self.actual_bracket.append(self.teams[12])
        self.actual_bracket.append(self.teams[15])
        self.actual_bracket.append(self.teams[2])
        self.actual_bracket.append(self.teams[1])
        self.actual_bracket.append(self.teams[6])
        self.actual_bracket.append(self.teams[5])
        self.actual_bracket.append(self.teams[10])
        self.actual_bracket.append(self.teams[9])
        self.actual_bracket.append(self.teams[14])
        self.actual_bracket.append(self.teams[13])

    #Defining a seeded order for the battles
    def orderedBattles(self):
        self.actual_bracket = self.teams_group
        self.teams_group = []

    '''How does the result of a game is defined?
    The variable "times" is the one related to seeding.
    "times" indicates how much more seed the bigger team has.
    So if you have a team seed 5, and one seed 8, times will be equal to 3.

    For the game itself, a number will be randomized with the number of goals scored.
    This number has 30% chance of being zero, 25% one, 20% two, 15% three, 5% four,
    3% five, 1% six, 0.4% seven, 0.3% eight, 0.2% nine, 0.1% ten goals.
    This number will be rolled a number of times: the average of the two bigger ones will be the final amount.
    
    For the rolls, each team will roll a certain amount of times:
    Lower seed: 2 times
    Bigger seed: 2+"times" times
    This means that the bigger seed has a higher chance of getting bigger numbes, given it will roll more times.'''

    #Defining the result of a game
    def result(self, times=0):
        total = []

        if times < 0:
            times = 0

        #rolling the numbers
        for k in range(0, 2+times):
            value = random.uniform(0,1000)
            if value <= 300:
                total.append(0)
            if 300 < value and value <= 550:
                total.append(1)
            if 550 < value and value <= 750:
                total.append(2)
            if 750 < value and value <= 900:
                total.append(3)
            if 900 < value and value <= 950:
                total.append(4)
            if 950 < value and value <= 980:
                total.append(5)
            if 980 < value and value <= 990:
                total.append(6)
            if 990 < value and value <= 994:
                total.append(7)
            if 994 < value and value <= 997:
                total.append(8)
            if 997 < value and value <= 999:
                total.append(9)
            if 999 < value and value <= 1000:
                total.append(10)

        total.sort(reverse=True)

        #returning the final value of scored goals
        return int((total[0]+total[1])/(2))

    #Initialization of a knockout bracket
    def knock_init(self):

        #control variables
        self.score = 0
        self.round = 0
        self.current_bracket = [] #bracket with the current teams in this knockout phase

        #Determining 2^n number of participants
        self.knock_2n()
        #Adding byes in case the bracket doesn't have an exact 2^n number
        self.addByes()
        #matches
        self.knock_callMatches()

    def knock_2n(self):

        #determining 2^n number of participants
        multn = 0

        while multn != 1:
            if self.n <= math.pow(2,self.multwo):
                multn = 1
            else:
                self.multwo += 1

    def addByes(self):
        #use this only if actual_bracket is ready, with the use of randomBattles or orderedBattles

        if self.n == (pow(2,self.multwo)):
            pass 
        else:
            for j in range(0, (pow(2,self.multwo) - self.n)):
                self.actual_bracket.insert(self.multj,"bye" + str(j)) # adding the byes to second matches
                self.multj += 2

    #Execution of each round of a knockout bracket
    def knock_round_of(self):

        team1 = 0
        team2 = 1

        for l in range(0, int((pow(2,self.multwo-self.round)/2))):

            self.current_bracket.append(self.actual_bracket[int(team1)])
            self.current_bracket.append(self.actual_bracket[int(team2)])

            #if it's a bye just skip the match, if not, enter the ride
            if 'bye' in self.current_bracket[0]:
                self.next_bracket.append(self.current_bracket[1])
                print(f'{self.current_bracket[0]} 0 - 1 {self.current_bracket[1]}')
            elif 'bye' in self.current_bracket[1]:
                self.next_bracket.append(self.current_bracket[0])
                print(f'{self.current_bracket[0]} 1 - 0 {self.current_bracket[1]}')
            else:

                #determining the seeding of each team
                force1 = (self.seed[self.listofteams.index(self.current_bracket[0])] - self.seed[self.listofteams.index(self.current_bracket[1])])
                force2 = (self.seed[self.listofteams.index(self.current_bracket[1])] - self.seed[self.listofteams.index(self.current_bracket[0])])
                
                value1 = self.result(times=force1)
                value2 = self.result(times=force2)

                #What happens when each team wins:
                if value1 > value2:
                    if (pow(2,self.multwo-self.round)/2) == 8:
                        self.quarterfinals[(self.current_bracket[0])][0] += 1 
                    elif (pow(2,self.multwo-self.round)/2) == 4:
                        self.semifinals[(self.current_bracket[0])][0]  += 1
                    elif (pow(2,self.multwo-self.round)/2) == 2:
                        self.finals[(self.current_bracket[0])][0]  += 1
                    elif (pow(2,self.multwo-self.round)/2) == 1:
                        self.champion[(self.current_bracket[0])][0]  += 1

                    self.next_bracket.append(self.current_bracket[0])

                if value2 > value1:
                    if (pow(2,self.multwo-self.round)/2) == 8:
                        self.quarterfinals[(self.current_bracket[1])][0]  += 1 
                    elif (pow(2,self.multwo-self.round)/2) == 4:
                        self.semifinals[(self.current_bracket[1])][0]  += 1 
                    elif (pow(2,self.multwo-self.round)/2) == 2:
                        self.finals[(self.current_bracket[1])][0]  += 1 
                    elif (pow(2,self.multwo-self.round)/2) == 1:
                        self.champion[(self.current_bracket[1])][0]  += 1 

                    self.next_bracket.append(self.current_bracket[1])

                if value1 == value2:
                    past = random.choice(self.current_bracket)

                    if (pow(2,self.multwo-self.round)/2) == 8:
                        self.quarterfinals[(past)][0]  += 1 
                    elif (pow(2,self.multwo-self.round)/2) == 4:
                        self.semifinals[(past)][0]  += 1 
                    elif (pow(2,self.multwo-self.round)/2) == 2:
                        self.finals[(past)][0]  += 1 
                    elif (pow(2,self.multwo-self.round)/2) == 1:
                        self.champion[(past)][0]  += 1 

                    self.next_bracket.append(past)

            team1 += 2
            team2 += 2

            self.current_bracket = []

    #Loop for all the knockout phases
    def knock_callMatches(self):
        while len(self.actual_bracket) != 1:
            self.knock_round_of()

            print(self.next_bracket)
            print("---")
            self.round+= 1
            self.actual_bracket = self.next_bracket
            self.next_bracket = []

        print(f"The champion is {self.actual_bracket[0]}!")

    #Initializing the group stage
    def groups_init(self):
        self.totalgroups = {}
        self.finalstand = []
        
        # self.t = int(input("Enter number of turns: "))
        self.t = 1

        self.groups_draws()
        self.groups_matches()
        champion1, champion2 = self.groups_results()
        return champion1, champion2
        #self.groups_toknock()

    #Initializing each of the groups in the group stage
    def groups_draws(self):
        for i in range(0, self.nn):
            #Points, Games, Victories, Draws, Defeats, Goals
            self.totalgroups[str(self.actual_bracket[i])] = [0, 0, 0, 0, 0, 0]

        #self.totalgroups[self.actual_bracket[1]][2] = 3
        
        print(self.totalgroups)


    #The group stage table: each team's points, wins, draws, goals, etc.
    def groups_matches(self):

        for h in range(0, self.t):
            mn = 0
            for j in range(mn,self.nn):
                for i in range(mn,self.nn):

                    if j == i:
                        pass

                    else:

                        force1 = (self.seed[self.listofteams.index(self.actual_bracket[j])] - self.seed[self.listofteams.index(self.actual_bracket[i])])
                        force2 = (self.seed[self.listofteams.index(self.actual_bracket[i])] - self.seed[self.listofteams.index(self.actual_bracket[j])])

                        value1 = self.result(times=force1)
                        value2 = self.result(times=force2)

                        if value1 > value2:
                            #print(f'{self.actual_bracket[j]} {value1} - {value2} {self.actual_bracket[i]}')
                            self.totalgroups[self.actual_bracket[j]][0] += 3
                            self.totalgroups[self.actual_bracket[j]][2] += 1
                            self.totalgroups[self.actual_bracket[j]][5] += value1 - value2
                            self.totalgroups[self.actual_bracket[i]][1] += 1
                            self.totalgroups[self.actual_bracket[j]][1] += 1
                            self.totalgroups[self.actual_bracket[i]][4] += 1
                            self.totalgroups[self.actual_bracket[i]][5] += value2 - value1
                            

                        elif value2 > value1:
                            #print(f'{self.actual_bracket[j]} {value1} - {value2} {self.actual_bracket[i]}')
                            self.totalgroups[self.actual_bracket[i]][0] += 3
                            self.totalgroups[self.actual_bracket[i]][2] += 1
                            self.totalgroups[self.actual_bracket[i]][5] += value2 - value1
                            self.totalgroups[self.actual_bracket[i]][1] += 1
                            self.totalgroups[self.actual_bracket[j]][1] += 1
                            self.totalgroups[self.actual_bracket[j]][4] += 1
                            self.totalgroups[self.actual_bracket[j]][5] += value1 - value2

                        elif value1 == value2:
                            #print(f'{self.actual_bracket[j]} {value1} - {value2} {self.actual_bracket[i]}')
                            self.totalgroups[self.actual_bracket[i]][0] += 1
                            self.totalgroups[self.actual_bracket[j]][0] += 1
                            self.totalgroups[self.actual_bracket[i]][3] += 1
                            self.totalgroups[self.actual_bracket[j]][3] += 1
                            self.totalgroups[self.actual_bracket[i]][1] += 1
                            self.totalgroups[self.actual_bracket[j]][1] += 1

                mn += 1

    #Function to determine the final table result
    def groups_results(self):
        totalcopy = self.totalgroups.copy()
        print(totalcopy)
        finalresults = {}
        safe = 'string'

        for j in range(0, self.nn-1):
            a = 0
            b = 0
            i = 0
            last = 0

            #This loop will keep checking which team has more points and remove it from the list at the end
            for keys,values in self.totalgroups.items():
                last = str(keys)
                print(values[0], a)
                if values[0] > a:
                    a = values[0]
                    b = values[5]
                    safe = str(keys)
                elif values[0] == a:
                    if values[5] > b:
                        a = values[0]
                        b = values[5]
                        safe = str(keys)
                    else:
                        pass
                else:
                    pass
                i += 1
            
            self.finalstand.append(safe)
            del self.totalgroups[str(safe)]

        self.finalstand.append(last)

        for k in range(0, self.nn):
            finalresults[str(self.finalstand[k])] = totalcopy[self.finalstand[k]]

        return self.finalstand[0], self.finalstand[1]

    #Initialization of a World Cup 
    def wc_init(self):
        self.grps = 8
        self.per_group = int(self.n/self.grps)
        self.classified = 2
        self.nn = 4
        self.teams_group = []

        #The range indicates how many times the World Cup will be ran
        #in this case, 2022022 times
        for i in range(2022022):
            self.wc_execute()

        self.wc_percent_results()

    #Execution of a World Cup
    def wc_execute(self):
        variable = 0
        for i in range(self.grps):
            self.teams_group.append(self.teams[variable])
            self.teams_group.append(self.teams[variable+1])
            self.teams_group.append(self.teams[variable+2])
            self.teams_group.append(self.teams[variable+3])

            variable += 4

            self.orderedBattles()
            champ1,champ2 = self.groups_init()

            self.rosixteen[(champ1)][0] += 1 
            self.rosixteen[(champ2)][0] += 1 

            self.finalists.append(champ1)
            self.finalists.append(champ2)

        self.actual_bracket = []
        self.teams = []
        print("---")
        #nkn = int(input("Choose the amount of teams that will head to the knockout stage."))
        nkn = 16
        
        for j in range(0, nkn):
            self.teams.append(self.finalists[j])
        
        self.n = len(self.teams)
        self.wcBattles()
        print(self.actual_bracket)

        self.knock_init()

        self.teams = list(self.countrylist)
        self.teams_group = list(self.countrylist)
        self.finalists = []

    #Displaying the results at the end
    def wc_percent_results(self):

        print()

        print("Round of Sixteen:")
        print(self.rosixteen)

        print("--------")

        print("Quarterfinals:")
        print(self.quarterfinals)
        

        print("--------")

        print("Semifinals:")
        print(self.semifinals)

        print("--------")

        print("Finals:")
        print(self.finals)

        print("--------")

        print("Champions:")
        print(self.champion)

champ = Camp()

champ.orderedBattles()

champ.wc_init()
