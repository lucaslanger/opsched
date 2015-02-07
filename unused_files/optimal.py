import itertools
import re
import json

found = 0
not_found = 0

def gen_possible_schedules(course_database, program, semester='fall', load = 5): # should also take, semester that one starts from and completed courses
    
    if semester == 'fall':
	schedules = {}
	f_comb_dict = {}
	w_comb_dict = {}
    
	f_candidates = determine_candidates(course_database, program, 'fall',{})
	print len(f_candidates)
	print f_candidates
	
	
	f_combs = list(itertools.combinations(f_candidates, min(fload,len(f_candidates) ) ) )

	for fc in f_combs:
	    f_comb_dict[fc] = find_valid_combs(course_database, fc, 'fall')
	    
	    if len(f_comb_dict[fc]) > 0: 
		seen_courses = {}
		for c in fc:
		    seen_courses[c] = True
		    
		#kindof a recursive step, but since only 2 cases and need to track schedules, wrote it out again	
    
		w_candidates = determine_candidates(course_database, program, 'winter' ,seen_courses)
		#print len(w_candidates)
    
		w_combs = list(itertools.combinations( w_candidates, wload ) ) #min of the two, like with fall?
		for wc in w_combs:
		    w_comb_dict[wc] = find_valid_combs( course_database, wc, 'winter' )
		    if len( w_comb_dict[wc]) > 0:
			if schedules.has_key( fc ):
			    schedules[fc].append( wc )
			    #print wc	
			else:
			    schedules[fc] = [wc]
			    	    
	return schedules, f_comb_dict, w_comb_dict
    
    elif semester == 'winter':
	schedules = {}
	
	w_candidates = determine_candidates(course_database,'winter',{})
	
	w_combs = list(itertools.combinations(w_candidates, wload ) )
	for wc in w_combs:
	    schedules[wc] = find_valid_combs(course_database, wc, 'fall')
	    
	

def optimize(database,schedules, fcomb, wcomb, ratings, filt3r ):
    optimal_score = 0
    optimal = None
    
    low = None
    
    for fc in schedules:
	for i in fcomb[fc]:
	    f_score, teacher_course_f, f_entries = get_score(i, ratings, filt3r)
	    for wc in schedules[fc]:
		for j in wcomb[wc]:
		    w_score, teacher_course_w, w_entries = get_score(j, ratings, filt3r)
		    try:
		    	total = (f_score + w_score) / (w_entries + f_entries )
		    except:
		    	total = 0
		    #print total

		    if total > optimal_score:
			optimal = [teacher_course_f, teacher_course_w]
			optimal_score = total
			
		    elif low == None or total < low:
			low = total
			
    tmp = []

    #for c in optimal[0]:
    #	sections = database[c[0]]['fall']
    #	for s in sections:
    #	    #cprint c[1], s['Crn']
    #	    if c[1] == s['Crn']:
    #		
    #		tmp.append(s)
    #print database['MATH-242']['fall']
    #print tmp[0].keys()
    #print [i['Course'] for i in tmp]
    #print test_schedule(tmp)
    #print optimal_score, low
    #print get_vsb_url(database, optimal[0], 'fall')

    return optimal	
	
def get_score(courses,ratings, filt3r):
    global found, not_found
    filter_dict = {'hotness': -1, 'easyness': -2, 'quality': -3}
    total = 0
    entries = 0 
    data = []
    for c in courses:
	instructors = c['Instructor']
	course, typ3 = c['Course'], c['Type']
	crn = c['Crn']

	score = 0.0
	known_teachers = 0.0
	
	#print ratings.keys()
	for i in instructors:
	    #print i, ratings.has_key(i)
	    if re.findall('TBA', i) != None and ratings.has_key(i):
		try:
		#score = float(ratings[instructor][ filter_dict[filt3r] ])
		    
		    score += float(ratings[i][2])
		    #data.append( (course, typ3, instructor, score) )
		    known_teachers += 1 
		    found += 1
		except Exception,e:
		    print str(e)
	    else:
	     
	        not_found+=1
		
		#total += 2.0
	
	if known_teachers != 0:
	    avg = score/known_teachers
	    data.append( (course, crn, typ3 , instructors, avg))
	    total += avg
	    entries += 1
	else:
	    data.append( (course, crn, typ3 , instructors, 'N/A'))
    	    
    return total, data, entries

