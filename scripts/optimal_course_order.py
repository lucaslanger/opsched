import itertools

def optimal_course_order(graph): # graph contains courses along with easyness, how good, hotness,
    possible_orderings = gen_possible_orderings(graph)

    f_candidates = []
    for c in graph:
        if graph[c]['prereqs'] == []:
            f_candidates.append(c)

    f_combinations = itertools.combinations(candidates, 5)
    w_combinations = []
    for comb in f_combinations:
        f_comb_dict = {}
        for c in comb:
            f_comb_dict[c] = True

        w_canditates = [cand for cand in f_candidates if f_comb_dict.has_key(c) == False]
        w_combinations.append()

def is_valid_schedule(course_times, courses, semester):    
    sched = {'M':[],'T': [],'W':[],'TR':[],'F':[] }

    for c in courses:
        data = course_times[c + "_" + semester]
        days = data[5].split("")
        time = data[7]
        for d in days:
            valid = try_time(d, time)
            if valid == False:
                return False
    return True

def try_time(day, time):
    for t in sched[day]:
        if collision(time, t) == True:
            return False

    return True

def collision(time, t): #time[1] must be greater than or equal to t[0], if time[1] is greater, need to check 
    if (time[1] > t[0] and time[1] <= t[1] ) or (time[1] > t[1] and time[0] < t[1]):  
        return True
    else:
        return False

print is_valid_schedule( [5,10], [4,5])