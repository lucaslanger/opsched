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
            print name
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
        
    with open("teacher_data.txt", "w") as f:
        json.dump(teachers, f)
        
find_teacher()