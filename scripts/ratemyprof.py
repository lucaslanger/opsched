import requests
from bs4 import BeautifulSoup
import re
import json

def find_teacher():
    teachers = {}
    c = 1
    
    html = requests.get("http://www.ratemyprofessors.com/SelectTeacher.jsp", params= {"sid": 1439, "pageNo": c} )
    soup = BeautifulSoup(html.text)
    failure = soup.find('h3', {'id': 'heading'} )
    '''
    with open("ratemyproftest.html","w") as f:
        print "hi"
        f.write(html.text)
    soup = BeautifulSoup(html.text)
    print soup.find(class_="tagcloud_item")
    '''
    while failure == None:
        results = []
        results.extend( soup.find_all(class_="entry even vertical-center") )
        results.extend( soup.find_all(class_="entry odd vertical-center") )
        
        for r in results:
            name = r.find(class_="profName").text
            name = process_name2(name)
            
            link = "http://www.ratemyprofessors.com/ShowRatings.jsp?" + re.findall(r'tid=[0-9]+', str( r.find(class_="profName") ) )[0]
            dept = r.find(class_="profDept").text
            rating = r.find(class_="profAvg").text
            diff = r.find(class_="profEasy").text
            hotness = r.find(class_="profHot").text
            
            teachers[name] = (link, dept, rating, diff, hotness)
            
        c = c + 1    
        html = requests.get("http://www.ratemyprofessors.com/SelectTeacher.jsp", params= {"sid": 1439, "pageNo": c} )
        soup = BeautifulSoup(html.text)
        failure = soup.find('h3', {'id': 'heading'} )
        
    with open("../data/teacher_data.txt", "w") as f:
        json.dump(teachers, f)
        

def process_name2(name):
    parts = re.findall('[A-Za-z]{3,50}', name)
    new_name = parts[-1] + " " + parts[0]
    return new_name


def manual_search(t_name):
    formatted_name = t_name.replace(" ", "%20")
    html = requests.get('http://www.ratemyprofessors.com/solr/interim.jsp?select?facet=true&q=' + formatted_name + '&facet.field=schoolname_s&facet.field=teacherdepartment_s&facet.field=schoolcountry_s&facet.field=schoolstate_s&facet.limit=50&rows=20&facet.mincount=1&json.nl=map&fq=content_type_s%3ATEACHER&wt=json')
                    #    ,params={'query':t_name , 'queryoption':'TEACHER','search_submit':'Search'})
    with open('testfilefile.html','w') as f:
        f.write(html.text)

def test():
    found = 0
    not_found = 0
    with open("../data/teacher_data.txt",'r') as f:
        td = json.load(f)
    with open('../data/teacher_dict.txt','r') as f1:
        cd = json.load(f1)
        for t in cd:
            b = td.has_key(t)
            if b == False:
                not_found += 1
            else:
                found += 1
    print found, not_found
#find_teacher()
manual_search('Michael Langer')
#test()