import requests
import json
from bs4 import BeautifulSoup
import re

def get_course_pages(start, readtitles = True): # CHANGES? :instead of printing last_page scraped, use a log file
    
    i = start
    
    if readtitles:
        with open("course_titles.txt","r") as f:
            titles = json.load(f)
    else:
        titles = []
    
    while True:
        try:
            html = requests.get("http://www.mcgill.ca/study/2014-2015/courses/search", params={"page":i}).text
            soup = BeautifulSoup(html)
            failure = soup.find('div', {"id":"content-area"}).find("h2")
            if failure == None:
                courses = soup.find_all(class_="title")
                
                for c in courses: 
                    a = c.find('a')
                    link = a['href']
                    title = re.findall(r'courses/(.+)', link)[0].upper()
            
                    html = requests.get(link).text.encode('utf-8')
                    with open("courses/" + title , "w") as f:
                        f.write(html)
                        titles.append(title)
                        
                    
                i += 1
                print i
            else:
                print "Finished reading at page " + str(i)
                
                with open("course_titles.txt","w") as f:
                    f.write( json.dumps( fast_unique_list(titles) ) )
                break
        
        except:
            with open("course_titles.txt","w") as f:
                f.write( json.dumps( fast_unique_list(titles) ) )    
        
def fast_unique_list(li):
    unique = []
    eles = {}
    for e in li:
        if eles.has_key(e) == False:
            eles[e] = True
            unique.append(e)
    return unique