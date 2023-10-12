# SNA Utilities

sna_utils is a python package containing a variety of convenience functions for automating various social
network analysis-related tasks. Such tasks currently include: creating NetworkX graph objects from pandas DataFrames; 
deriving network graph visualizations from NetworkX graph objects via PyVis.

# Installation

`pip install git+https://github.com/agile-enigma/SNA-Utilities`

# Use

After importing sna_utils via `import sna_utils` you can create a NetworkX graph object from a pandas DataFrame
by running `sna_utils.create_nxgraph()`. Its parameters are:

* edges_df    : pandas DataFrame. Must contain 'source' and 'target' columns, and optionally a 'weight' column.
all other columns will not factor into the creation of the NetworkX graph object.
* weight_scale: Determines edge thickness. Defaults to 1.0.
* cmap_       : Specifies colormap for node and edge colors. Defaults to 'viridis'. 
* directed    : Boolean specifying whether the graph is directed or undirected. Defaults to False.
* centrality  : Specifies the centrality measure determining node and label sizing. Defaults to 
nx.degree_centrality. 

In the event that edges_df does not contain a weight column, create_nxgraph() will calculate weights. If
the graph is undirected and contains duplicate source-target pairs, it will delete duplicates and sum the weights
of all occurrences of that source-target pair. Additionally, for undirected graph create_nxgraph() will sort 
source-target pairs to ensure that weights are properly determined. Finally, create_nxgraph will assign nodes to 
a community using nx.community.louvain_community(). Node 'color' attribute will be mapped accordingly.

The PyVis graph visualization functionality can be accessed via `sna_utils.pyvisualize_graph()`. It will return
 an .html file in the run directory containing the network visualization. Its parameters are as follows:

* graph       : The NetworkX graph object to be visualized.
* directed    : Boolean specifying whether the output visualization is directed or undirected. Defaults to False.
* notebook    : If set to True and run from within a Jupyter notebook will output visualization in the notebook. Default is False.
* select_menu : Display select menu. Defaults to True.
* filter_menu : Display filter menu. Defaults to True.
* show_buttons: Display 'physics' and 'nodes' configuration menus. Defaults to False.

The physics of the output visualization are "forceAtlas2Based".
