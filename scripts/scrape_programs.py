import requests
import json
from bs4 import BeautifulSoup
import re

def get_program_pages(start, read_titles=False): # as with scrape courses, possibly add logging
    #faculties = ['science']
    faculties = ['arts','law','engineering','macdonald','basc','continuing','dentistry','education','engineering','environment','desautels','medicine','music']
  
    if read_titles:
        with open("../data/program_titles.txt","r") as f:
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
                with open("../data/program_titles.txt","w") as f:
                    json.dump( fast_unique_list(titles), f )
            
        
        with open("../data/program_titles.txt","w") as f:
            json.dump( fast_unique_list(titles), f ) 

def get_programs_on_page(soup, titles):
        
    programs = soup.find_all(class_="title")
    for p in programs:
        link = p.find('a')['href']
        html = requests.get(link).text
        program_soup = BeautifulSoup(html)
        title = program_soup.find('h1').text.replace(' ', '_').replace('/',"_or_")
        print title
        with open("../programs/" + title, "w") as f:
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
        

get_program_pages(0)