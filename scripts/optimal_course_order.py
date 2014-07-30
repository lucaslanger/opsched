import itertools
import re
import json

found = 0
not_found = 0

def gen_possible_schedules(program, semester, fload=5, wload=5): # should also take, semester that one starts from and completed courses
    with open('../data/course_database.txt', 'r') as f:
	course_database = json.load(f)
    
    if semester == 'fall':
	schedules = {}
	f_comb_dict = {}
	w_comb_dict = {}
    
	f_candidates = determine_candidates(course_database, program, 'fall',{})
	#print len(f_candidates)
	
	f_combs = list(itertools.combinations(f_candidates, fload ) )

	for fc in f_combs:
	    f_comb_dict[fc] = find_valid_combs(course_database, fc, 'fall')
	    
	    if len(f_comb_dict[fc]) > 0: 
		seen_courses = {}
		for c in fc:
		    seen_courses[c] = True
		    
		#kindof a recursive step, but since only 2 cases and need to track schedules, wrote it out again	
    
		w_candidates = determine_candidates(course_database, program, 'winter' ,seen_courses)
		#print len(w_candidates)
    
		w_combs = list(itertools.combinations( w_candidates, wload ) )
		for wc in w_combs:
		    w_comb_dict[wc] = find_valid_combs( course_database, wc, 'winter' )
		    if len( w_comb_dict[wc]) > 0:
			if schedules.has_key( fc ):
			    schedules[fc].append( wc )	
			else:
			    schedules[fc] = [wc]
			    	    
	return schedules, f_comb_dict, w_comb_dict
    
    elif semester == 'winter':
	schedules = {}
	
	w_candidates = determine_candidates(course_database,'winter',{})
	print w_candidates
	
	w_combs = list(itertools.combinations(w_candidates, wload ) )
	for wc in w_combs:
	    schedules[wc] = find_valid_combs(course_database, wc, 'fall')
	    
	

def optimize(schedules, fcomb, wcomb, filt3r ):
    with open('../data/teacher_data.txt', 'r') as f:
	ratings = json.load(f)
    
    optimal_score = 0
    optimal = None
    
    low = None
    
    for fc in schedules:
	for i in fcomb[fc]:
	    f_score, teacher_course_f, f_entries = get_score(i, ratings, filt3r)
	    for wc in schedules[fc]:
		for j in wcomb[wc]:
		    w_score, teacher_course_w, w_entries = get_score(j, ratings, filt3r)
		    total = (f_score + w_score) / (w_entries + f_entries )
		    if total > optimal_score:
			optimal = [teacher_course_f, teacher_course_w]
			optimal_score = total
			
		    elif low == None or total < low:
			low = total
		
    print low, optimal_score, optimal		
    return optimal, optimal_score	
	
def get_score(courses,ratings, filt3r):
    #global found, not_found
    filter_dict = {'hotness': -1, 'easyness': -2, 'quality': -3}
    total = 0
    entries = 0 
    data = []
    for c in courses:
	instructors = c['Instructor']
	course, typ3 = c['Course'], c['Type']

	score = 0.0
	known_teachers = 0.0
	for i in instructors:
    
	    if re.findall('TBA', i) != None and ratings.has_key(i):
		#score = float(ratings[instructor][ filter_dict[filt3r] ])
		score += float(ratings[i][2])
		#data.append( (course, typ3, instructor, score) )
		known_teachers += 1 
	    #    found += 1
	    #else:
	     
	    #    not_found+=1
		
		#total += 2.0
	
	if known_teachers != 0:
	    avg = score/known_teachers
	    data.append( (course, typ3 , instructors, avg))
	    total += avg
	    entries += 1
	else:
	    
	    data.append( (course, typ3 , instructors, 'N/A'))
    	    
    return total, data, entries    
	
def process_name(name):
    try:
        parts = re.findall('[A-Za-z]{3,50}', name)
        new_name = parts[0] + " " + parts[-1]
        return new_name
    except:
        print "Problem: " + name
        return name
    


