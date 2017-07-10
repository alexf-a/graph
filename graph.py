import random
import copy
import random

class Graph:
    '''An abstract data structure representing a Graph.'''
    def __init__(self, dct):
        self._dct = dct
        
    def add_edge(self, v, w):
        '''Add an edge in this Graph from v to w'''
        raise NotImplementedError("Requires subclass implementation")
    
    def remove_edge(self, v, w):
        '''Remove the edge from v to w in this Graph'''
        raise NotImplementedError("Requires subclass implementation")
    
    def add_node(self, v):
        '''Add node v to this Graph'''
        raise NotImplementedError("Requires subclass implementation")
    
    def remove_node(self, v):
        '''Remove node v from this Graph and return its neighbours'''
        raise NotImplementedError("Requires subclass implementation")
        
    
    def edges(self, v=None):
        '''Return a set of all edges that touch vertex v. 
           Includes all edges in this Graph if v is None.
                   
          args:
          v -- str of v's contents
       '''  
        raise NotImplementedError("Requires subclass implementation")
  
    def nodes(self, v=None):
        '''Return a set of all nodes in this Graph that are adjacent to vertex v. 
         Includes all nodes if v is None:
         
         args:
         v -- str of v's contents
         '''  
        raise NotImplementedError("Requires subclass implementation")
      
        

class UGraph:
    ''' A data structure representing an undirected graph.'''
    def __init__(self, dct):
        ''' Initialize this UGraph with a dictionary dct '''
        self._dct = dct
        
    def add_edge(self, v, w):
        '''Add an edge in this Graph from v to w'''
        if w in self._dct[v] or v in self._dct[w]:
            return
        self._dct[v].append(w)
        self._dct[w].append(v)
    
    def remove_edge(self, v, w):
        '''Remove the edge from v to w in this Graph'''
        self._dct[v].remove(w)
        self._dct[w].remove(v)
    
    def add_node(self, v):
        '''Add node v to this Graph'''
        if v in self._dct.keys():
            return
        self._dct[v] = []
    
    def remove_node(self, v):
        '''Remove node v from this Graph and return its neighbours'''
        self._dct.delete(v)
        
    
    def edges(self, v=None):
        '''Return a set of all edges that touch node v. 
           Includes all edges in this UGraph if v is None.
           
           args:
           v -- str of v's contents
        '''
        res = []
        if v:
            adjacents = self._dct[v]
            for a in adjacents:
                res.append((v, a)) 
        else:
            #for each key, append (key, adj) if (adj, key) not already there
            for vtx in self._dct.keys():
                for adj in self._dct[vtx]:
                    if (adj, vtx) not in res:
                        res.append((vtx, adj))
        return set(res)
    
    def nodes(self, v=None):
        '''Return a set of all nodes in this UGraph that are adjacent to node v. 
           Includes all nodes if v is None:
           
           args:
           v -- str of v's contents
        '''
        res = []
        if v:
            return set(self._dct[v])
        else:
            return set(self._dct.keys())
        
    def is_connected(self):
        '''Return whether this UGraph is connected.'''
        #Pick the first vertex and perform BFS. Return true iff BFS touches every node
        visited = []
        q = [random.sample(self.nodes(), 1)[0]]
        while q:
            curr = q.pop(0)
            visited.append(curr)
            for adj in self.nodes(curr):
                if adj not in visited:
                    q.append(adj)
        if set(visited) == set(self.nodes()):
            return True 
        else:
            return False
    
    def has_eulerian_path(self):
        '''Return whether Graph self has a Eulerian path'''
        if not self.is_connected():
            return False
        count = 0
        for v in self.nodes():
            if len(self.nodes(v))%2 != 0:
                count+=1
                if count > 2: #Return early if odd degree v's surpasses 2
                    return False
        if count == 0 or count == 2:
            return True
        else:
            return False
        
    def has_eulerian_circuit(self):
        '''Return whether Graph self has a Eulerian circuit.'''
        if not self.is_connected():
            return False
        for v in self.nodes():
            if len(self.nodes(v))%2 != 0:
                return False
        return True
    
    def eulerian_circuit(self, v):
        '''Return a Eulerian circuit list beginning at vertex v, if one exists.
        
        Uses Hierholzer's algorithm.
        '''
        result = []
        if not self.has_eulerian_circuit():
            return result
        cpy = copy.deepcopy(self)
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
        
        
    
'''        
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
    print(ug.eulerian_circuit('A'))
'''
                   
    
        
        


        
        