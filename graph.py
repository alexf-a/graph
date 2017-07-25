import random
import copy
import logging

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
        if v in self._dct.keys():
            logging.info("Node " + str(v) + " already in this Graph")
            return
        self._dct[v] = []
    
    def remove_node(self, v):
        '''Remove node v from this Graph and return its neighbours'''
        try:
            result = self._dct.pop(v, None)
            if result:
                for vtx in self.nodes():
                    if vtx in self._dct[vtx]:
                        result.append(vtx)
                        self._dct[vtx].remove(v)  
            return set(result)
        except KeyError:
            return
        
    
    def edges(self, v=None):
        '''Return a set of all edges that touch vertex v. 
           Includes all edges in this Graph if v is None.
                   
          args:
          v -- str of v's contents
       '''  
        raise NotImplementedError("Requires subclass implementation")
  
    def nodes(self):
        '''Return a set of all nodes in this Graph'''  
        return set(self._dct.keys())
      
        

class UGraph(Graph):
    ''' A data structure representing an undirected graph.'''
    def __init__(self, dct):
        ''' Initialize this UGraph with a dictionary dct '''
        Graph.__init__(self, dct)
        
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
    
    def remove_node(self, v):
        '''Remove node v from this Graph and return its neighbours'''
        try:
            result = self._dct.pop(v, None)
        except KeyError:
            return
        if result:
            for vtx in self._dct.keys():
                self._dct[vtx].remove(v)
        return result
        
    
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
    
    def neighbours(self, v):
        '''Return a set of all neighbours in this UGraph of node v. '''
        return set(self._dct[v])
        
    def is_connected(self):
        '''Return whether this UGraph is connected.'''
        #Pick the first vertex and perform BFS. Return true iff BFS touches every node
        visited = []
        q = [random.sample(self.nodes(), 1)[0]]
        while q:
            curr = q.pop(0)
            visited.append(curr)
            for adj in self._dct[curr]:
                if adj not in visited:
                    q.append(adj)
        if set(visited) == set(self.nodes()):
            return True 
        else:
            return False
    
    def has_eulerian_path(self):
        '''Return whether UGraph self has a Eulerian path'''
        if not self.is_connected():
            return False
        count = 0
        for v in self.nodes():
            if len(self.neighbours(v))%2 != 0:
                count+=1
                if count > 2: #Return early if odd degree v's surpasses 2
                    return False
        if count == 0 or count == 2:
            return True
        else:
            return False
        
    def has_eulerian_circuit(self):
        '''Return whether UGraph self has a Eulerian circuit.'''
        if not self.is_connected():
            return False
        for v in self.nodes():
            if len(self.neighbours(v))%2 != 0:
                return False
        return True
    
    def eulerian_circuit(self, v):
        '''Return a Eulerian circuit list beginning at vertex v, if one exists.
         Raise NodeError if v not in this UGraph
        
        Uses Hierholzer's algorithm.
        '''
        if v not in self.nodes():
            raise NodeError("Node " + str(v) + " is not in this UGraph")
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
                nbr = random.sample(cpy.neighbours(w), 1)[0]
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
    
    
class DGraph(Graph):
    '''A data structure representing a directed graph.'''
    def __init__(self, dct):
        '''Initialize this DGraph with a dictionary dct'''
        Graph.__init__(self, dct)
        
    def add_edge(self, v, w):
        '''Add a directed edge from v to w in this DGraph.'''
        if w not in self._dct[v]:
            self._dct[v].append(w)
        else:
            logging.info("The edge from " + str(v) + " to " + str(w) + " is already in this DGraph")
        
    def remove_edge(self, v, w):
        '''Remove the directed edge from v to w in this DGraph.'''
        if w in self._dct[v]:
            self._dct[v].remove(w)
        else:
            logging.info("The edge from " + str(v) + " to " + str(w) + " is not in this DGraph")
        
    def remove_node(self, v):
        '''Remove node v from this DGraph, and return its successors.'''
        try:
            result = self._dct.pop(v, None)
            for node in self.nodes():
                if node in self._dct[node]:
                    self._dct[node].remove(v)
            return set(result)
        except KeyError:
            logging.info("Node " + str(v) + " is not in this Graph")
            return
        
    def successors(self, v):
        '''Return a set of the successors of node v in this DGraph.'''
        return set(self._dct[v])
    
    def transpose(self):
        '''Return the transpose of this DGraph (all directed edges are reversed).'''
        result = DGraph({})
        for node in self._dct.keys():
            result.add_node(node)
        for node in self._dct.keys():
            for scr in self.successors(node):
                result.add_edge(scr, node)
        return result
                

    def is_connected(self):
        '''Return whether this DGraph is connected.'''
        #See if DFS from random node hits every other node
        if not self._dfs_conn():
            return False
        tpose = self.transpose()
        if not tpose._dfs_conn():
            return False
        return True
            
        
    def _dfs_conn(self):
        s = [random.sample(self.nodes(), 1)[0]]
        visited = []
        while s:
            print(s)
            curr = s.pop()
            visited.append(curr)
            for scr in self.successors(curr):
                if scr not in visited and scr not in s:
                    s.append(scr)
        if set(visited) != self.nodes():
            return False
        else:
            return True
        
        
def NodeError(Exception):
    '''An Exception for raised trying to access non-existant nodes in a Graph.'''
    pass
        
   
    
       
if __name__ == '__main__':
    '''
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
    
    dg = DGraph({})
    dg.add_node('A')
    dg.add_node('B')
    dg.add_node('C')
    dg.add_node('D')
    dg.add_node('E')
    dg.add_node('F')
    dg.add_edge('A', 'B')
    dg.add_edge('A', 'F')
    dg.add_edge('F', 'A')
    dg.add_edge('B', 'A')
    dg.add_edge('B', 'C')
    dg.add_edge('B', 'E')
    dg.add_edge('C', 'D')
    dg.add_edge('D', 'C')
    dg.add_edge('C', 'F')
    dg.add_edge('F', 'B')
    dg.add_edge('F', 'E')
    dg.add_edge('E', 'F')
    dg.add_edge('E', 'D')
    print(dg.is_connected())
                   
    
        
        


        
        