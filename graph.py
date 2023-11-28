import json
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D  # for custom legends
from networkx.drawing.nx_agraph import graphviz_layout

matplotlib.use('agg')

def add_nodes_from_json(parent_name, subcapabilities, G):
    for item in subcapabilities:
        cap_name = item['name']
        G.add_node(cap_name)
        G.add_edge(parent_name, cap_name)
        if 'subCapabilities' in item:
            add_nodes_from_json(cap_name, item['subCapabilities'], G)

def create_graph_from_json(json_data):
    G = nx.DiGraph()
    for capability in json_data['capabilities']:
        cap_name = capability['name']
        G.add_node(cap_name)
        if 'subCapabilities' in capability:
            add_nodes_from_json(cap_name, capability['subCapabilities'], G)
    return G


def save_graph(json_data, pdf_path):
    G = create_graph_from_json(json_data)

    # Use Graphviz to lay out the graph
    pos = graphviz_layout(G, prog='dot')

    # Visualize the graph
    plt.figure(figsize=(150, 30))
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=4000, font_size=10, arrowsize=20, margins=0, min_target_margin=25)
    plt.title('Capability Hierarchy')

    plt.savefig(pdf_path)
