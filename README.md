# SNA Utilities

sna_utils is a Python package containing a variety of convenience functions that automate various social
network analysis-related tasks. Such tasks currently include: creating NetworkX graph objects from pandas DataFrames; 
deriving network graph visualizations from NetworkX graph objects via PyVis; creating neighbor overlap graphs from 
DataFrames; and converting nodes + node attributes contained in a NetworkX graph object to DataFrames.

# Installation

To install sna_utils into the site-packages directory of your virtual environment, run:

`pip install git+https://github.com/agile-enigma/SNA-Utilities.git`

sna_utils is now ready to be imported within your virtual environment.

# Usage

## create_graph
### create_nxgraph()

After importing sna_utils via `import sna_utils` you can create a NetworkX graph object from a pandas DataFrame
by running `sna_utils.create_nxgraph()`.

Parameters are as follows:

* **edges_df**    : pandas DataFrame. Must contain 'source' and 'target' columns, and optionally a 'weight' column.
No other columns will factor into the creation of the NetworkX graph object.
* **weight_scale**: Scales edge thickness. Defaults to 1.0.
* **cmap_**       : Specifies colormap for node and edge colors. Defaults to 'viridis'. 
* **directed**    : Boolean specifying whether the graph is directed or undirected. Defaults to False.
* **centrality**  : Specifies the centrality measure determining node and label sizing via node 'value' attributes.
Defaults to nx.degree_centrality. 

In the event that edges_df does not contain a weight column, create_nxgraph() will calculate weights. Unlike
NetworkX's from_pandas_edgelist() function, it will sum the weights of all occurrences of specific source-target 
pairs in addition to deleting duplicates. For undirected graphs create_nxgraph() will sort nodes 
within source-target pairs to ensure that weights are properly calculated. Additionally, it will assign a 'value'
attribute to nodes, which determines node and label sizing when input into pyvisualize_graph().

Finally, create_nxgraph() will assign nodes to a community using nx.community.louvain_community(). 
Node 'color' attributes will be mapped accordingly.

## visualize_graph
### pyvisualize_graph()

The output of create_nxgraph() is intended to be fully prepped for input into the pyvisualize_graph function for 
visualization. The PyVis graph visualization functionality can be accessed via `sna_utils.pyvisualize_graph()`. 
It will return an .html file in the run directory containing the network visualization. pyvisualize_graph() will 
automatically determine whether the input NetworkX graph object is directed or not.

Parameters are as follows:

* **nx_graph**    : The NetworkX graph object to be visualized.
* **select_menu** : Display select menu. Defaults to True.
* **filter_menu** : Display filter menu. Defaults to True.
* **show_buttons**: Display 'physics' and 'nodes' configuration menus. Defaults to False.

The physics of the output visualization are "forceAtlas2Based".

## neighbor_overlap
### create_overlaph_graph()

`sna_utils.create_overlap_graph()` links nodes by mutual neighbors. For directed graphs, neighbors can 
take one of two forms: all nodes targeting example node A, or all nodes targeted by example node A. The 
'incoming' parameter determines which of these two architectures is used for directed graphs. Two directed 
edges will be created for each node pair with mutual neighbors in the output NetworkX graph: one directed at 
node B from node A and vice-versa. Edge weights are calculated by dividing mutual neighbors by the originating 
node's total neighbor count. 

Like create_nxgraph(), create_overlap_graph() will assign each node to a community and map color attributes accordingly.
Node 'value' attributes--which determine node and label sizing in pyvisualize_graph()--are determined by a node's 
neighbor count. As with create_nxgraph(), the intent is for the output to be fully prepared for input into pyvisualize_graph().

If directed is set to False, create_overlap_graph() will ignore the 'incoming' parameter.

Parameters are as follows:

* **edges_df**: pandas DataFrame object
* **directed**: Specifies whether the graph is directed. Default is False.
* **incoming**: Specifies whether overlap is determined by incoming or outgoing edges for directed graphs. Default is False.
* **cmap_**   : Specifies cmap to be used to map node community assignment to 'color'. Default is 'viridis'.

### mutual_neighbors()

`sna_utils.mutual_neighbors()` outputs mutual neighbors between two input nodes contained within a NetworkX
graph object. It will automatically determine whether the input NetworkX graph is directed or not. If input 
NetworkX graph object is not directed mutual_neighbors() ignore the 'incoming' parameter. 

Parameters are as follows:

* **nx_graph**: NetworkX graph object.
* **node1**   : Node contained within nx_graph.
* **node2**   : Node contained within nx_graph.
* **incoming**: Specifies whether neighbors are determined by incoming or outgoing edges for directed graphs. Default is False.

## convert_graph
### to_pd_nodeslist()

`sna_utils.to_pd_nodeslist()` converts the nodes contained in a NetworkX graph object to a pandas DataFrame. 
Each node attribute will be contained in a distinct column.

* **nx_graph**: NetworkX graph object to be converted to a pandas DataFrame.
