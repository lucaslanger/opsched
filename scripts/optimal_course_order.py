import itertools
import re
import json

def gen_possible_schedules(course_graph): # should also take, semester that one starts from and completed courses
    schedules = {}
    
    course_graph = course_graph['graph'] # what..

    f_candidates = determine_candidates(course_graph,'fall',{})

    f_comb_dict = {}
    f_combs = list(itertools.combinations(f_candidates, 5) )
    for fc in f_combs:
	f_comb_dict[fc] = find_valid_combs(course_graph, fc, 'fall')
	
    	if len(f_comb_dict[fc]) > 0: 
	    seen_courses = {}
	    for c in fc:
		seen_courses[c] = True
		
	    #kindof a recursive step, but since only 2 cases and need to track schedules, wrote it out again	

	    w_candidates = determine_candidates(course_graph, 'winter' ,seen_courses)

	    w_comb_dict = {}
	    w_combs = list(itertools.combinations( w_candidates, 5 ) )
	    for wc in w_combs:
		w_comb_dict[wc] = find_valid_combs( course_graph, wc, 'winter' )
		if len( w_comb_dict[wc] > 0):
		    if schedules.has_key( fc ):
			schedules[fc].append( wc )	
		    else:
			schedules[fc] = [wc]
			
    return schedules, f_comb_dict, w_comb_dict

def determine_candidates(course_graph, semester ,completed):
	cands = []
	mc = max_completed(completed)

	for key in course_graph.keys():
	    t = course_graph[key].has_key('Timing')
	    if t:
		o = course_graph[key]['Timing'].has_key(semester)
	    else:
		o = False
		
	    #print o	
	    if key not in completed and o:
		possible = True
		for p in course_graph[key]['prereq']:
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

def find_valid_combs(course_graph, courses, semester): #possible optimization by implementing combinations algorithm myself? Web says NP-complete?   
    semester_components = []
    for co in courses:
	cd = course_graph[co]['Timing'][semester]
	lectures = []
	labs = []
	for p in cd:
	    t = p['Type']
	    if t == 'Lecture':
		lectures.append(p)
		
	    elif t == 'Laboratory':
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
    sched = {'M':[],'T': [],'W':[],'TR':[],'F':[] }
    for course in combo:
	print course
	days = course['Days']
	time = convert_time(course['Time'])

	for d in days:
	    valid = try_time(d, time, sched)
	    if valid == False:
	        return False
    return True

def convert_time(s):
    r_times = []
    times = s.split("-")
    zones = re.findall(r'AM|PM',s)
    for t in times:
	hours = re.findall(r'[0-9]{2}:' , t)
	minutes = re.findall(r':[0-9]{2}', t)
	
	for i in range(2):
	    if zones[i] == 'PM':
		r_times.append( (int(hours[i][:2]) + 12)*60 + int(minutes[i][1:]) )
	    else:
		r_times.append( (int(hours[i][:2]) + 12)*60 + int(minutes[i][1:]) )
		
    return r_times
    

def try_time(day, time, sched):
    for t in sched[day]:
        if collision(time, t) == True:
            return False

    return True

def collision(time, t): #time[1] must be greater than or equal to t[0], if time[1] is greater, need to check 
    if (time[1] > t[0] and time[1] <= t[1] ) or (time[1] > t[1] and time[0] < t[1]):  
        return True
    else:
        return False

def load_test_graph():
    with open("../data/program_graph.txt") as f:
	data = json.load(f)
	return data['Honours_Planetary_Sciences__(81_credits)']


g = load_test_graph()
ps = gen_possible_schedules(g)
keys = ps.keys()
sample = ps[keys[0]]
print keys[0], sample[0]