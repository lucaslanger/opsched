import itertools

def optimal_course_order(graph): # graph contains courses along with easyness, how good, hotness,
    possible_orderings = gen_possible_orderings(graph)
    
    
def gen_possible_orderings(graph):
    graph_clone = dict(graph)
    
    possibilities = []
    sched = {"fall1":[], "winter1":[], "fall2":[], "winter2":[], "fall3":[], "winter3":[]}
    
    fall1_candidates = []
    for v in graph:
        if v['prereqs'] == []:
            fall1_candidates.append(v)
            
    fall1_combinations = itertools.combinations(fall1_candidates, 5)
    
    for f1c in fall1_combinations:
        for v in f1c:
            
        
    
    
    
