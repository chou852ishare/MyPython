from igraph import *

g = Graph.Tree(127, 2)
print 'summary of g.tree(127,2)'
summary(g)

g2 = Graph.Tree(127, 2)
print g2.get_edgelist() == g.get_edgelist()

print g2.get_edgelist()[0:10]

g = Graph.GRG(100, 0.2)
print 'summary of g.GRG(100, 0.2)'
summary(g)

g2 = Graph.GRG(100, 0.2)
print g.get_edgelist() == g2.get_edgelist()
print g.isomorphic(g2)