def get_vsb_url(database,optimal,semester):
    if semester == 'fall':
	semnumber = '201409'
    url = "https://vsb.mcgill.ca/results.jsp?session_" + semnumber + "=1"
    
    o = optimal # shorten length of lines below
    seen_courses = {}
    l_seen = 0
    for i in range(len (o)):
	#print seen_courses
	if o[i][0] not in seen_courses:
	    seen_courses[o[i][0]] = True
	    si = str(l_seen)
	    sa_code, course_parts = getsa(database,o[i][0], semester)
	    dropdown_code = 'us_' + o[i][0] + "-" + semnumber + "-" + getdd(o[i], o)
	    addon = '&course'+"_"+ si+"_0="+str(o[i][0])+'&'+'sa' + "_"+ si+"_0="+ sa_code+'&dropdown'+ "_"+ si+"_0="+ dropdown_code
	    url += addon
	    l_seen += 1
	
    end = "&sf=ffftimeinclass&submit_action=search"
    url += end
    
    return url

def getsa(database,course,semester):
    sections = database[course][semester]

    lecs = 0
    labs = 0
    tut = 0
    for s in sections:
	typ = s['Type']
	if typ == 'Lecture':
	    lecs += 1
	elif typ == 'Laboratory':
	    labs += 1
	elif typ == 'Tutorial':
	    tut += 1
	else:
	    print typ
	    
    l = max(labs, lecs, tut)
    p = (1 if labs > 0 else 0) + (1 if tut > 0 else 0) + (1 if lecs>0 else 0)
    
    if l == 1:
	return 'tm',p
    elif l == 2:
	return 'tty',p
    elif l == 3:
	return 'tttk',p
    elif l == 4:
	print course, " 4 sections "
    elif l == 5:
	return 'ttttti',p

def getdd(course, optimal):
    s = ''
    for o in optimal:
	if o[0] == course[0]:
	    if s != '':
		s = s + "-" + o[1]
	    else:
		s = o[1]
    return s


'''	
def process_name(name):
    try:
        parts = re.findall('[A-Za-z]{3,50}', name)
        new_name = parts[0] + " " + parts[-1]
        return new_name
    except:
        print "Problem: " + name
        return name
'''    


def determine_candidates(course_database, program ,semester ,completed):
	cands = []
	mc = max_completed(completed)

	for key in program:
	    t = course_database[key].has_key(semester)
	    
	    if key not in completed and t and re.findall('-[0-9]+',key)[0][1] != '1':
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
			
		    if pl != None and pl >= 2 and p not in completed and p in program: #ignores prereqs below 100 level
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
	tutorials = [] # do we want this?
	labs = []
	for p in cd:
	    t = p['Type']
	    if t == 'Lecture':
		p['Course'] = co 
		lectures.append(p)
		
	    elif t == 'Laboratory':
		p['Course'] = co
		labs.append(p)
		
	    elif t == 'Tutorial':
		p['Course'] = co
		tutorials.append(p)
		
	if len(lectures) > 0:
	    semester_components.append(lectures)
	if len(labs) > 0:
	    semester_components.append(labs)
	if len(tutorials) > 0:
	    semester_components.append(tutorials)
	
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
	#print course['Days']
	days = course['Days']#.replace("TR", "R")
	#print days
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
	return data['Major_Atmospheric_Science_and_Physics_(67_credits)']

def optimal_schedule(course_database, program, ratings, f='quality'):
    ps = gen_possible_schedules(course_database, program)
    #print ps
    o = optimize(course_database, ps[0], ps[1], ps[2],ratings, f)
    
    url = get_vsb_url(course_database, o[0], 'fall')
	
    return o, url


'''
with open('../data/course_database.txt', 'r') as f:
    course_database = json.load(f)
g = load_test_graph()
ps = gen_possible_schedules(course_database, g,'fall')
optimize(course_database, ps[0],ps[1], ps[2], 'quality')
print found, not_found
'''