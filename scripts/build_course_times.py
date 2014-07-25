#coding: utf8

import csv
import json
import re
import unicodedata

def remove_accents(s):
	nkfd_form = unicodedata.normalize('NFKD', unicode(s.decode("utf-8")  ))
	return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

#print remove_accents('François Crépeau')

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

	course_data = {}
	for f in faculties:
		add_data("../course_times_csv/f2014/" + f + "_f2014.csv", "fall", course_data)
		add_data("../course_times_csv/w2015/" + f + "_w2015.csv", "winter", course_data)

	with open("../data/course_times.txt", "w") as f:
		#print course_data['COMP-250']
		json.dump(course_data, f)
		
	return course_data

def add_data(location, semester ,course_data):

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
					try:
						instructor = remove_accents(data[13])
					except: 
						instructor = unicode(data[13], errors='ignore')
					
					info = {
						'Type':typeofclass, 'section': section,
						"Days": days,
						"Time": time,
						"Instructor": instructor,
						"Status": status
					}
					
					if course_data.has_key(course):
						if course_data[course].has_key(semester):
							course_data[course][semester].append(info)
						else:
							course_data[course][semester] = [info]
					else:
						course_data[course] = {semester: [info]}
						
def merge_data(course_times):
	with open('../data/course_graph.txt', 'r') as f:
		course_graph = json.load(f)
	with open('../data/course_database.txt', 'w') as f1:
		c = 0
		for key in course_graph.keys():
			try:
				course_graph[key]['Timing'] = course_times[key]
			except:
				if re.search('COMP',key) != None:
					#print key
					pass
		json.dump(course_graph, f1)
		
ct = build_course_times()
merge_data(ct)