# Problem Set 11SC: Graph optimization
# Example Problem: Finding shortest paths through MIT buildings
# Name: Mohammad Ehsanul Karim
# Collaborators: Rasik Hasan
# Start: July 12, 2016; 11:41pm
#
# A set of data structures to represent graphs


class Node(object):
   def __init__(self, name):
      self.name = str(name)

   def getName(self):
      return self.name

   def __str__(self):
      return self.name

   def __repr__(self):
      return self.name

   def __eq__(self, other):
      return self.name == other.name

   def __ne__(self, other):
      return not self.__eq__(other)

   def __hash__(self):
        return hash(self.__repr__())

class Edge(object):
   def __init__(self, src, dest):
      self.src = src
      self.dest = dest

   def getSource(self):
      return self.src

   def getDestination(self):
      return self.dest
         
   def __str__(self):
      return str(self.src) + '->' + str(self.dest)

class WeightedEdge(Edge):
   def __init__(self, src, dest, weight):
      self.src = src
      self.dest = dest
      self.weight = weight

   def getWeight(self):
      return self.weight

class Digraph(object):
   """
   A directed graph
   """
   def __init__(self):
      self.nodes = set([])
      self.edges = {}

   def addNode(self, node):
      if node in self.nodes: pass         
      else:
         self.nodes.add(node)
         self.edges[node] = []

   def addEdge(self, edge):
      src = edge.getSource()
      dest = edge.getDestination()

      if not(src in self.nodes and dest in self.nodes):
         raise ValueError('Node not in graph')
      self.edges[src].append(dest)

   def childrenOf(self, node):
      if node in self.nodes: return self.edges[node]
      else: raise ValueError('Node not in graph')   

   def hasNode(self, node):
      return node in self.nodes

   def __str__(self):
      res = ''
      for k in self.edges:
         for d in self.edges[k]:
            res = res + str(k) + '->' + str(d) + '\n'
      return res[:-1]

class WeightedDigraph(Digraph):
   """
   A weighted directed graph
   """
   def __init__(self):
      self.nodes = set([])
      self.edges = {}
      self.weights = {}

   def addEdge(self, edge):
      src = edge.getSource()
      dest = edge.getDestination()      

      if not(src in self.nodes and dest in self.nodes):
         raise ValueError('Node not in graph')
      
      self.edges[src].append(dest)
      self.weights[(src, dest)] = edge.getWeight()  
      
   def getWeight(self, src, dest):
      return self.weights[(src, dest)]

   def __str__(self):
      res = ''
      for s in self.edges:
         for d in self.edges[s]:
            (dist1, dist2) = self.weights[(s, d)]
            weight = '(' + str(dist1) + ', ' + str(dist2) + ')'
            res = res + str(s) + ' -> ' + weight + ' -> ' + str(d) + '\n'
      return res[:-1]
