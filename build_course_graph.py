import json
from bs4 import BeautifulSoup
import re
    
def build_graph(read_courses = False):
    with open("course_titles.txt","r") as f:
        titles = json.load(f)
    
    if read_courses:
        with open("course_graph.txt","r") as f:
            course_graph = json.load(f)
    else:        
        course_graph = {}
    
    for title in titles:
        print title
        
        try:     
            get_course_info( title, course_graph )
            
        except Exception, e:
            print str(e)
            print "Failed on " + title
            
            with open("course_graph.txt","w") as f:
                f.write( json.dumps(course_graph) )
                break
                
    with open("course_graph.txt","w") as f:
        f.write( json.dumps(course_graph) )
        print "Successfully built the graph!"
 
    return course_graph
   
def get_course_info(title, course_graph): # courses should have a title, url, prereqs, coreqs, description
    with open("courses/"+title, "r") as f:
        soup = BeautifulSoup( f.read() )
        link = 'http://www.mcgill.ca/study/2014-2015/courses/' + title.lower()
        #title = re.findall(r'[A-Z]{2,6} [0-9]{2,6}[a-zA-Z]*[0-9]*',soup.find('div',{'id':'content-inner'}).text)[0]
        
        prereq, coreq = find_requisites(soup)
        desc = find_description(soup)
        
        course_graph[title] = {"url": link,"prereq": prereq,"coreq":coreq,"desc": desc}

def find_requisites(soup):
    prereq = []
    coreq = []    
    
    testp, testc = False, False
    
    try:
        lis = soup.find(class_="catalog-notes").find_all('li')
    except:
        return [],[]
    
    for l in lis:
        text = l.text
        if re.search(r'Prerequi',text) != None:
            #p = re.findall(r'[A-Z]{2,6} [0-9]{2,6}[a-zA-Z]{0-4}| or |[E,e]quivalent|[p,P]ermission|,| and |',text)
            p = re.findall(r'[A-Z]{2,6} [0-9]{2,6}[a-zA-Z]*[0-9]*',text) 
            prereq.extend( evaluate_requirements(p) )     
            
        elif re.search(r'Corequi',text) != None:
            #p = re.findall(r'[A-Z]{2,6} [0-9]{2,6}[a-zA-Z]{0-4}| or |[E,e]quivalent|[p,P]ermission|,| and |',text)
            p = re.findall(r'[A-Z]{2,6} [0-9]{2,6}[a-zA-Z]*[0-9]*',text)

            coreq.extend( evaluate_requirements(p) ) 
    
    return prereq,coreq 
        
def evaluate_requirements(req_exp): #needs fix
    choices = []
    curr = []
    for v in req_exp:
        if re.search(r'[A-Z]{2,6} [0-9]{2,6}[a-zA-Z]*[0-9]*',v) != None:
            curr.append( v.replace(" ", "_") )
        #make conditionals for  (, | and | or | permission | equivalent)
      
    return curr               
    
    
def find_description(soup):
    desc = soup.find('div', {'id':"content-area"}).find(class_="content").find('p').text
    colon = desc.find(':')    
    d = desc[colon+1:]
    return d

    
def test():
    with open("course_titles.txt","r") as f:
        titles = json.load(f)
        print len(set(titles))
        print len(titles)
        
   

test()
#build_graph()