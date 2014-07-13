import requests
import json
from bs4 import BeautifulSoup
import re

def get_program_pages(start, read_titles=True): # as with scrape courses, possibly add logging
    #faculties = ['science']
    faculties = ['arts']#,'law','engineering','macdonald','basc','continuing','dentistry','education','engineering','environment','desautels','medicine','music']
  
    if read_titles:
        with open("program_titles.txt","r") as f:
            titles = json.load(f)
    else:    
        titles = []
        
    for f in faculties:
    
        fac_url = "http://www.mcgill.ca/study/2014-2015/faculties/" + f + "/undergraduate/programs"
        n=start
        
        while True:
            try:
                html = requests.get(fac_url, params={"page": n} ).text
                soup = BeautifulSoup(html)
            
                failure_message = soup.find('div', {"id":"content-area"}).find("h2")
                if failure_message == None:
                    get_programs_on_page(soup, titles )
                    n+= 1
                else:
                    print "Finished at page " + str(n)
                    break
             
            except Exception,e:
                print "Error on page " + str(n)
                print str(e)
                with open("program_titles.txt","w") as f:
                    json.dump( fast_unique_list(titles), f )
            
        
        with open("program_titles.txt","w") as f:
            json.dump( fast_unique_list(titles), f ) 

def get_programs_on_page(soup, titles):
        
    programs = soup.find_all(class_="title")
    for p in programs:
        link = p.find('a')['href']
        html = requests.get(link).text
        program_soup = BeautifulSoup(html)
        title = program_soup.find('h1').text.replace(' ', '_').replace('/',"_or_")
        print title
        with open("programs/" + title, "w") as f:
            f.write(html.encode('utf-8'))
            titles.append(title)
        
        
def fast_unique_list(li):
    unique = []
    eles = {}
    for e in li:
        if eles.has_key(e) == False:
            eles[e] = True
            unique.append(e)
    return unique
        
        
def find_info_by_program(link):
    #title,courses = find_info_by_program(link)
    #program_graph = make_program_graph(title, courses, course_graph)
    #program_object = {'title':title, 'url':link, 'courses':courses, 'graph':program_graph}
    #program_urls.append(program_object)
    
    
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

get_program_pages(0)