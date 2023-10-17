import pandas as pd
import matplotlib as mpl
import networkx as nx
from itertools import combinations

def create_overlap_graph(edges_df, cmap_='viridis', directed=False, incoming=False):
    
    if not type(edges_df) == type(pd.DataFrame()):
        raise TypeError('edges_df type must be pandas.core.frame.DataFrame')

    edges_df.columns = map(str.lower, edges_df.columns)
    edges_df = edges_df[['source', 'target']].astype(object)
    
    graph = nx.DiGraph() if directed else nx.Graph()
    if directed == True and incoming == True:
        graph.add_edges_from(map(lambda x: (x.target, x.source), edges_df.itertuples()))
    else:
        if directed == False and incoming == True:
            print('incoming set to True even though graph is undirected. ignoring incoming parameter...')
        graph.add_edges_from(map(lambda x: (x.source, x.target), edges_df.itertuples()))

    overlap_graph = nx.DiGraph()
    for node1, node2 in combinations(graph.nodes, 2):
        shared_audience = len(set(nx.neighbors(graph, node1)).intersection(set(nx.neighbors(graph, node2))))
        if shared_audience > 0:
            overlap_graph.add_edge(node1, node2, weight = round((shared_audience/
                                                          len(list(nx.neighbors(graph, node1))) * 100),1)
                                  )
            overlap_graph.add_edge(node2, node1, weight = round((shared_audience/
                                                          len(list(nx.neighbors(graph, node2))) * 100),1)
                                  )
        
    community = {}
    part = nx.community.louvain_communities(overlap_graph, seed=0)
    for i in range(len(part)):
        community.update({node:i for node in part[i]})
    cmap = mpl.cm.get_cmap(cmap_, len(part))
    
    for node in overlap_graph.nodes:                   
        overlap_graph.nodes[node]['label']     = ' '.join([node + ':', str(len(list(nx.neighbors(graph, node))))])
        overlap_graph.nodes[node]['value']     = len(list(nx.neighbors(graph, node)))
        overlap_graph.nodes[node]['community'] = community[node]
        overlap_graph.nodes[node]['color']     = mpl.colors.rgb2hex(cmap.colors[overlap_graph.nodes[node]['community']])

    # style = edges_df.style.format(precision=2).background_gradient(cmap='BuPu', axis=0)
    # return style

    return overlap_graph


def mutual_neighbors(nx_graph, node1, node2, incoming=False):

    if 'networkx' not in str(type(nx_graph)):
        raise TypeError('nx_graph must be an nx graph object.')

    directed = True if 'DiGraph' in str(type(nx_graph)) else False
    if directed == True and incoming == True:
        reversed_graph = nx.DiGraph()
        reversed_graph.add_edges_from(map(lambda x: (x[1], x[0]), list(nx_graph.edges)))
        return set(nx.neighbors(reversed_graph, node1)).intersection(
               set(nx.neighbors(reversed_graph, node2))
        )
    else:
        if directed == False and incoming == True: 
            print('incoming set to True even though graph is directed. ignoring incoming parameter...')

        return set(nx.neighbors(nx_graph, node1)).intersection(
               set(nx.neighbors(nx_graph, node2))
        )
