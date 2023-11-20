import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout

# Create a directed graph
G = nx.DiGraph()

# Add nodes for Level 0 capabilities
G.add_node('Product Development')
G.add_node('Urban Mobility Solutions Development')
G.add_node('Autonomous Driving Technology Development')
G.add_node('Dynamic Routing Algorithm Development')
G.add_node('Operations and Logistics')
G.add_node('Ridepooling Service Operations')
G.add_node('Fleet Management')
G.add_node('Infrastructure Management')
G.add_node('Multimodal Transportation Integration')
G.add_node('Public Transit Integration')
G.add_node('Customer Management')
G.add_node('Co-Creation and User Engagement')
G.add_node('Data Analysis and Modeling')

# Add edges for Level 0 capabilities
G.add_edges_from([('Product Development', 'Urban Mobility Solutions Development'),
                  ('Product Development', 'Autonomous Driving Technology Development'),
                  ('Product Development', 'Dynamic Routing Algorithm Development'),
                  ('Operations and Logistics', 'Ridepooling Service Operations'),
                  ('Operations and Logistics', 'Fleet Management'),
                  ('Operations and Logistics', 'Infrastructure Management'),
                  ('Operations and Logistics', 'Multimodal Transportation Integration'),
                  ('Operations and Logistics', 'Public Transit Integration'),
                  ('Customer Management', 'Co-Creation and User Engagement'),
                  ('Customer Management', 'Data Analysis and Modeling')])

# Add nodes for Level 1 capabilities
level_1_capabilities = ['Research and Development', 'Prototyping', 'Testing and Validation',
                       'Service Planning', 'Driver Management', 'Customer Support',
                       'Vehicle Maintenance', 'Asset Tracking', 'Fuel Management',
                       'Network Security', 'Facility Maintenance', 'Technology Integration',
                       'Seamless Transfer Solutions', 'Intermodal Connectivity',
                       'Schedule Coordination', 'Fare Integration', 'Accessibility Planning',
                       'Customer Feedback Management', 'Community Events', 'User Surveys',
                       'Performance Metrics Analysis', 'Predictive Modeling', 'Data Visualization']
G.add_nodes_from(level_1_capabilities)

# Add edges for Level 1 capabilities
G.add_edges_from([('Urban Mobility Solutions Development', 'Research and Development'),
                  ('Urban Mobility Solutions Development', 'Prototyping'),
                  ('Urban Mobility Solutions Development', 'Testing and Validation'),
                  ('Ridepooling Service Operations', 'Service Planning'),
                  ('Ridepooling Service Operations', 'Driver Management'),
                  ('Ridepooling Service Operations', 'Customer Support'),
                  ('Fleet Management', 'Vehicle Maintenance'),
                  ('Fleet Management', 'Asset Tracking'),
                  ('Fleet Management', 'Fuel Management'),
                  ('Infrastructure Management', 'Network Security'),
                  ('Infrastructure Management', 'Facility Maintenance'),
                  ('Infrastructure Management', 'Technology Integration'),
                  ('Multimodal Transportation Integration', 'Seamless Transfer Solutions'),
                  ('Multimodal Transportation Integration', 'Intermodal Connectivity'),
                  ('Public Transit Integration', 'Schedule Coordination'),
                  ('Public Transit Integration', 'Fare Integration'),
                  ('Public Transit Integration', 'Accessibility Planning'),
                  ('Co-Creation and User Engagement', 'Customer Feedback Management'),
                  ('Co-Creation and User Engagement', 'Community Events'),
                  ('Co-Creation and User Engagement', 'User Surveys'),
                  ('Data Analysis and Modeling', 'Performance Metrics Analysis'),
                  ('Data Analysis and Modeling', 'Predictive Modeling'),
                  ('Data Analysis and Modeling', 'Data Visualization')])



# Use Graphviz to lay out the graph
pos = graphviz_layout(G, prog="dot", args='-Grankdir=TB -Granksep=2 -Gnodesep=1')

# Visualize the graph
plt.figure(figsize=(20, 20))
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=8, arrowsize=15, min_target_margin=25)
plt.title('Integrated Capabilities Network')

# Save the graph as a PDF
plt.savefig("data/capability_map.pdf", format="PDF")

plt.show()
