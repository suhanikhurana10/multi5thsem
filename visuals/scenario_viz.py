
import matplotlib.pyplot as plt
import networkx as nx

def draw_flowchart(steps=None, title="Process Flow", output_path="flowchart.png"):
    """
    Draws a simple linear flowchart from a list of steps.
    steps: list of strings e.g. ["Start", "Process", "End"]
    """
    if not steps:
        steps = ["Start", "Process", "End"]
        
    G = nx.DiGraph()
    
    for i in range(len(steps) - 1):
        G.add_edge(steps[i], steps[i+1])
        
    pos = {}
    for i, step in enumerate(steps):
        pos[step] = (i * 2, 0) # Horizontal layout

    plt.figure(figsize=(max(6, len(steps)*2), 3))
    
    nx.draw(G, pos, with_labels=True, 
            node_shape="s",  # box shape (square-ish)
            node_color="lightblue", 
            node_size=3000, 
            font_size=10,
            font_weight="bold",
            edge_color="gray",
            arrowsize=20,
            bbox=dict(facecolor="lightblue", edgecolor="black", boxstyle="round,pad=0.3"))
            
    plt.title(title)
    plt.axis("off") # hide axis
    plt.savefig(output_path)
    plt.close()
    return output_path
