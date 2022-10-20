import networkx as nx
import matplotlib.pyplot as plt
def draw_napartitie(np):
  dimension = nx.get_node_attributes(np, 'dimension')
  nx.draw_networkx(np,labels=dimension,node_size = 30)
  plt.show()