def determine_candidates(course_database, program ,semester ,completed):
	cands = []
	mc = max_completed(completed)

	for key in program:
	    t = course_database[key].has_key(semester)
	    
	    if key not in completed and t:
		possible = True
		for p in course_database[key]['prereq']:
		    try:
			pl = int( re.findall(r'-[0-9]{3,6}', p)[0][1] )
		    except:
			pl = None
		    try:
			l = int(re.findall(r'Level[0-9]',p)[0][5])
		    except:
			l = None
			
		    if pl != None and pl >= 2 and p not in completed: #ignores prereqs below 100 level
			possible = False
			break
		    
		    elif l != None and mc < l - 1: # checks if mcgill had a high-level course with no prereqs
			possible = False
			break
		
		if possible:    
		    cands.append(key)			

	return cands
    
    
def max_completed(completed):
    m = 0
    for c in completed.keys():
	l = int(re.findall(r'-[0-9]{3,6}', c)[0][1])
	if l > m:
	    m = l
	    
    return m

def find_valid_combs(course_database, courses, semester): #possible optimization by implementing combinations algorithm myself? Web says NP-complete?   
    semester_components = []
    for co in courses:
	cd = course_database[co][semester]
	lectures = []
	labs = []
	for p in cd:
	    t = p['Type']
	    if t == 'Lecture':
		p['Course'] = co 
		lectures.append(p)
		
	    elif t == 'Laboratory':
		p['Course'] = co
		labs.append(p)
		
	if len(lectures) > 0:
	    semester_components.append(lectures)
	if len(labs) > 0:
	    semester_components.append(labs)
	
    combs = []
    gen_combs( semester_components ,combs)
    valid_combs = []
    for c in combs:
	#print c
	v = test_schedule(c)
	if v:
	    valid_combs.append(c)
	    
    return valid_combs
    
    #combo doenst neccesarily have to be 5 courses cuz of labs, etc
    
def gen_combs(components, combs ,prefix = []):
    if len(components) == 0:
	combs.append(prefix[::])
    else:	
	for p in components[0]:
	    prefix.append(p)
	    gen_combs(components[1:], combs, prefix)
	    prefix.pop()

def test_schedule(combo):
    sched = {'M':[],'T': [],'W':[],'R':[],'F':[] }
    for course in combo:
	days = course['Days'].replace("TR", "R")
	time = convert_time(course['Time'])

	for d in days:
	    try:
		valid = try_time(d, time, sched)
		if valid == False:
		    return False
	    except Exception,e :
		#print str(e)
		return False
    return True

def convert_time(s):
    r_times = []
    
    zones = re.findall(r'AM|PM',s)
    hours = re.findall(r'[0-9]{2}:' , s)
    minutes = re.findall(r':[0-9]{2}', s)
    
    try:
	for i in range(2):
	    if zones[i] == 'PM':
		r_times.append( (int(hours[i][:2]) + 12)*60 + int(minutes[i][1:]) )
	    else:
		r_times.append( (int(hours[i][:2]) + 12)*60 + int(minutes[i][1:]) )
    except:
	pass
    return r_times

def try_time(day, time, sched):
    for t in sched[day]:
        if collision(time, t) == True:
            return False

    
    sched[day].append(time)

    return True

def collision(time, t): #time[1] must be greater than or equal to t[0], if time[1] is greater, need to check 
    if (time[1] > t[0] and time[1] <= t[1] ) or (time[1] > t[1] and time[0] < t[1]):  
        return True
    else:
        return False

def load_test_graph():
    with open("../data/program_graph.txt") as f:
	data = json.load(f)
	return data['Major_Physiology_and_Mathematics_(77_credits)']


g = load_test_graph()
ps = gen_possible_schedules(g,'fall')
optimize(ps[0],ps[1], ps[2], 'quality')
print found, not_found
