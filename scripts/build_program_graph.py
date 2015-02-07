from bs4 import BeautifulSoup
import json
import re
import math
import unicodedata

def remove_accents(s):

    nkfd_form = unicodedata.normalize('NFKD', s  ) 
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

def fast_unique(li):
    seen = {}
    unique = []
    for l in li:
        if seen.has_key(l) == False:
            unique.append(l)
            seen[l] = True
            
    return unique
    

def build_programs():
    find_graph_by_program = {}
    
    with open("../server_code/app/scheduling_app/app_data/program_titles.py", "r") as f:
        s = f.read()
        start = s[:s.index("=") + 1]
        s = s[s.index("=")+1:]
        titles = json.loads(s)
        
    #titles = [remove_accents(t) for t in titles]
    #with open("../server_code/app/scheduling_app/app_data/program_titles.py", "w") as f:
     #   f.write(start + " " + json.loads(titles) )
        
    for title in titles:
        with open("../programs/" + title) as f:
            html = f.read()    
    
        soup = BeautifulSoup(html)
        
        #courses = {}
        sections = []
        headers = soup.find_all('h4')
        
        for h in headers:
            headertext= h.text
            section = []
            
            if re.search(r'.{3,100}', h.text ):
                #print h.text
                for sibling in h.next_siblings:
                    s = repr(sibling)
                    #print s
                    if len(re.findall(r'program-set', s)) > 0:
                        courses = sibling.find_all('a')
    
                        for co in courses:
                            try:
                                co = re.findall(r'[A-Z]{2,6} [0-9]{2,6}[a-zA-Z]*[0-9]*', co.text)[0]
                            except:
                                continue
                            co = co.replace(" ", "-")
                            
                            section.append(co)
                                
                            
                    elif re.search(r'<h4>.{3,100}</h4>', s ) != None:
                        #print s
                        break
             
            #print headertext, section[headertext]            
            if len(section) > 0:
                sections.append([headertext, section])
        
        if title != remove_accents(title):
            print title
        title = remove_accents(title.replace("_"," "))#.replace("\u","- ")
        
        find_graph_by_program[ title ] = sections
        
        with open("../server_code/app/scheduling_app/app_data/program_graph.py" , "w") as f:
            print "Successfully wrote out programs"
            f.write("program_graph = " + json.dumps(find_graph_by_program) )
            #json.dump(find_graph_by_program, f)
            #print len(find_graph_by_program)
        
        
        
        # below is the non categorical version

        '''
        if courses == []: #if required wasnt found, take the first set of courses listed
            
            try:
                ncredits = re.findall('[0-9]+_credit', title)[0]
                creds = int(ncredits[:ncredits.index('_')])
            except:
                creds = 90
            coursenum = math.ceil(creds/3.0)
            #print coursenum    

            headers = soup.find_all('h4')
            loop = True
            for h in headers:
                if loop:
                    for sibling in h.next_siblings:
                            s = repr(sibling)
                            if re.search(r'program-set', s ) != None:
                                for c in re.findall(r'[A-Z]{2,6} [0-9]{2,6}[a-zA-Z]*[0-9]*', s):
                                    if len(courses) < coursenum:
                                        c = c.replace(" ","-")
                                    
                                        courses.append(c)
                                    else:
                                        loop = False
           
        '''                         

        '''
        for c in courses_li:
            try:
                name = re.findall(r'[A-Z]{2,6} [0-9]{2,6}[a-zA-Z]*[0-9]*', c.text)[0]
                courses.append(name.replace(' ','-'))   
                    
            except:
                print 'Something went wrong -->   ' + c.text
                print
        '''    


    

build_programs()