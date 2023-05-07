import functions, fuzzywc
import random

def knock_callMatches(next_bracket, number_placements, multwo, actual_bracket, datajson, round):
    print(f"Huh? - {next_bracket}")

    while len(actual_bracket) != 1:
        next_bracket, number_placements = knock_round_of(
            multwo, actual_bracket, next_bracket, datajson, round, number_placements)

        print(next_bracket)
        print("---")
        round+= 1
        actual_bracket = next_bracket
        next_bracket = []

    print(f"The champion is {actual_bracket[0]}!")

def knock_round_of(multwo, actual_bracket, next_bracket, datajson, round, number_placements):

    current_bracket = []

    team1 = 0
    team2 = 1

    for l in range(0, int((pow(2,multwo-round)/2))):

        current_bracket.append(actual_bracket[int(team1)])
        current_bracket.append(actual_bracket[int(team2)])

        if 'bye' in current_bracket[0]:
            next_bracket.append(current_bracket[1])
            print(f'{current_bracket[0]} 0 - 1 {current_bracket[1]}')
        elif 'bye' in current_bracket[1]:
            next_bracket.append(current_bracket[0])
            print(f'{current_bracket[0]} 1 - 0 {current_bracket[1]}')
        else:

            defs = datajson[str(current_bracket[0])]["StatsNL22"]["Defense"] - datajson[str(current_bracket[1])]["StatsNL22"]["Defense"]
            mid = datajson[str(current_bracket[0])]["StatsNL22"]["Midfield"] - datajson[str(current_bracket[1])]["StatsNL22"]["Midfield"]
            atk = datajson[str(current_bracket[0])]["StatsNL22"]["Attack"] - datajson[str(current_bracket[1])]["StatsNL22"]["Attack"]
            ben = datajson[str(current_bracket[0])]["StatsNL22"]["Bench"] - datajson[str(current_bracket[1])]["StatsNL22"]["Bench"]

            force1 = int((fuzzywc.entrance_fuzzy(defs, mid, atk, ben))/10)
            force2 = force1 * (-1)
    
            value1 = functions.result(times=force1)
            value2 = functions.result(times=force2)

            if value1 > value2:
                if (pow(2,multwo-round)/2) >= 8:
                    number_placements.loc[number_placements[f'Countries'] == f'{(current_bracket[0])}','Quarterfinals'] += 1
                elif (pow(2,multwo-round)/2) >= 4:
                    number_placements.loc[number_placements[f'Countries'] == f'{(current_bracket[0])}','Semifinals'] += 1
                elif (pow(2,multwo-round)/2) >= 2:
                    number_placements.loc[number_placements[f'Countries'] == f'{(current_bracket[0])}','Finals'] += 1
                elif (pow(2,multwo-round)/2) == 1:
                    number_placements.loc[number_placements[f'Countries'] == f'{(current_bracket[0])}','Champion'] += 1

                next_bracket.append(current_bracket[0])
                print(f'{current_bracket[0]} {value1} - {value2} {current_bracket[1]}')

            if value2 > value1:
                if (pow(2,multwo-round)/2) >= 8:
                    number_placements.loc[number_placements[f'Countries'] == f'{(current_bracket[1])}','Quarterfinals'] += 1
                elif (pow(2,multwo-round)/2) >= 4:
                    number_placements.loc[number_placements[f'Countries'] == f'{(current_bracket[1])}','Semifinals'] += 1
                elif (pow(2,multwo-round)/2) >= 2:
                    number_placements.loc[number_placements[f'Countries'] == f'{(current_bracket[1])}','Finals'] += 1
                elif (pow(2,multwo-round)/2) >= 1:
                    number_placements.loc[number_placements[f'Countries'] == f'{(current_bracket[1])}','Champion'] += 1

                next_bracket.append(current_bracket[1])
                print(f'{current_bracket[0]} {value1} - {value2} {current_bracket[1]}')

            if value1 == value2:
                past = random.choice(current_bracket)

                if (pow(2,multwo-round)/2) >= 8:
                    number_placements.loc[number_placements[f'Countries'] == f'{(past)}','Quarterfinals'] += 1
                elif (pow(2,multwo-round)/2) >= 4:
                    number_placements.loc[number_placements[f'Countries'] == f'{(past)}','Semifinals'] += 1
                elif (pow(2,multwo-round)/2) >= 2:
                    number_placements.loc[number_placements[f'Countries'] == f'{(past)}','Finals'] += 1
                elif (pow(2,multwo-round)/2) >= 1:
                    number_placements.loc[number_placements[f'Countries'] == f'{(past)}','Champion'] += 1

                next_bracket.append(past)
                print(f'{current_bracket[0]} {value1} - {value2} {current_bracket[1]}')
                print(f'{past} wins on penalties!')

        team1 += 2
        team2 += 2

        current_bracket = []

    return next_bracket, number_placements

