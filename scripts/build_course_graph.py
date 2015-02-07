import json
from bs4 import BeautifulSoup
import re
    
def build_graph(read_courses = False):
    with open("../data/course_titles.txt","r") as f:
        titles = json.load(f)
    
    if read_courses:
        with open("../data/course_graph.txt","r") as f:
            course_graph = json.load(f)
    else:        
        course_graph = {}
    
    for title in titles:
        
        try:     
            get_course_info( title, course_graph )
            
        except Exception, e:
            print str(e)
            print "Failed on " + title
            
            with open("../data/course_graph.txt","w") as f:
            	json.dump(course_graph, f)
                break
         
    with open("../data/course_graph.txt","w") as f:
        json.dump(course_graph, f)
        print "Successfully built the graph!"
 
    return course_graph
   
def get_course_info(title, course_graph): # courses should have a title, url, prereqs, coreqs, description
    with open("../courses/"+title, "r") as f:
        soup = BeautifulSoup( f.read() )
        link = 'http://www.mcgill.ca/study/2014-2015/courses/' + title.lower()
        name, credit = find_name(soup) 
        prereq, coreq = find_requisites(soup,title)
        desc = find_description(soup)
        #faculty = find_faculty(soup)
        #offerings = find_offerings(soup)

        data =	{
                "name":name,
                "credit":credit, 
                'url': link,
                "prereq": prereq,
                "coreq":coreq,
                "desc": desc
                }
	course_graph[title] = data

def find_name(soup):
    h1 = soup.find('div',{'id': 'content-inner'} ).find('h1').text
    s = re.findall(r'[0-9]{2,6}[a-zA-Z]*[0-9]* .+', h1 )

    if len(s) > 0:
        s = s[0]
        try:
            name = s[s.index(' ') + 1: s.index("(") -1]
        except:
            name = s[s.index(' ') + 1:]
        
    else:
        name = h1
        print "No match"
    
    creds = re.findall(r'([0-9]+ credit|[0-9]+ CE)', h1)
    if len(creds) > 0:
        creds = creds[0]
    else:
        creds = "N/A"
        
    return name, creds
    
def find_faculty(soup):
    try:
        faculty = soup.find('div', {'id':"content-area"} ).find('a').text 
       
    except Exception, e:
        #print str(e)
        faculty = "Graduate"
    #faculty = faculty[11:]
    return faculty

def find_requisites(soup, title):
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
            
        if re.search(r'Corequi',text) != None:
            #p = re.findall(r'[A-Z]{2,6} [0-9]{2,6}[a-zA-Z]{0-4}| or |[E,e]quivalent|[p,P]ermission|,| and |',text)
            p = re.findall(r'[A-Z]{2,6} [0-9]{2,6}[a-zA-Z]*[0-9]*',text)

            coreq.extend( evaluate_requirements(p) )
    
    '''        
    if len(prereq) == 0:
        try:
            level = re.findall("-[0-9]{3,6}", title)[0][1]
            if int(level) > 2:
                prereq.append("Level" +  level)
        
        except:
            print "Fail: " + title
    '''
    
    return prereq,coreq

def find_description(soup):
    desc = soup.find('div', {'id':"content-area"}).find(class_="content").find('p').text
    colon = desc.find(':')    
    d = desc[colon+1:]
    return d

def find_offerings(soup): # add summer in
    
    teachers_html = soup.find(class_="catalog-instructors").text
    time_html = soup.find(class_="catalog-terms").text
    
    teacher_info = {}
    
    if re.search(r"associated", teachers_html) == None:
        teachers = re.findall(r'[a-zA-Z]+|,', teachers_html)
        teachers = [t for t in teachers if re.match(r"Instructor",t) == None]
        
        teacher_queue = []
        name = ''
        
        for t in teachers:
            if re.search("Fall",t) != None:
                name = process_name(name)
                #print name
                if teacher_info.has_key('Fall'):
                    teacher_info['Fall'].append(name)
                else:
                    teacher_info['Fall'] = [name]
                
                for n in teacher_queue:                
                    teacher_info['Fall'].append(n)
                teacher_queue = []
                name = ''
                    
            elif re.search("Winter",t) != None:
                name = process_name(name)
                #print name
                if teacher_info.has_key('Winter') > 0:
                    teacher_info['Winter'].append(name)
                else:
                    teacher_info['Winter'] = [name]
                
                for n in teacher_queue:
                    teacher_info['Winter'].append(n)
                teacher_queue = []
                name = ''
            else:
                if t == ',':
                    teacher_queue.append( name )
                    name = ''
                else:
                    if name == '':
                        name = t
                    else:
                        name += " " + t
    
    time = re.findall(r'[a-zA-Z]+', time_html)
    
    for ti in time:
        if re.search("Fall", ti) != None and teacher_info.has_key('Fall') == False:
            teacher_info['Fall'] = 'Unassigned'
        elif re.search('Winter', ti) != None and teacher_info.has_key('Winter') == False :
            teacher_info['Winter'] = 'Unassigned'
                   
    return teacher_info

def process_name(name):
    try:
        parts = re.findall('[A-Za-z]{3,50}', name)
        new_name = parts[0] + " " + parts[-1]
        return new_name
    except:
        print "Problem: " + name
        return name
    
def evaluate_requirements(req_exp): #needs fix
    choices = []
    curr = []
    for v in req_exp:
        if re.search(r'[A-Z]{2,6} [0-9]{2,6}[a-zA-Z]*[0-9]*',v) != None:
            curr.append( v.replace(" ", "-") )
        #make conditionals for  (, | and | or | permission | equivalent)
      
    return curr               
    
          
def test():
    with open("../data/course_titles.txt","r") as f:
        titles = json.load(f)
        print len(set(titles))
        print len(titles)
        
   
#test()
build_graph()