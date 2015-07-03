from igraph import *

g = Graph([(0,1), (0,2), (2,3), (3,4), (4,2), (2,5), (5,0), (6,3), (5,6)])
print g.degree()
print g.degree(6)
print g.degree([2,3,4])

print g.degree(type='in')
print g.degree(type='out')

print g.edge_betweenness() # or g.betweenness() or g.pagerank()
ebs = g.edge_betweenness()
max_eb = max(ebs)
print [g.es[idx].tuple for idx, eb in enumerate(ebs) if eb == max_eb]

print g.vs.degree()
print g.es.edge_betweenness()
print g.vs[2].degree()
