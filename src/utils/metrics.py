import networkx as nx
import numpy as np

def compute_global_metrics(G: nx.Graph) -> dict:
    """
    Compute basic network topological properties for any Graph.
    Similar to Figure 2 in the maritime paper.

    Parameters:
    -----------
    G : nx.Graph
        Input network graph (can be directed or undirected)
    Returns:
    --------
    props : dict
        Dictionary of computed network properties
        n_nodes: Number of nodes
        n_edges: Number of edges
        density: Network density
        avg_degree: Average node degree
        max_degree: Maximum node degree
        avg_path_length: Average shortest path length
        diameter: Network diameter
        lcc_fraction: Fraction of nodes in largest connected component
        avg_clustering: Average clustering coefficient
        transitivity: Network transitivity
        assortativity: Degree assortativity coefficient
    """
    props = {}
    
    # Basic stats
    props['n_nodes'] = G.number_of_nodes()
    props['n_edges'] = G.number_of_edges()
    props['density'] = nx.density(G)
    
    # Convert to undirected for some measures
    G_und = G.to_undirected()
    
    # Degree statistics
    degrees = dict(G_und.degree())
    props['avg_degree'] = np.mean(list(degrees.values()))
    props['max_degree'] = np.max(list(degrees.values()))
    
    # Path length and clustering (only for main component)
    if nx.is_connected(G_und):
        props['avg_path_length'] = nx.average_shortest_path_length(G_und)
        props['diameter'] = nx.diameter(G_und)
    else:
        # Use largest component
        largest_cc = max(nx.connected_components(G_und), key=len)
        G_lcc = G_und.subgraph(largest_cc)
        props['avg_path_length'] = nx.average_shortest_path_length(G_lcc)
        props['diameter'] = nx.diameter(G_lcc)
        props['lcc_fraction'] = len(largest_cc) / G_und.number_of_nodes()
    
    props['avg_clustering'] = nx.average_clustering(G_und)
    props['transitivity'] = nx.transitivity(G_und)
    
    # Assortativity
    props['assortativity'] = nx.degree_assortativity_coefficient(G_und)
    
    return props
