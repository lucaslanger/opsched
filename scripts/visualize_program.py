import json

def visualize(program_title):
    
    with open("program_graph.txt", "r") as f1:
        program_graph = json.load(f1)
    with open("course_graph.txt", "r") as f2:
        course_graph = json.load(f2)
        
    with open("visual_test.dot", "w") as f3:
        graph = program_graph[program_title]['graph']
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
     
visualize("Joint_Honours_Mathematics_and_Computer_Science_(75_credits)")