from bs4 import BeautifulSoup
import json
import re

def build_program_graphs():
    find_graph_by_program = {}
    
    with open("../data/program_titles.txt", "r") as f:
        titles = json.load(f)
        
    with open("../data/course_database.txt","r") as f2:
        course_graph = json.load(f2)
        
    for title in titles:
        with open("../programs/" + title) as f:
            html = f.read()    
    
        soup = BeautifulSoup(html)
        
        #url =  ... add a url for every program?
        
        courses = []
        courses_li = soup.find_all(class_='program-course-title')
    
        for c in courses_li:
            try:
                name = re.findall(r'[A-Z]{2,6} [0-9]{2,6}[a-zA-Z]*[0-9]*', c.text)[0]
                courses.append(name.replace(' ','-'))   
                    
            except:
                print 'Something went wrong -->   ' + c.text
                print
                
        find_graph_by_program[ title ] = {"graph": make_program_graph(courses, course_graph)}
        
    with open("../data/program_graph.txt" , "w") as f:
        print "Successfully wrote out program graphs"
        json.dump(find_graph_by_program, f)
    
def make_program_graph(courses, cg):
    graph = {}
    
    for c in courses:
        try:
            graph[c] = cg[c]
        except:
            print c
    return graph

build_program_graphs()