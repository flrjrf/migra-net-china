import pandas as pd
import networkx as nx

# Build network with geographic data full data from all datapoints. Only used for plotting
def build_geo_network(df: pd.DataFrame, start_year: int, end_year: int) -> nx.DiGraph:
    G = nx.DiGraph()
    
    # Helper to get node ID and Coords
    def get_node_info(row, prefix) -> tuple[str, tuple[float, float]]:
        # Determine column names based on prefix
        name_col = 'current_city' if prefix == 'current' else f'{prefix}_Name_Prefecture'
        lon_col = f'{prefix}_lon'
        lat_col = f'{prefix}_lat'
        
        node_id = row[name_col]
        coords = (row[lon_col], row[lat_col])
        return node_id, coords

    for idx, row in df.iterrows():
        # Extract info
        u_name, u_pos = get_node_info(row, 'hometown')
        v1_name, v1_pos = get_node_info(row, 'first')
        v2_name, v2_pos = get_node_info(row, 'current')
        
        # Add Nodes with Position Data (Idempotent)
        G.add_node(u_name, pos=u_pos)
        G.add_node(v1_name, pos=v1_pos)
        G.add_node(v2_name, pos=v2_pos)

        # Logic: Hometown -> First
        if start_year <= row['year_first_flow'] <= end_year:
            is_intra = (u_name == v1_name)
            if G.has_edge(u_name, v1_name):
                G[u_name][v1_name]['weight'] += 1
            else:
                G.add_edge(u_name, v1_name, weight=1, type='within' if is_intra else 'inter')

        # Logic: First -> Current
        # Only add if locations differ (otherwise it's a "stay")
        if (start_year <= row['year_current_flow'] <= end_year) and (v1_name != v2_name):
            is_intra = (v1_name == v2_name)
            if G.has_edge(v1_name, v2_name):
                G[v1_name][v2_name]['weight'] += 1
            else:
                G.add_edge(v1_name, v2_name, weight=1, type='within' if is_intra else 'inter')
                
    return G

def build_migration_network(df: pd.DataFrame, year: int) -> nx.DiGraph:
    """
    Build directed migration network for a specific year.
    
    Parameters:
    -----------
    df : DataFrame
        Migration data
    year : int
        Year to analyze
        either year_first_flow or year_current_flow matches this year.
    
    Returns:
    --------
    G : nx.DiGraph
        Network with nodes (cities) and edges (migration flows)
    """
    G = nx.DiGraph()
    
    # Filter data for the year
    year_data = df[
        ((df['year_first_flow'] == year) | (df['year_current_flow'] == year))
    ]

    
    for _, row in year_data.iterrows():
        # Extract city names and coordinates
        hometown = row['hometown_Name_Prefecture']
        first_city = row['first_Name_Prefecture']
        current_city = row['current_city']
        
        hometown_pos = (row['hometown_lon'], row['hometown_lat'])
        first_pos = (row['first_lon'], row['first_lat'])
        current_pos = (row['current_lon'], row['current_lat'])
        
        # Add nodes with positions
        G.add_node(hometown, pos=hometown_pos, 
                  lon=row['hometown_lon'], lat=row['hometown_lat'])
        G.add_node(first_city, pos=first_pos,
                  lon=row['first_lon'], lat=row['first_lat'])
        G.add_node(current_city, pos=current_pos,
                  lon=row['current_lon'], lat=row['current_lat'])
        
        # Add edges for flows in this year
        if row['year_first_flow'] == year and hometown != first_city:
            if G.has_edge(hometown, first_city):
                G[hometown][first_city]['weight'] += 1
            else:
                G.add_edge(hometown, first_city, weight=1)
        
        if row['year_current_flow'] == year and first_city != current_city:
            if G.has_edge(first_city, current_city):
                G[first_city][current_city]['weight'] += 1
            else:
                G.add_edge(first_city, current_city, weight=1)
    
    # Remove isolated nodes
    G.remove_nodes_from(list(nx.isolates(G)))
    
    return G
