def get_vsb_url(database,o,semester='fall'):
    if semester == 'fall':
	semnumber = '201409'
    url = "https://vsb.mcgill.ca/results.jsp?session_" + semnumber + "=1"
    
    seen_courses = {}
    l_seen = 0
    for i in range(len(o)):
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
        return 'ttttw',p
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