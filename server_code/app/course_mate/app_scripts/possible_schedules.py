import itertools
import re

from test_schedule import *

def gen_possible_schedules(course_database, program, completed={}, semester='fall', load = 5): # should also take, semester that one starts from and completed courses
    
        schedules = []
        
        candidates = determine_candidates(course_database, program, semester, completed)
        combs = list(itertools.combinations(candidates, min(load,len(candidates) ) ) )

	for c in combs:
	    schedules.extend( find_valid_combs(course_database, c, semester) )
    
	return schedules
    
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