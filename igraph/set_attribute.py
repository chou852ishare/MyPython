from igraph import *

g = Graph([(0,1), (0,2), (2,3), (3,4), (4,2), (2,5), (5,0), (6,3), (5,6)])
print g.vs
g.vs['name'] = ['Alice', 'Bob', 'Claire', 'Dennis', 'Esther', 'Frank', 'George']
g.vs['age'] = [25, 31, 18, 47, 22, 23, 50]
g.vs['gender'] = ['f', 'm', 'f', 'm', 'f', 'm', 'm']
g.es['is_formal'] = [False, False, True, True, True, False, True, False, False]

print g.es[0]
print g.es[0].attributes()
g.es[0]['is_formal'] = True
print g.es[0]

g['date'] = '2009-01-10'
print g['date']

g.vs[3]['foo'] = 'bar'
print g.vs['foo']
del g.vs['foo']
print g.vs['foo']
