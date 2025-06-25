import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict

def visualize_streamlet(consensus_data):
    G = nx.DiGraph()
    pos = {}
    colors = []
    levels = defaultdict(list)
    
    # Create nodes with positioning by epoch
    for block in consensus_data["blocks"]:
        G.add_node(block["hash"])
        levels[block["epoch"]].append(block["hash"])
    
    # Position nodes in columns by epoch
    for epoch, hashes in levels.items():
        hashes.sort()
        for i, hash_val in enumerate(hashes):
            pos[hash_val] = (epoch, -i)
    
    # Add edges and determine colors
    for block in consensus_data["blocks"]:
        if block["parent"] != "0":  # Skip genesis
            G.add_edge(block["parent"], block["hash"])
        
        # Color coding
        if block["finalized"]:
            colors.append("green")
        elif block["notarized"]:
            colors.append("yellow")
        else:
            colors.append("red")
    
    # Draw graph
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, 
            node_color=colors, 
            with_labels=True, 
            node_size=2000,
            font_size=8,
            arrows=True)
    
    # Add epoch labels
    for epoch in set(levels.keys()):
        plt.text(epoch, 1, f"Epoch {epoch}", 
                 horizontalalignment='center',
                 fontsize=12, 
                 bbox=dict(facecolor='white', alpha=0.5))
    
    plt.title("Streamlet Consensus Blockchain")
    plt.savefig("streamlet_blockchain.png")
    plt.close()