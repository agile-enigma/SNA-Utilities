import matplotlib as mpl
import networkx as nx
import numpy as np
import pandas as pd
import warnings

warnings.filterwarnings("ignore")


def create_nxgraph(
    edges_df,
    weight_scale=1.0,
    cmap_="viridis",
    directed=False,
    centrality=nx.degree_centrality
):
    if not isinstance(edges_df, pd.DataFrame):
        raise TypeError("edges_df type must be pandas.core.frame.DataFrame.")

    # format dtypes and column headers
    edges_df.columns = map(str.lower, edges_df.columns)

    if "weight" in edges_df.columns:
        weight_column = True
        edges_df["weight"] = edges_df["weight"].astype(float)
        edges_df = edges_df[["source", "target", "weight"]]
    else:
        weight_column = False
        edges_df = edges_df[["source", "target"]]

    edges_df[["source", "target"]] = edges_df[["source", "target"]].astype(str)

    # apply weights if not present; sort edges for undirected graphs
    if not weight_column:
        edges_df["weight"] = 1.0
    if not directed:
        for row in edges_df[edges_df.source > edges_df.target].itertuples():
            sorted_ = sorted([row.source, row.target])
            edges_df.loc[row.Index, ["source", "target"]] = sorted_

    # sum weights and delete duplicate rows via groupby and apply weight_scale
    edges_df = edges_df.groupby(["source", "target"]).sum().reset_index()
    edges_df.weight = round((edges_df.weight * weight_scale), 2)

    # initialize graph; add edges and weight
    graph_type = nx.DiGraph() if directed else nx.Graph()
    graph = nx.from_pandas_edgelist(
        edges_df,
        source="source",
        target="target",
        edge_attr="weight",
        create_using=graph_type,
    )

    # community partition and cmap
    community = {}
    part = nx.community.louvain_communities(graph, seed=0)
    for i in range(len(part)):
        community.update({node: i for node in part[i]})
    cmap = mpl.cm.get_cmap(cmap_, len(part))

    # add node attributes
    for node in graph.nodes:
        graph.nodes[node]["value"] = round(
            abs(
                (
                    centrality(graph)[node]
                    - np.mean(list(dict(centrality(graph)).values()))
                )
                / np.std(list(dict(centrality(graph)).values()))
            ),
            2,
        )
        graph.nodes[node]["label"] = (
            str(node) + ": " + str(round(centrality(graph)[node], 3))
        )
        graph.nodes[node]["title"] = (
            str(node) + " Neighbors:\n" + "\n".join(list(graph.neighbors(node)))
        )
        graph.nodes[node]["community"] = community[node]
        graph.nodes[node]["color"] = mpl.colors.rgb2hex(
            cmap.colors[graph.nodes[node]["community"]]
        )

    return graph
