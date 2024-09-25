import pydot

def generate_graph_cfg(dot_code):

    # Create a graph from the DOT code
    (graph,) = pydot.graph_from_dot_data(dot_code)

    # Write to SVG
    graph.write_png("graph2.png")
