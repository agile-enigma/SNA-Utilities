def create_overlap_graph(edges_df, cmap_='viridis', directed=False):
    
    for col in edges_df.columns: edges_df.rename(columns={col: col.lower()}, inplace=True)
    edges_df = edges_df[['source', 'target']].astype(object)
    
    if directed == False:
        graph = nx.Graph()
        graph.add_edges_from([(row.source, row.target) for _, row in edges_df.iterrows()])

    elif directed == True:
        graph = nx.DiGraph()
        graph.add_edges_from([(row.target, row.source) for _, row in edges_df.iterrows()])

    overlap_graph = nx.DiGraph()
    for node1, node2 in combinations(graph.nodes, 2):
        shared_audience = len(set(nx.neighbors(graph, node1)).intersection(set(nx.neighbors(graph, node2))))
        if shared_audience > 0:
            overlap_graph.add_edge(node1, node2, weight = round((shared_audience/
                                                          len(list(nx.neighbors(graph, node1))) * 100),1))
            overlap_graph.add_edge(node2, node1, weight = round((shared_audience/
                                                          len(list(nx.neighbors(graph, node2))) * 100),1))
        
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
    # style

    return overlap_graph


def mutual_neighbors(nx_graph, node1, node2, directed=False, incoming=False):

    if directed == True and incoming == True:
        reversed_graph = nx.DiGraph()
        reversed_graph.add_edges_from(list(map(lambda x: (x[1], x[0]), 
                                               list(got_graph.edges)))
                                     )
        return set(nx.neighbors(reversed_graph, node1)).intersection(
               set(nx.neighbors(reversed_graph, node2))
        )
    else:
        return set(nx.neighbors(nx_graph, node1)).intersection(
            set(nx.neighbors(nx_graph, node2))
        )
