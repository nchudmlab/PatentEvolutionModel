import networkx as nx
#import matplotlib.pyplot as plt
from pyMysql import mysql 


G=nx.Graph()

G.add_edge('a', 'b')
G.add_edge('a', 'c')

for node in G.nodes():
    if G.degree(node) is 1:
        G.remove_node('a')

print(G.nodes())

# f = open('STedges.txt','r',encoding='utf-8')
# #G = nx.read_edgelist(f,delimiter=' ')
# s = '['
# for line in f.readlines():
#     tmp = line.strip().split()
#     s+='["{}",5,"{}"],'.format(tmp[0],tmp[1])
#     G.add_edge(tmp[0], tmp[1])
# s = s[:-1]+']'
# 
# f.close()
# 
# sql = mysql()
# sql.connect()
# f = open('tmp','w')
#  
# dict = {}
# for patNO,date in sql.getDate(set(G.nodes())):
#     key = str(date)
#     if key in dict:
#         dict[key].append(patNO)
#     else:
#         dict[key] = []
#         dict[key].append(patNO)
#          
# count=0        
# for key in dict:
#     f.write('sankey.stack({},{});\n'.format(count,dict[key]))
#     count+=1
#      
# f.write('sankey.setData({});'.format(s))
#  
# f.close()

#nx.draw_shell(G)
# nx.draw_graphviz(G)
# plt.show()