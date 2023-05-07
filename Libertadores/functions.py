
import random
import pandas as pd

def result(times=0):
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

        #print(f'seed {times} + results {total}')

        return int((total[0]+total[1])/(2))

def groups_draws(actual_bracket, nn):

    zeroes = []
    teams = []

    for i in range(0, len(actual_bracket)):
        zeroes.append(0)
        teams.append(actual_bracket[i])
        #Points, Games, Victories, Draws, Defeats, Goals

    #self.totalgroups[self.actual_bracket[1]][2] = 3
    d = {'Countries': teams, 'Points': zeroes, 'Games':zeroes, 'Victories': zeroes, 'Draws': zeroes, 'Defeats': zeroes, 'Goals': zeroes}
    teams_determined = pd.DataFrame(data=d)
    
    return teams_determined