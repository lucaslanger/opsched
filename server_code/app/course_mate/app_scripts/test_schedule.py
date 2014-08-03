import re

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