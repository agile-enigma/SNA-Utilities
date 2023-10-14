import matplotlib as mpl
import matplotlib.cm as cm
import networkx as nx
import numpy as np
import pandas as pd

def create_nxgraph(edges_df, weight_scale=1.0, cmap_='viridis', directed=False, 
                   centrality=nx.degree_centrality):
    """

    """
    
    if not type(edges_df) == type(pd.DataFrame()):
        raise TypeError('edges_df type must be pandas.core.frame.DataFrame.')

    # format dtypes and column headers
    for col in edges_df.columns:
        edges_df.rename(columns={col: col.lower()}, inplace=True)
        
    if 'weight' in edges_df.columns:
        weight_column=True
        edges_df['weight'] = edges_df['weight'].astype(float)
        edges_df = edges_df[['source', 'target', 'weight']]
    else:
        weight_column=False
        edges_df = edges_df[['source', 'target']]

    edges_df[['source', 'target']] = edges_df[['source', 'target']].astype(str)
    
    # determine weights and format edges
    if not directed:
        if not weight_column:
            edges_df['weight'] = 1.0
        for row_index in edges_df[edges_df.source > edges_df.target].index:
            sorted_ = sorted(edges_df.loc[row_index, ['source', 'target']])
            edges_df.loc[row_index, 'source'] = sorted_[0]
            edges_df.loc[row_index, 'target'] = sorted_[1]

    elif directed and not weight_column:
        edges_df['weight'] = 1.0
        
    # final edges_df processing: groupby and weight_scale
    edges_df = edges_df.groupby(['source', 'target']).sum().reset_index()
    edges_df.weight = edges_df.weight * weight_scale
    
    # initialize graph; add edges and weight
    graph_type = nx.DiGraph() if directed else nx.Graph()
    graph = nx.from_pandas_edgelist(
        edges_df,
        source       = 'source',
        target       = 'target',
        edge_attr    = 'weight',
        create_using = graph_type
        )
    
    # community partition and cmap
    part = nx.community.louvain_communities(graph, seed=0)
    for i, community in enumerate(part):
        for node in community:
            graph.nodes[node]['community'] = i
    cmap = cm.get_cmap(cmap_, len(part))
    
    # add node attributes
    for node in graph.nodes:
        # graph.nodes[node]['size'] = (centrality(graph)[node]  - np.mean(list(dict(centrality(graph)).values())) / 
        #                                   np.std(list(dict(centrality(graph)).values())))
        graph.nodes[node]['value'] = abs((centrality(graph)[node] - np.mean(list(dict(centrality(graph)).values()))) / 
                                     np.std(list(dict(centrality(graph)).values())))
        graph.nodes[node]['label'] = str(node) + ': ' + str(round(centrality(graph)[node], 3))
        # graph.nodes[node]['title'] = str(node) + ' Neighbors:\n' + \
        #                              '\n'.join(list(graph.neighbors(node)))
        graph.nodes[node]['color'] = mpl.colors.rgb2hex(cmap.colors[graph.nodes[node]['community']]) # map partition class onto cmap rgba; convert to hex

    return graph
