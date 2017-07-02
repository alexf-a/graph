class Graph:
    '''An abstract data structure representing a Graph.'''
    def __init__(self, dct):
        self._dct = dct
    
    def edges(self, v=None):
        '''Return a set of all edges that touch vertex v. 
           Includes all edges in this Graph if v is None.
                   
          args:
          v -- str of v's contents
       '''  
        raise NotImplementedError("Requires subclass implementation")
  
    def vertices(self, v=None):
        '''Return a set of all vertices in this Graph that are adjacent to vertex v. 
         Includes all vertices if v is None:
         
         args:
         v -- str of v's contents
         '''  
        raise NotImplementedError("Requires subclass implementation")
      
        

class UGraph:
    ''' A data structure representing an undirected graph.'''
    def __init__(self, dct):
        ''' Initialize this UGraph with a dictionary dct '''
        self._dct = dct
    
    def edges(self, v=None):
        '''Return a set of all edges that touch vertex v. 
           Includes all edges in this UGraph if v is None.
           
           args:
           v -- str of v's contents
        '''
        res = []
        if v:
            ajdacents = self._dct[v]
            for a in adjacents:
                res.append((v, a)) 
        else:
            #for each key, append (key, adj) if (adj, key) not already there
            for vtx in self._dct.keys():
                for adj in self._dct[vtx]:
                    if (adj, vtx) not in res:
                        res.append((vtx, adj))
        return set(res)
    
    def vertices(self, v=None):
        '''Return a set of all vertices in this UGraph that are adjacent to vertex v. 
           Includes all vertices if v is None:
           
           args:
           v -- str of v's contents
        '''
        res = []
        if v:
            return set(self._dct[v])
        else:
            return self._dct.keys()
        
    def is_connected(self):
        '''Return whether this UGraph is connected.'''
        #Pick the first vertex and perform BFS. Return true iff BFS touches every node
        visited = []
        q = [self.vertices()[0]]
        while q:
            curr = q.pop(0)
            visited.append(curr)
            for adj in self.vertices(q):
                if adj not in visited:
                    q.append(adj)
        if set(visited) == set(self.vertices()):
            return True 
        else:
            return False
        
        


        
        