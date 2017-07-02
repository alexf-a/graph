def has_eulerian_path(G):
    '''Return whether Graph G has a Eulerian path'''
    if isinstance(G, UGraph):
        if not G.is_connected():
            return False
        count = 0
        for v in G.vertices():
            if len(G.vertices(v))%2 != 0:
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
        for v in G.vertices():
            if len(G.vertices(v))%2 != 0:
                return False
        return True
    elif isinstance(G, DGraph):
        pass #Needs implementation
    return False 

def eulerian_circuit(G, v):
    '''Return a Eulerian circuit list beginning at vertex v, if one exists.'''
    result = []
    if not has_eulerian_circuit(G):
        return result
    return result
    
        
            
        
        
    
                   
            
        