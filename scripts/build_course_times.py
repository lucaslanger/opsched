import csv
import json
import re
import unicodedata

def remove_accents(s):
	nkfd_form = unicodedata.normalize('NFKD', unicode(s.decode("latin-1")  ))
	return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

def build_course_times():
	faculties = ['arts',
				'continuing',
				'dentistry',
				'engineering',
				'education', 
				'environmentsci',
				'graduate',
				'law',
				'management',
				'medecine',
				'music',
				'nursing',
				'physocc',
				'postdoc',
				'religious',
				'science'
				]

	course_timing = {}
	teacher_names = {}
	for f in faculties:
		add_data("../course_times_csv/f2014/" + f + "_f2014.csv", "fall", course_timing, teacher_names)
		add_data("../course_times_csv/w2015/" + f + "_w2015.csv", "winter", course_timing, teacher_names)

	with open("../data/course_graph.txt", "r") as f:
		course_graph = json.load(f)

	course_database = {}
	for key in course_graph:
		if key in course_timing:
			course_database[key] = dict(course_graph[key].items() + course_timing[key].items() )
			#print course_timing[key].keys()
		else:
			course_database[key] = course_graph[key]
			#print "Not offered: " + str(key)

	with open('../data/course_database.txt','w') as f:
		json.dump(course_database,f)
		
	with open('../data/teacher_names.txt', 'w') as f:
		json.dump(teacher_names,f)

def add_data(location, semester ,course_timing, teacher_names={}):
	#c = 0
	with open(location, "r") as f:
		r = csv.reader(f, delimiter=',')
		for data in r:
		
			if len(data) > 10:
				course = data[1] + "-" + data[2]

				if re.findall("[A-Z]+-[0-9]+.+",course) != []:
					days = data[7]
					time = data[8]
					section = data[3]
					typeofclass = data[4]
					status = data[16]
					crn = data[0]
					
					instructors = [i for i in remove_accents(data[13]).split(',')]
					
					for i in instructors:
						#if i == 'TBA':
							#c+=1
							#print c, course
						teacher_names[i] = True
					
					
					if status == 'Active':# any other kinds?
						
						info = {
							'Crn' : crn,
							'Type':typeofclass, 
							'Section': section,
							"Days": days,
							"Time": time,
							"Instructor": instructors,
							"Status": status
						}
						#print info

						if course_timing.has_key(course) == False:
							course_timing[course] = {semester: [info] }
						elif course_timing[course].has_key(semester) == False:
							course_timing[course][semester] = [info]
						else:
							course_timing[course][semester].append(info)
		
build_course_times()