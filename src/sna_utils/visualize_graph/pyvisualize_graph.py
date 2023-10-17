from pyvis.network import Network

def pyvisualize_net(graph, height="800px", width="100%", algo="forceAtlas2Based", notebook=True, 
                    select_menu=True, filter_menu=True, show_buttons=False):
    
    directed = True if 'DiGraph' in str(type(graph)) else False
    net = Network(height=height, width=width, bgcolor="#222222", font_color="white", directed=directed,
                  notebook=notebook, select_menu=select_menu, filter_menu=filter_menu)
    
    if show_buttons: net.show_buttons(filter_=['physics', 'nodes'])
        
    net.set_options("""
        const options = {
          "nodes": {
            "borderWidth": 1.5,
            "borderWidthSelected": null,
            "opacity": 1.0,
            "fixed": {
              "x": null,
              "y": null
            },
            "scaling": {
              "min": 10,
              "max": 60,
              "label": {
                "enabled": true,
                "min": 20,
                "max": 60,
                "maxVisible": null,
                "drawThreshold": null
              }
            },
            "size": true
          },
          "physics": {
            "forceAtlas2Based": {
            },
            "minVelocity": 0.75,
            "solver": "forceAtlas2Based"
          }
        }
    """)
    net.from_nx(graph)
    return net.show(str(graph) + ".html")
