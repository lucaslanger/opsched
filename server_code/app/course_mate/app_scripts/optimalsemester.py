import re

found, not_found = 0,0
    
def optimal(database, schedules, teacher_data, filt='quality' ):
    print len(schedules)
    optimal_score = 0
    optimal = None
    
    low = None
    
    for s in schedules:
	score, schedule_info = get_score(s, teacher_data, filt)
	    
        if score > optimal_score:
            optimal = schedule_info
            optimal_score = score
            
        elif low == None or score < low:
            low = score

    return optimal

def get_score(courses,teacher_data, filt):
    global found, not_found
    filter_dict = {'hotness': -1, 'easyness': -2, 'quality': -3}
    total = 0.0
    entries = 0 
    semester_data = []
    for c in courses:
	instructors = c['Instructor']
	course, typ3 = c['Course'], c['Type']
	crn = c['Crn']

	score = 0.0
	known_teachers = 0.0
	
	for i in instructors:
	    if re.findall('TBA', i) != None and teacher_data.has_key(i):
		try:
		    score += float(teacher_data[i][2])
		    known_teachers += 1 
		    found += 1
		except Exception,e:
		    print str(e)
                    print course
	    else:
	        not_found+=1
                #Give a default rating for unknown teachers?
	
	if known_teachers != 0:
	    avg = score/known_teachers
	    semester_data.append( [course, crn, typ3 , instructors, avg] )
	    total += avg #avg refers to average amounts instructors teaching a single course. For example some courses have 2 instructors teaching the same section
	    entries += 1
	else:
	    semester_data.append( [course, crn, typ3 , instructors, 'N/A'])
    
    try:        
        final_avg = total/entries
    except:
        final_avg = 0
        #print semester_data
    	    
    return final_avg, semester_data
