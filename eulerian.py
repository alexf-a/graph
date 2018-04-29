import copy
import random
from graph import UGraph
def has_eulerian_path(G):
    '''Return whether Graph G has a Eulerian path'''
    if isinstance(G, UGraph):
        if not G.is_connected():
            return False
        count = 0
        for v in G.nodes():
            if len(G.nodes(v))%2 != 0:
                count+=1
                if count > 2: #Return early if odd degree v's surpasses 2
                    return False
        if count == 0 or count == 2:
            return True
        else:
            return False
            
    elif isinstance(G, DGraph):
        pass #Needs implementation
    return False
    
def has_eulerian_circuit(G):
    '''Return whether Graph G has a Eulerian circuit.'''
    if isinstance(G, UGraph):
        if not G.is_connected():
            return False
        for v in G.nodes():
            if len(G.nodes(v))%2 != 0:
                return False
        return True
    elif isinstance(G, DGraph):
        pass #Needs implementation
    return False 

def eulerian_circuit(G, v):
    '''Return a Eulerian circuit list beginning at vertex v, if one exists.
    
    Uses Hierholzer's algorithm.
    '''
    result = []
    if not has_eulerian_circuit(G):
        return result
    cpy = copy.deepcopy(G)
    result = []
    start = v
    #while all edges have not been used
    while cpy.edges() != set([]):
        q = [start]
        nbr = None
        #looking for a cycle...
        while nbr != start:
            w = q[len(q)-1]
            nbr = random.sample(cpy.nodes(w), 1)[0]
            q.append(nbr)
            cpy.remove_edge(w, nbr)
        
        #join cycle to result, if a previous cycle has been found
        if result != []:
            for i, node in enumerate(result):
                if node == start:
                    p1 = result[0:i]
                    p2 = result[i+1:len(result)]
                    result = p1 + q + p2
                    break
        else:
            result = q
        
                
        #find a node from q with unused edges, if any. Set start to it.
        for node in q:
            if cpy.edges(node) != set([]):
                start = node
                break
    
    return result

        
            
        
if __name__ == '__main__':
    dct = {'A':['B','C'], 'B':['A', 'C'], 'C':['A', 'B']}
    ug = UGraph(dct)
    ug.add_node('D')
    ug.add_node('E')
    ug.add_edge('A', 'E')
    ug.add_edge('E', 'C')
    ug.add_edge('A', 'D')
    ug.add_edge('D', 'C')
    ug.add_node('F')
    ug.add_edge('F', 'D')
    ug.add_edge('F', 'E')
    ug.add_edge('E', 'D')
    print(eulerian_circuit(ug, 'A'))
                   
            
        