import math
import random
from re import I

class Camp(object):
    def __init__(self):
        # creating empty lists
        self.teams = []
        self.listofteams = []
        self.seed = []
        self.actual_bracket = []
        self.next_bracket = []
        
        #variables to determine number of byes
        self.multwo = 0
        self.multj = 1 

        #variable to determine if seeding is set or not
        self.seed_set = 0

        # number of elements as input
        self.n = int(input("Enter number of teams: "))

        # iterating till the range
        for i in range(0, self.n):
            country = input()
        
            self.teams.append(country) # adding the element
            self.listofteams.append(country)

        detail = 0

        #determine if teams will be seeded or not

        while detail == 0:
            print("Do you want the tourney to be seeded in the chosen order of teams? (y/n)")
            print("The first team will be the best seed, the last team will be the worst seed.")
            choose = input()
            print("---")
            if choose == 'y':
                print("Teams will be seeded!")
                print(self.seed)
                self.seed_set = 1
                detail = 1

            elif choose == 'n':
                print("Teams will not be seeded!")
                self.seed_set = 0
                detail = 1

            else:
                print("Please try again.")

        #seed the teams

        if self.n >= 10:
            sed = int(self.n/10)
            seed_value = 10

            for i in range(0,self.n):
                if self.seed_set == 1:
                    if i > sed:
                        seed_value -= 1
                        sed += int(self.n/10)
                    self.seed.append(seed_value)
                if self.seed_set == 0:
                    self.seed.append(0)

        else:
            sed = int(10/self.n)
            seed_value = 10

            for i in range (0,self.n):
                if self.seed_set == 1:
                    self.seed.append(seed_value)
                    seed_value -= sed
                if self.seed_set == 0:
                    self.seed.append(0)



    def randomBattles(self):
        n_random = self.n-1

        for k in range(0, self.n):
            random_value = random.uniform(1,n_random)

            self.actual_bracket.append(self.teams[int(random_value)]) # randomizing the bracket
            del self.teams[int(random_value)]
            n_random -= 1

    def orderedBattles(self):
        self.actual_bracket = self.teams
        self.teams = []

    def result(self, times=0):
        total = []

        if times < 0:
            times = 0

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

        print(f'seed {times} + results {total}')

        return int((total[0]+total[1])/(2))

    def knock_init(self):

        #control variables
        self.score = 0
        self.round = 0
        self.current_bracket = []

        self.knock_2n()
        self.addByes()
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

    def knock_round_of(self):

        team1 = 0
        team2 = 1

        for l in range(0, int((pow(2,self.multwo-self.round)/2))):

            self.current_bracket.append(self.actual_bracket[int(team1)])
            self.current_bracket.append(self.actual_bracket[int(team2)])

            if 'bye' in self.current_bracket[0]:
                self.next_bracket.append(self.current_bracket[1])
                print(f'{self.current_bracket[0]} 0 - 1 {self.current_bracket[1]}')
            elif 'bye' in self.current_bracket[1]:
                self.next_bracket.append(self.current_bracket[0])
                print(f'{self.current_bracket[0]} 1 - 0 {self.current_bracket[1]}')
            else:

                force1 = (self.seed[self.listofteams.index(self.current_bracket[0])] - self.seed[self.listofteams.index(self.current_bracket[1])])
                force2 = (self.seed[self.listofteams.index(self.current_bracket[1])] - self.seed[self.listofteams.index(self.current_bracket[0])])
                
                value1 = self.result(times=force1)
                value2 = self.result(times=force2)

                if value1 > value2:
                    self.next_bracket.append(self.current_bracket[0])
                    print(f'{self.current_bracket[0]} {value1} - {value2} {self.current_bracket[1]}')

                if value2 > value1:
                    self.next_bracket.append(self.current_bracket[1])
                    print(f'{self.current_bracket[0]} {value1} - {value2} {self.current_bracket[1]}')

                if value1 == value2:
                    past = random.choice(self.current_bracket)
                    self.next_bracket.append(past)
                    print(f'{self.current_bracket[0]} {value1} - {value2} {self.current_bracket[1]}')
                    print(f'{past} wins on penalties!')

            team1 += 2
            team2 += 2

            self.current_bracket = []

    def knock_callMatches(self):
        while len(self.actual_bracket) != 1:
            self.knock_round_of()

            print(self.next_bracket)
            print("---")
            self.round+= 1
            self.actual_bracket = self.next_bracket
            self.next_bracket = []

        print(f"The champion is {self.actual_bracket[0]}!")

    def groups_init(self):
        self.totalgroups = {}
        self.finalstand = []
        
        self.t = int(input("Enter number of turns: "))

        self.groups_draws()
        self.groups_matches()
        self.groups_results()
        self.groups_toknock()

    def groups_draws(self):
        for i in range(0, self.n):
            #Points, Games, Victories, Draws, Defeats, Goals
            self.totalgroups[str(self.actual_bracket[i])] = [0, 0, 0, 0, 0, 0]

        #self.totalgroups[self.actual_bracket[1]][2] = 3
        
        print(self.totalgroups)

    def groups_matches(self):

        for h in range(0, self.t):
            mn = 0
            for j in range(mn,self.n):
                for i in range(mn,self.n):

                    if j == i:
                        pass

                    else:

                        force1 = (self.seed[self.listofteams.index(self.actual_bracket[j])] - self.seed[self.listofteams.index(self.actual_bracket[i])])
                        force2 = (self.seed[self.listofteams.index(self.actual_bracket[i])] - self.seed[self.listofteams.index(self.actual_bracket[j])])

                        value1 = self.result(times=force1)
                        value2 = self.result(times=force2)

                        if value1 > value2:
                            print(f'{self.actual_bracket[j]} {value1} - {value2} {self.actual_bracket[i]}')
                            self.totalgroups[self.actual_bracket[j]][0] += 3
                            self.totalgroups[self.actual_bracket[j]][2] += 1
                            self.totalgroups[self.actual_bracket[j]][5] += value1 - value2
                            self.totalgroups[self.actual_bracket[i]][1] += 1
                            self.totalgroups[self.actual_bracket[j]][1] += 1
                            self.totalgroups[self.actual_bracket[i]][4] += 1
                            self.totalgroups[self.actual_bracket[i]][5] += value2 - value1
                            

                        elif value2 > value1:
                            print(f'{self.actual_bracket[j]} {value1} - {value2} {self.actual_bracket[i]}')
                            self.totalgroups[self.actual_bracket[i]][0] += 3
                            self.totalgroups[self.actual_bracket[i]][2] += 1
                            self.totalgroups[self.actual_bracket[i]][5] += value2 - value1
                            self.totalgroups[self.actual_bracket[i]][1] += 1
                            self.totalgroups[self.actual_bracket[j]][1] += 1
                            self.totalgroups[self.actual_bracket[j]][4] += 1
                            self.totalgroups[self.actual_bracket[j]][5] += value1 - value2

                        elif value1 == value2:
                            print(f'{self.actual_bracket[j]} {value1} - {value2} {self.actual_bracket[i]}')
                            self.totalgroups[self.actual_bracket[i]][0] += 1
                            self.totalgroups[self.actual_bracket[j]][0] += 1
                            self.totalgroups[self.actual_bracket[i]][3] += 1
                            self.totalgroups[self.actual_bracket[j]][3] += 1
                            self.totalgroups[self.actual_bracket[i]][1] += 1
                            self.totalgroups[self.actual_bracket[j]][1] += 1

                mn += 1

    def groups_results(self):
        totalcopy = self.totalgroups.copy()
        finalresults = {}

        for j in range(0, self.n):
            a = 0
            b = 0
            i = 0
            safe = 'str'
            for keys,values in self.totalgroups.items():
                if values[0] > a:
                    a = values[0]
                    b = values[2]
                    safe = str(keys)
                if values[0] == a:
                    if values[2] > b:
                        a = values[0]
                        b = values[2]
                        safe = str(keys)
                    else:
                        pass
                else:
                    pass

                i += 1
                #print(f"keys = {safe} + {type(safe)}")
            
            self.finalstand.append(safe)
            del self.totalgroups[str(safe)]

        for k in range(0, self.n):
            finalresults[str(self.finalstand[k])] = totalcopy[self.finalstand[k]]

        print("--- Name - Points - Games - Victories - Draws - Defeats - Goals")
        for key, value in finalresults.items():
            print(f"{key} - {value}")

            b += 1

    def groups_toknock(self):
        print("---")
        detail = 0

        while detail == 0:
            kn = str(input("Do you want to move this result to a knockout stage? (y/n)"))
            if kn == 'n':
                print("---")
                print(f"The champion is {self.finalstand[0]}!")
                detail = 1

            elif kn == 'y':
                self.actual_bracket = []
                self.teams = []
                print("---")
                nkn = int(input("Choose the amount of teams that will head to the knockout stage."))
                
                for j in range(0, nkn):
                    self.teams.append(self.finalstand[j])
                
                self.n = len(self.teams)
                self.randomBattles()
                print(self.actual_bracket)
                detail = 1

                self.knock_init()

            else:
                print("Please try again.")


champ = Camp()

detail = 0

while detail == 0:
    print("Will the battles be randomized or set in an order? (r/o)")
    randorder = input()
    print("---")
    if randorder == 'r':
        print("Randomize chosen!")
        champ.randomBattles()
        detail = 1

    elif randorder == 'o':
        print("Ordered chosen!")
        champ.orderedBattles()
        detail = 1

    else:
        print("Please try again.")

detail = 0

while detail == 0:
    print("Will the tourney be a group stage or knockout? (g/k)")
    choose = input()
    print("---")
    if choose == 'g':
        print("Group chosen!")
        champ.groups_init()
        detail = 1

    elif choose == 'k':
        print("Knockout chosen!")
        champ.knock_init()
        detail = 1

    else:
        print("Please try again.")

