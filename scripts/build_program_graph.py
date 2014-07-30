from bs4 import BeautifulSoup
import json
import re

def build_programs():
    find_graph_by_program = {}
    
    with open("../data/program_titles.txt", "r") as f:
        titles = json.load(f)
        
    for title in titles:
        with open("../programs/" + title) as f:
            html = f.read()    
    
        soup = BeautifulSoup(html)
        
        courses = []
        courses_li = soup.find_all(class_='program-course-title')
    
        for c in courses_li:
            try:
                name = re.findall(r'[A-Z]{2,6} [0-9]{2,6}[a-zA-Z]*[0-9]*', c.text)[0]
                courses.append(name.replace(' ','-'))   
                    
            except:
                print 'Something went wrong -->   ' + c.text
                print
                
        find_graph_by_program[ title ] = make_program_graph(courses)
        
    with open("../data/program_graph.txt" , "w") as f:
        print "Successfully wrote out programs"
        json.dump(find_graph_by_program, f)
    
def make_program_graph(courses):
    graph = {"Required","Complementary"}
    
    return courses

build_programs()