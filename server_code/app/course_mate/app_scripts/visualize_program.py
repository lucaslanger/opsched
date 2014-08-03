def visualize_old(program_title, program_graph):
        
    with open("visual_test.dot", "w") as f3:
        graph = program_graph[program_title]
        f3.write("digraph G {\n")
        
        for v in graph:
            prereq = graph[v]['prereq']
            
            for p in prereq:
                if p.replace("_","-") in graph: # the replacement is a temporary bugfix that occured because of previous improper formatting in build_course_graph (prereq section)
                    f3.write("\t" + p.replace("-","_") + " -> " + v.replace("-","_") + ";\n")
                    print p
                else:
                    print "Excluded " + p
            
        f3.write('}')


def visualize(program_title, program_graph, course_database):
    edges = []
    nodes = []
    ids = {}
    p = program_graph[program_title]
    counter = 1

    for v in p:
        if v in course_database:
            ids[v] = counter
            nodes.append({'id':counter,'label':v})
            counter += 1
       
    for v in p:
        if v in course_database:
            for pre in course_database[v]['prereq']:
                if pre in p:
                    edges.append( {'from': ids[pre], 'to': ids[v], 'value': 30 })

    return nodes,edges
#visualize("Honours_Applied_Mathematics_(60_credits)")
