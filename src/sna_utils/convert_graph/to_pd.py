import pandas as pd
import networkx as nx

def to_pd_nodeslist(nx_graph):
    
    nodes_df =  pd.DataFrame([node[1] for node in 
                              list(nx_graph.nodes(data=True))],
                              index = list(nx_graph.nodes)
    ).reset_index()
    nodes_df.rename(columns={'index': 'node'}, inplace=True)
    return nodes_df
