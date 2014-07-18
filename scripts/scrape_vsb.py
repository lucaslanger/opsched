import requests

def check_schedule(year, season, courses):
    res = requests.get("https://vsb.mcgill.ca/results.jsp", params= {
        'session_201409':1,
        'code_number': '',
        'remove_course': '',
        'view_details': '',
        'course_0_0': 'COMP-250',
        'sa_0_0': 'tty',
        'dropdown_0_0': 'al',
        'td_0_0_1': 201409,
        'cams': 'all',
        'tip': '3',
        'pins': '',
        'sf': 'ffftimeinclass',
        'bbs': '',
        'submit_action': 'search'
        })
    with open("vsbtest.html", "w") as f:
        f.write( res.text )
        
check_schedule('','','')