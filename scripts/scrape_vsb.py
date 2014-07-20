import requests

#code is currently having trouble with second request. Decided to just manually download 30ish files

def scrape_course_times():
	p = {'sel_subj':'AECH'
	}

	s = requests.Session()

	r = s.get('https://horizon.mcgill.ca/pban1/bwckschd.p_disp_dyn_sched')
	d={
		'p_calling_proc':'bwckschd.p_disp_dyn_sched',
		'search_mode_in':'',
		'p_term':201409
	}

	r1 = s.post('https://horizon.mcgill.ca/pban1/bwckgens.p_proc_term_date', data=d )

	d2 = {
			'display_mode_in':'LIST',
			'search_mode_in': '',		
			'term_in':201409,
			'sel_subj':'dummy',
			'sel_day':'dummy',
			'sel_schd':'dummy',
			'sel_insm':'dummy',
			'sel_camp':'dummy',
			'sel_levl':'dummy',
			'sel_sess':'dummy',
			'sel_instr':'dummy',
			'sel_ptrm':'dummy',
			'sel_attr':'dummy',
			'sel_subj':'MATH',
			'sel_crse':'',
			'sel_title':'',
			'sel_schd':'%',
			'sel_from_cred':'',
			'sel_to_cred':'',
			'sel_levl':'%',
			'sel_ptrm':'%',
			'sel_instr':'%',
			'sel_attr':'%',
			'begin_hh':0,
			'begin_mi':0,
			'begin_ap':'a',
			'end_hh':0,
			'end_mi':0,
			'end_ap':'a'
	}
	r2 = s.post('https://horizon.mcgill.ca/pban1/bwckschd.p_get_crse_unsec', data=d2)	
	print dir(s)
	with open("schedtest.html","w") as f:
		f.write(r1.text.encode('utf-8'))	

scrape_course_times()
