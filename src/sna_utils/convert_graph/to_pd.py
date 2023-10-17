import pandas as pd
import networkx as nx

def to_pd_nodeslist(nx_graph):
    
    if 'networkx' not in str(type(nx_graph)):
        raise TypeError('nx_graph must be an nx graph object.')

    nodes_df =  pd.DataFrame([node[1] for node in 
                              list(nx_graph.nodes(data=True))],
                              index = list(nx_graph.nodes)).reset_index()
    nodes_df.rename(columns={'index': 'node'}, inplace=True)
    
    return nodes_df
