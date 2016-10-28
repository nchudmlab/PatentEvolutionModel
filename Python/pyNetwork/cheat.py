import networkx as nx


g = nx.Graph()

f = open('com-amazon.ungraph.txt','r')
for line in f:
    line = line.strip()
    splited = line.split('\t')
    #print(splited[0])
    g.add_edge(splited[0], splited[1])
    
print('-----')
print(g.number_of_nodes(),g.number_of_edges())
print(nx.diameter(g, e=None))


