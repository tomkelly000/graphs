''' graphs.py
    A python module for manipulating graphs
    Tom Kelly '''

from itertools import permutations
from copy import deepcopy

class Graph:
  ''' A graph is represented by a dictionary where the keys represent vertices
      and the values are an array of neighbors '''
  incidence = {}
  V = 0

  def __init__(self, incidence):
    self.incidence = deepcopy(incidence)
    self.V = len(incidence)

  def equals(self, graph):
    ''' Return True if the graphs are equal as labeled graphs '''
    if self.numVertices() != graph.numVertices():
      return False

    for vertex in self.vertices():
      if set(self.neighbors(vertex)) != set(graph.neighbors(vertex)):
        return False
    return True

  def isomorphisms(self):
    ''' Return a list of all isomorphic copies of the graph '''
    copies = []
    for perm in permutations(range(self.V)):
      graph = self.permuteVertexLabels(perm)
      duplicate = False
      for copy in copies:
        if copy.equals(graph):
          duplicate = True
          break
      if not duplicate:
        copies.append(graph)

    return copies

  def permuteVertexLabels(self, perm):
    ''' return a copy of the graph with the labels permuted as per perm '''
    copy = deepcopy(self.incidence)

    vertices = self.vertices()

    # change outgoing part of edges
    for vertex in vertices:
      copy[vertex] = [vertices[perm[vertices.index(neighbor)]] for neighbor in self.neighbors(vertex)]

    # change where they come from
    temp = deepcopy(copy)
    for i in range(len(vertices)):
      copy[vertices[perm[i]]] = sorted(temp[vertices[i]])

    return Graph(copy)

  def isomorphic(self, graph):
    ''' Returns True if the graph is isomorphic to graph '''
    for g in graph.isomorphisms():
      if self.equals(g):
        return True
    return False

  def fitsIn(self, graph):
    ''' If the graph can fit inside an isomorphic copy of graph return that copy
        otherwise return None '''
    for g in graph.isomorphisms():
      if self.equals(g.subgraph([x for x in range(self.numVertices())]).relabel()):
        return g
    return None

  def addVertex(self, label, neighbors):
    ''' Add a vertex with the given neighbors to the graph '''
    self.V = self.V + 1
    self.incidence[label] = neighbors
    for neighbor in neighbors:
      self.incidence[neighbor].append(label)

  def neighbors(self, vertex):
    ''' Returns the neighbors of the given vertex '''
    return self.incidence[vertex]

  def numVertices(self):
    ''' Returns the number of vertices '''
    return self.V

  def numEdges(self):
    ''' Returns the number of edges '''
    totalDegree = 0
    for vertex in self.incidence.keys():
      totalDegree = totalDegree + len(self.incidence[vertex])
    return totalDegree / 2

  def vertices(self):
    ''' Return a list of the edges '''
    return self.incidence.keys()

  def subgraph(self, vertices):
    ''' Return the subgraph induced on the given vertices '''
    copy = dict([(vertex, [v for v in self.incidence[vertex] if v in vertices]) for vertex in vertices])
    return Graph(copy)

  def relabel(self):
    ''' Map the vertices to range(V) and return itself for chaining '''
    copy = {}
    vertices = self.vertices()
    for vertex in vertices:
      copy[vertices.index(vertex)] = [vertices.index(neighbor) for neighbor in self.neighbors(vertex)]
    self.incidence = copy
    return self

  def copy(self):
    ''' Return a new copy of the graph '''
    return Graph(self.incidence)

  def __str__(self):
    ''' Return the string representation of the graph '''
    return str(self.incidence)

