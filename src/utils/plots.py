import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import geopandas as gpd

from config import BaseConfig


def plot_migration_map_local(G, config: BaseConfig):
    fig, ax = plt.subplots(figsize=(16, 12))
    china_map = gpd.read_file(config.china_provinces_path)


    # 2. Plot the Map
    # Facecolor = province fill, Edgecolor = border lines
    china_map.plot(ax=ax, color='#f0f0f0', edgecolor='#d9d9d9', linewidth=0.8)
    
    ax.set_title("Chinese Migration Network", fontsize=20, fontweight='bold', pad=20)
    
    # 3. Draw Nodes (Cities)
    pos = nx.get_node_attributes(G, 'pos')
    
    for node, (lon, lat) in pos.items():
        if lon < 70 or lon > 140 or lat < 10 or lat > 60:
            continue # Skip bad coordinates
            
        # Node size based on connections
        degree = G.degree(node)
        size = degree * 20 + 30 
        
        # Draw node
        ax.scatter(lon, lat, s=size, c='#3b82f6', edgecolors='white', linewidth=1, zorder=5, alpha=0.9)
        
        # Label top cities only (to avoid clutter)
        if degree > 2: 
            ax.text(lon + 0.5, lat + 0.3, node, fontsize=9, fontweight='bold', color='#333333', zorder=6)

    # 4. Draw Curved Edges
    for u, v, data in G.edges(data=True):
        if u not in pos or v not in pos or u == v:
            continue
            
        start = pos[u]
        end = pos[v]
        edge_type = data.get('type', 'inter')
        weight = data.get('weight', 1)
        
        # Logic: Red dashed for internal, Solid black for external
        if edge_type == 'within':
             # Skip or draw very subtly
             color = '#ef4444' 
             style = ':'
             alpha = 0.5
        else:
             color = '#1f2937'
             style = '-'
             alpha = 0.4
        
        # Draw Curve
        arrow = patches.FancyArrowPatch(
            start, end,
            connectionstyle="arc3,rad=0.2",
            color=color,
            alpha=alpha,
            linewidth=min(weight * 0.5, 3),
            linestyle=style,
            arrowstyle="-|>", 
            mutation_scale=10, 
            zorder=4
        )
        ax.add_patch(arrow)

    # Focus on the mainland area
    ax.set_xlim(73, 136)
    ax.set_ylim(18, 54)
    plt.axis('off')
    plt.tight_layout()
    plt.show()
