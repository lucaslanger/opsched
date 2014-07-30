import requests
from bs4 import BeautifulSoup
import re
import json

def scrape_rmp():
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
            names = possiblenames(name)
            
            link = "http://www.ratemyprofessors.com/ShowRatings.jsp?" + re.findall(r'tid=[0-9]+', str( r.find(class_="profName") ) )[0]
            dept = r.find(class_="profDept").text
            rating = r.find(class_="profAvg").text
            diff = r.find(class_="profEasy").text
            hotness = r.find(class_="profHot").text
            
            for p in names:
                teachers[p] = (link, dept, rating, diff, hotness)
            
        c = c + 1    
        html = requests.get("http://www.ratemyprofessors.com/SelectTeacher.jsp", params= {"sid": 1439, "pageNo": c} )
        soup = BeautifulSoup(html.text)
        failure = soup.find('h3', {'id': 'heading'} )
        
    with open('../data/rmp_data.txt' ,'w') as f:
        json.dump(teachers,f)
        

def possiblenames(name):
    possibilities = []
    pieces = name.split(',')
    try:
        first_name = re.findall(r'[a-zA-Z]+', pieces[1])
        last_name = pieces[0]
        first_name_initials = [p[0].upper() for p in first_name]
        
        possibilities = dynamic_naming('',first_name,first_name_initials, last_name)
        return possibilities
    
    except:
        print "Problem " + name
        return [name]
    
def possiblenames2(n):

    first_name = re.findall(r'[a-zA-Z]+', n)
    last_name = first_name.pop()
   
    try:
        first_name_initials = [p[0].upper() for p in first_name]
        
        possibilities = dynamic_naming('',first_name,first_name_initials, last_name)
        return possibilities
    
    except:
        print "Problem2 " + n
        return [n]

def dynamic_naming(s,o1, o2, e):
    #either name has o1 and no o2 or o2 and no o1 or has neither
    
    if len(o1) == 1 and len(o2) == 1:
        if s!='':
            return [s+ " " + o1[0] + " " + e,
                    s + " " + o2[0] + " " +  e,
                    s + " " + e]
        else:
            return [o1[0] + " " + e,
                    o2[0] + " " + e]
        
    else:
        t1=  o1.pop(0)
        t2 = o2.pop(0)
        start = s + " " if s!= '' else ''
        p1 = dynamic_naming(start + t1, o1, o2, e)
        p2 = dynamic_naming(start + t2, o1, o2, e)
        p3 = dynamic_naming(start , o1, o2, e)
        return p1 + p2 + p3
    
    

def manual_search(t_name):
    formatted_name = t_name.replace(" ", "+")
    r = requests.get('http://www.ratemyprofessors.com/solr/interim.jsp?select?facet=true&q=' +
                    formatted_name + '&facet.field=schoolname_s&facet.field=teacherdepartment_s&facet.field=schoolcountry_s&facet.field=schoolstate_s&facet.limit=50&rows=20&facet.mincount=1&json.nl=map&fq=content_type_s%3ATEACHER&wt=json')
                    
    data = r.json()
    entries =  data['response']['docs']
    for e in entries:
        if e['schoolid_s'] == '1439':
            link = 'http://www.ratemyprofessors.com/ShowRatings.jsp?tid=' + re.findall(r'[0-9]+',e['id'])[0]
            dept = e['teacherdepartment_s']
            rating = e['averageratingscore_rf']
            diff = e['averageeasyscore_rf']
            hotness = e['averagehotscore_rf']
            stats = (link, dept, rating, diff, hotness)
            name = e["teacherfullname_s"]
            print name, t_name
            return stats
    return None
    

# was thinking of implementing sequence alignment type solution, but abbreviations could cause problems + need to do it a linear number of times --> slow as hell, manual search just easier
# seq align is n^2 so about 100 * 2000 -> number of teachers ... would need to do this 1000 times..
def manual_searchrARRGGG(t_name): 
    r = requests.get('http://ajax.googleapis.com/ajax/services/search/web', params=
                     {
                        'v': '1.0',
                      'q' : t_name 
                     }
                     ).text
    with open("manualtest.txt",'w') as f:
        f.write(r.encode('utf-8'))
        
        ## google rages about requests...

def test():
    c1,c2 = 0,0
    with open("../data/rmp_data.txt") as f:
        rmpdata = json.load(f)
    with open('../data/teacher_names.txt', "r") as f:
        teacher_data = {}
        teachers = json.load(f)
        for key in teachers:
            found = False
            namecombs = possiblenames2(key)
            for p in namecombs:
            
                if rmpdata.has_key(p):
                    teacher_data[key] = rmpdata[p]
                    break
                
                        
            if found:
                c1 += 1
                
           
             
            else: # this extra process should kill off about 100 of the misses! 4%
                '''
                combs = [namecombs[i] for i in range(len(namecombs)) if i%6==0] #most of the fixes are either 0 or 6
                for p in combs :
                    try:
                        m = manual_search(p)
                        if m:
                            found = True
                            t_found[p] = m
                            break
                    except:
                        pass
                        
                if found:
                    c1 +=1
                else:
                '''
                print key
                c2 +=1
            
            
    with open('../data/teacher_data.txt','w') as f:
        json.dump(teacher_data,f)
    
    
#scrape_rmp()
#manual_search('michael langer')
test()