def knock_onlyphase(actual_bracket, next_bracket, datajson, number_placements):

    current_bracket = []

    team1 = 0
    team2 = 1

    for l in range(0, int((len(actual_bracket)/2))):

        current_bracket.append(actual_bracket[int(team1)])
        current_bracket.append(actual_bracket[int(team2)])

        if 'bye' in current_bracket[0]:
            next_bracket.append(current_bracket[1])
            print(f'{current_bracket[0]} 0 - 1 {current_bracket[1]}')
        elif 'bye' in current_bracket[1]:
            next_bracket.append(current_bracket[0])
            print(f'{current_bracket[0]} 1 - 0 {current_bracket[1]}')
        else:

            defs = datajson[str(current_bracket[0])]["StatsNL22"]["Defense"] - datajson[str(current_bracket[1])]["StatsNL22"]["Defense"]
            mid = datajson[str(current_bracket[0])]["StatsNL22"]["Midfield"] - datajson[str(current_bracket[1])]["StatsNL22"]["Midfield"]
            atk = datajson[str(current_bracket[0])]["StatsNL22"]["Attack"] - datajson[str(current_bracket[1])]["StatsNL22"]["Attack"]
            ben = datajson[str(current_bracket[0])]["StatsNL22"]["Bench"] - datajson[str(current_bracket[1])]["StatsNL22"]["Bench"]

            force1 = int((fuzzywc.entrance_fuzzy(defs, mid, atk, ben))/10)
            force2 = force1 * (-1)
    
            value1 = functions.result(times=force1)
            value2 = functions.result(times=force2)

            if value1 > value2:

                next_bracket.append(current_bracket[0])
                print(f'{current_bracket[0]} {value1} - {value2} {current_bracket[1]}')

            if value2 > value1:

                next_bracket.append(current_bracket[1])
                print(f'{current_bracket[0]} {value1} - {value2} {current_bracket[1]}')

            if value1 == value2:
                past = random.choice(current_bracket)

                next_bracket.append(past)
                print(f'{current_bracket[0]} {value1} - {value2} {current_bracket[1]}')
                print(f'{past} wins on penalties!')

        team1 += 2
        team2 += 2

        current_bracket = []

    return next_bracket, number_placements

def groups_matches(datajson, turns, nn, actual_bracket, totalgroups):

    for h in range(0, turns):
        mn = 0
        for j in range(mn,len(totalgroups)):
            for i in range(mn,len(totalgroups)):

                if j == i:
                    pass

                else:

                    defs = datajson[str(actual_bracket[j])]["StatsNL22"]["Defense"] - datajson[str(actual_bracket[i])]["StatsNL22"]["Defense"]
                    mid = datajson[str(actual_bracket[j])]["StatsNL22"]["Midfield"] - datajson[str(actual_bracket[i])]["StatsNL22"]["Midfield"]
                    atk = datajson[str(actual_bracket[j])]["StatsNL22"]["Attack"] - datajson[str(actual_bracket[i])]["StatsNL22"]["Attack"]
                    ben = datajson[str(actual_bracket[j])]["StatsNL22"]["Bench"] - datajson[str(actual_bracket[i])]["StatsNL22"]["Bench"]

                    force1 = int((fuzzywc.entrance_fuzzy(defs, mid, atk, ben))/10)
                    force2 = force1 * (-1)

                    value1 = functions.result(times=force1)
                    value2 = functions.result(times=force2)

                    if value1 > value2:
                        print(f'{actual_bracket[j]} {value1} - {value2} {actual_bracket[i]}')
                        totalgroups = victory_parade(totalgroups, actual_bracket[j], actual_bracket[i], (value1 - value2), 'w')                        

                    elif value2 > value1:
                        print(f'{actual_bracket[j]} {value1} - {value2} {actual_bracket[i]}')
                        totalgroups = victory_parade(totalgroups, actual_bracket[i], actual_bracket[j], (value2 - value1), 'w')  

                    elif value1 == value2:
                        print(f'{actual_bracket[j]} {value1} - {value2} {actual_bracket[i]}')
                        totalgroups = victory_parade(totalgroups, actual_bracket[i], actual_bracket[j], 0, 'd')  

            mn += 1

    
    return totalgroups

def victory_parade(totalgroups, victory, defeat, goals, wd):

    if wd == 'w':

        totalgroups.loc[totalgroups[f'Countries'] == f'{(victory)}','Points'] += 3
        totalgroups.loc[totalgroups[f'Countries'] == f'{(victory)}','Victories'] += 1
        totalgroups.loc[totalgroups[f'Countries'] == f'{(victory)}','Goals'] += goals
        totalgroups.loc[totalgroups[f'Countries'] == f'{(victory)}','Games'] += 1
        totalgroups.loc[totalgroups[f'Countries'] == f'{(defeat)}','Games'] += 1
        totalgroups.loc[totalgroups[f'Countries'] == f'{(defeat)}','Defeats'] += 1
        totalgroups.loc[totalgroups[f'Countries'] == f'{(defeat)}','Goals'] -= goals

    if wd == 'd':

        totalgroups.loc[totalgroups[f'Countries'] == f'{(victory)}','Points'] += 1
        totalgroups.loc[totalgroups[f'Countries'] == f'{(defeat)}','Points'] += 1
        totalgroups.loc[totalgroups[f'Countries'] == f'{(victory)}','Draws'] += 1
        totalgroups.loc[totalgroups[f'Countries'] == f'{(defeat)}','Draws'] += 1
        totalgroups.loc[totalgroups[f'Countries'] == f'{(victory)}','Games'] += 1
        totalgroups.loc[totalgroups[f'Countries'] == f'{(defeat)}','Games'] += 1

    return totalgroups