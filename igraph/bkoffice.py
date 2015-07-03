from igraph import *

path = './bkoff-GraphML/'
gfile_undirected = path + 'BKOFFB.GraphML'
gfile_directed = path + 'BKOFFC.GraphML'

bkoff = Graph.Read_GraphML(gfile_directed)
#bkoff = bkoff.as_directed()
print summary(bkoff)
print bkoff.is_directed()
#plot(bkoff)

print bkoff.degree(type='in')
print bkoff.degree(type='out')

print bkoff.is_simple()
#print bkoff.is_loop()
