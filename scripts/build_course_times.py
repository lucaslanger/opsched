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
		add_data("../course_times_csv/f2014/" + f + "_f2014.csv", "f2014", course_data)
		add_data("../course_times_csv/w2015/" + f + "_w2015.csv", "w2014", course_data)

	with open("../data/course_times.txt", "w") as f:
		#print course_data.keys()
		json.dump(course_data, f)

def add_data(location, semester ,course_data):

	with open(location, "r") as f:
		r = csv.reader(f, delimiter=',')
		for data in r:
		
			if len(data) > 10:
				course = data[1] + "-" + data[2]

				if re.findall("[A-Z]+-[0-9]+.+",course) != []:
					days = remove_accents(data[7])
					time = remove_accents(data[8])
					try:
						instructor = remove_accents(data[13])
					except: 
						instructor = unicode(data[13], errors='ignore')
					
					status = remove_accents(data[16])
					course_data[ course + "_" + semester ] = {"Days": days, "Time": time, "Instructor": instructor, "status": status} 
					

build_course_times()