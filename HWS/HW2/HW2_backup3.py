class Efficiency:

    def init(self, app_list, week_spla, week_lahsa, curr_spla, curr_lahsa):
        # set a flag to determine the next organization, at first, it is spla's turn
        is_spla = True
        chosen_list = []
        self.max_efficiency(app_list, week_spla, week_lahsa, curr_spla, curr_lahsa, is_spla, chosen_list)

    def max_efficiency(self, app_list, week_spla, week_lahsa, curr_spla, curr_lahsa, is_spla, chosen_list):

        # if there is no more candidates can be picked
        if self.is_over(app_list, chosen_list):
            print(chosen_list)
            print(curr_spla)
            print(curr_lahsa)
            return

        # SPLA's turn:
        if is_spla:
            # determine whether there is at least one qualified candidate
            does_exist = False
            size = len(app_list)
            # for candidate in app_list:
            for candidate_index in range(size):
                # choose the qualified candidates for SPLA, calculate the efficiency
                if app_list[candidate_index][10:13] == "NYY":

                    candidate = app_list[candidate_index]

                    # for pruning!!!! calculate the contribution of one candidate
                    score = 0

                    # record for backtracking!!!
                    temp_week_spla = list(week_spla)
                    temp_week_lahsa = list(week_lahsa)
                    temp_curr_spla = curr_spla

                    for index in range(7):
                        # if there exists one day that exceed the remaining room, then rule out
                        if int(candidate[13 + index:14 + index]) == 1 and week_spla[index] + 1 > p_spla:
                            score = 0
                            week_spla = list(temp_week_spla)
                            week_lahsa = list(temp_week_lahsa)
                            curr_spla = temp_curr_spla
                            break
                        if int(candidate[13 + index:14 + index]) == 1 and week_spla[index] < p_spla:
                            week_spla[index] += 1
                            curr_spla = curr_spla + 1

                            score = score + 1

                    # pruning!!!! though qualified, if the contribution is zero / spaces are exceeded, then rule out
                    if score == 0:
                        continue
                    # if the score is bigger than 0, which means there exists at least one candidate can be accommodated
                    does_exist = True
                    chosen_list.append(candidate)
                    app_list.pop(candidate_index)
                    # change turn to another organization
                    is_spla = not is_spla
                    self.max_efficiency(app_list, week_spla, week_lahsa, curr_spla, curr_lahsa, is_spla, chosen_list)
                    # backtracking!!!!
                    is_spla = not is_spla
                    app_list.insert(candidate_index, candidate)
                    chosen_list.remove(app_list[candidate_index])
                    week_spla = list(temp_week_spla)
                    week_lahsa = list(temp_week_lahsa)
                    curr_spla = temp_curr_spla

            if not does_exist:
                chosen_list.append("none")
                is_spla = not is_spla
                self.max_efficiency(app_list, week_spla, week_lahsa, curr_spla, curr_lahsa, is_spla,
                                    chosen_list)
                # backtracking!!!!????
                is_spla = not is_spla
                chosen_list.pop(len(chosen_list) - 1)

        # LAHSA's turn:
        if not is_spla:
            # determine whether there is at least one qualified candidate
            does_exist = False
            size = len(app_list)
            # for candidate in app_list:
            for candidate_index in range(size):
                # choose the qualified candidates for LAHSA, calculate the efficiency
                if app_list[candidate_index][5:6] == "F" and int(app_list[candidate_index][6:9]) > 17 and app_list[candidate_index][9:10] == "N":
                    candidate = app_list[candidate_index]
                    # for pruning!!!! calculate the contribution of one candidate
                    score = 0
                    # record for backtracking!!!
                    temp_week_lahsa = list(week_lahsa)
                    temp_week_spla = list(week_spla)
                    temp_curr_lahsa = curr_lahsa
                    for index in range(7):
                        # if there exists one day that exceed the remaining room, then rule out
                        if int(candidate[13 + index:14 + index]) == 1 and week_lahsa[index] + 1 > b_lahsa:
                            score = 0
                            week_lahsa = list(temp_week_lahsa)
                            week_spla = list(temp_week_spla)
                            curr_lahsa = temp_curr_lahsa
                            break
                        # if candidate request for room for a day and the day has remaining room
                        if int(candidate[13 + index:14 + index]) == 1 and week_lahsa[index] < b_lahsa:
                            week_lahsa[index] += 1
                            curr_lahsa = curr_lahsa + 1

                            score = score + 1
                    # pruning!!!! though qualified, if the contribution is zero, then rule out
                    if score == 0:
                        continue

                    does_exist = True
                    chosen_list.append(candidate)
                    app_list.pop(candidate_index)
                    # change turn to another organization
                    is_spla = not is_spla
                    self.max_efficiency(app_list, week_spla, week_lahsa, curr_spla, curr_lahsa, is_spla,
                                        chosen_list)
                    # backtracking!!!!
                    is_spla = not is_spla
                    app_list.insert(candidate_index, candidate)
                    chosen_list.remove(candidate)
                    week_lahsa = list(temp_week_lahsa)
                    week_spla = list(temp_week_spla)
                    curr_lahsa = temp_curr_lahsa

            if not does_exist:
                chosen_list.append("none")
                is_spla = not is_spla
                self.max_efficiency(app_list, week_spla, week_lahsa, curr_spla, curr_lahsa, is_spla,
                                    chosen_list)
                # backtracking!!!!????
                is_spla = not is_spla
                chosen_list.pop(len(chosen_list) - 1)

    def is_over(self, app_list, chosen_list):
        if len(app_list) == 0:
            return True
        if len(chosen_list) > 1:
            # if the last two chosen nodes are both marked as "none", then it indicates the choosing is over
            if chosen_list[len(chosen_list) - 1] == "none" and chosen_list[len(chosen_list) - 2] == "none":
                return True
        return False





with open("input6.txt") as input_file:
    lines = input_file.read().splitlines()
    b_lahsa = int(lines[0])
    p_spla = int(lines[1])
    l_so_far = int(lines[2])
    s_so_far = int(lines[3 + l_so_far])
    total = int(lines[4 + l_so_far + s_so_far])

    # create remaining applicants list, calculate the init state
    app_list = []
    spla_set = set()
    lahsa_set = set()
    for index in range(s_so_far):
        spla_set.add(int(lines[4 + l_so_far + index]))

    for index in range(l_so_far):
        lahsa_set.add(int(lines[3 + index]))

    week_spla = [0, 0, 0, 0, 0, 0, 0]
    week_lahsa = [0, 0, 0, 0, 0, 0, 0]
    curr_spla = 0
    curr_lahsa = 0
    for index in range(total):
        applicant = lines[5 + l_so_far + s_so_far + index]
        if index + 1 in spla_set:
            for i in range(7):
                if int(applicant[13 + i:14 + i]) == 1:
                    week_spla[i] += int(applicant[13 + i:14 + i])
                    curr_spla = curr_spla + 1
        elif index + 1 in lahsa_set:
            for i in range(7):
                if int(applicant[13 + i:14 + i]) == 1:
                    week_lahsa[i] += int(applicant[13 + i:14 + i])
                    curr_lahsa = curr_lahsa + 1
        else:
            app_list.append(applicant)

    # print(app_list)
    # print(week_spla)
    # print(week_lahsa)
    # print(curr_spla)
    # print(curr_lahsa)

    efficiency = Efficiency()
    efficiency.init(app_list, week_spla, week_lahsa, curr_spla, curr_lahsa)

with open("output.txt", "w") as output_file:
    output_file.write("rytryt" + "\n")
