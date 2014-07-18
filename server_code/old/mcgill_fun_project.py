import requests
import grequests
import re
import json
import pymongo
from bs4 import BeautifulSoup


def make_request_files():
    #find_prerequisites("http://www.mcgill.ca/study/2014-2015/courses/ansc-551")    
    cg = make_request_docs()
    
    print cg['COMP 250']
    
def load_graph_of_courses():
   jdata = open("course_graph.txt").read()
   data = json.loads(jdata)
   print data['ACCT 351']

def main():    
    faculties = ['science','arts','law','engineering','macdonald','basc','continuing','dentistry','education','engineering','environment','desautels','medicine','music']
   
    programs = {}
    for f in faculties:    
        programs[f] = find_programs_by_faculty(f,course_graph)
        
    
def make_request_docs():
    cg = {}
    requests = grequests.map( (grequests.get("http://www.mcgill.ca/study/2014-2015/courses/search", params={"page":i}) for i in range(386)) )
    counter = 0
    print "Done Requesting"
    
    for r in requests:
        print counter
        counter += 1
        get_courses_on_page( BeautifulSoup(r.text), cg )
 
    return cg
        
        
def get_courses_on_page(soup, course_graph): # courses should have a title, url, prereqs, coreqs, description
    titles = soup.find_all(class_="title")
    for t in titles:
        a = t.find('a')
        link = a['href']
        title = re.findall(r'courses/(.+)', link)[0].upper().replace('-' ,' ')
        #title = re.findall(r'[A-Z]{2,6} [0-9]{2,6}[a-zA-Z]*[0-9]*',soup.find('div',{'id':'content-inner'}).text)[0]
        
        html = requests.get(link).text
        soup = BeautifulSoup(html)
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
            prereq = evaluate_requirements(p)  
            
            if testp:
                print "Word Prequisite showed up twice :(" 
                print lis
            testp = True
            
        elif re.search(r'Corequi',text) != None:
            #p = re.findall(r'[A-Z]{2,6} [0-9]{2,6}[a-zA-Z]{0-4}| or |[E,e]quivalent|[p,P]ermission|,| and |',text)
            p = re.findall(r'[A-Z]{2,6} [0-9]{2,6}[a-zA-Z]*[0-9]*',text)

            coreq = evaluate_requirements(p)  
            
            if testc:
                print "Word Corequisite showed up twice :(" 
                print lis
            testc = True
    
    return prereq,coreq 
        
def evaluate_requirements(req_exp): #needs fix
    choices = []
    curr = []
    for v in req_exp:
        if re.search(r'[A-Z]{2,6} [0-9]{2,6}[a-zA-Z]*[0-9]*',v) != None:
            curr.append(v)
        elif v != " or ":
            if len(curr) != 0:
                choices.append(curr)
            choices.append([v])
        else:
            if len(curr) != 0:
                choices.append(curr)
                curr = []
            
    if len(curr) != 0:
        choices.append(curr)
      
    return choices                
    
    
def find_description(soup):
    desc = soup.find('div', {'id':"content-area"}).find(class_="content").find('p').text
    colon = desc.find(':')    
    d = desc[colon+1:]
    return d
    
    
#find list of urls corresponding to mcgills different programs!    
    
def find_programs_by_faculty(f, course_graph): 
    u = []
    fac_url = "http://www.mcgill.ca/study/2014-2015/faculties/" + f + "/undergraduate/programs"
    n=0
    while True:

        html = requests.get(fac_url, params={"page": n} ).text
        soup = BeautifulSoup(html)
    
        failure = soup.find('div', {"id":"content-area"}).find("h2")
        if failure == None:
            get_programs_on_page(soup, u, course_graph )
            n+= 1
        else:
            break
        
    return u

def get_programs_on_page(soup, program_urls, course_graph):
    titles = soup.find_all(class_="title")
    for t in titles:
        link = t.find('a')['href']
        title,courses = find_info_by_program(link)
        program_graph = make_program_graph(title, courses, course_graph)
        program_object = {'title':title, 'url':link, 'courses': courses, 'graph':program_graph}
        program_urls.append(program_object)
        
        
def find_info_by_program(link):
    html = requests.get(link).text
    soup = BeautifulSoup(html)
    
    title = soup.find('h1').text
    
    courses_li = soup.find_all(class_='program-course-title')
    courses = []
    for c in courses_li:
        name = re.findall(r'[A-Z]{2,6} [0-9]{2,6}[a-zA-Z]*[0-9]*', c.text)[0]
        if name != None:
            courses.append(name)
        else:
            print 'Something went wrong -->   ' + c.text 
               
    return title,courses
    
def make_program_graph(courses, cg):
    graph = {}
    for c in courses:
        graph[c] = cg[c]
        
    return graph
    
def pygraph_to_dot(title, graph):
    f = open(title+".dot",'w')
    f.write("digraph G {\n")
    
    for key in graph:
        for p in graph[key]:
            f.write("\t"+ p + " -> " + key + ";\n")
    
    f.write("}")
    f.close()    
    
#pygraph_to_dot("testgagag", {"hi":["bye"]})
make_request_files()

