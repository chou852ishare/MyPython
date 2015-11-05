from igraph import *

g = Graph([(0,1), (0,2), (2,3), (3,4), (4,2), (2,5), (5,0), (6,3), (5,6)])
g.vs['name'] = ['Alice', 'Bob', 'Claire', 'Dennis', 'Esther', 'Frank', 'George']
g.vs['age'] = [25, 31, 18, 47, 22, 23, 50]
g.vs['gender'] = ['f', 'm', 'f', 'm', 'f', 'm', 'm']
g.es['is_formal'] = [False, False, True, True, True, False, True, False, False]
g.es[0]['is_formal'] = True
g['date'] = '2009-01-10'
g.vs[3]['foo'] = 'bar'
del g.vs['foo']

# selecting vertices and edges
print g.vs.select(_degree = g.maxdegree())['name']

seq = g.vs.select(None)
print len(seq)

graph = Graph.Full(10)
only_odd_vertices = graph.vs.select(lambda vertex: vertex.index % 2 == 1)
print len(only_odd_vertices)

seq = graph.vs.select([2 ,3, 7])
print len(seq)
print [v.index for v in seq]
seq = seq.select([0,2])
print [v.index for v in seq]
seq = graph.vs.select([2, 3, 7, 'foo', 3.5]) # floats, strings, invalid vertex IDs will be ignored
print len(seq)

print [v.index for v in g.vs.select(age_lt=30)]
print [v.index for v in g.vs(age_lt=30)]
print [v.index for v in g.vs(_degree_gt=2)]
print [e.index for e in g.es(_source=2)]
print [e.index for e in g.es(_within=[2,3,4])]
print [e.index for e in g.es(_within=g.vs[2:5])]
men = g.vs(gender='m')
women = g.vs(gender='f')
print [e.index for e in g.es(_between=(men,women))]

# finding a single vertex or edge with some properties
claire = g.vs.find(name='Claire')
print type(claire)
print claire.index
#g.vs.find(name='Joe')

# looking up vertices by names
print g.degree('Dennis')
print g.vs.find('Dennis').degree()
