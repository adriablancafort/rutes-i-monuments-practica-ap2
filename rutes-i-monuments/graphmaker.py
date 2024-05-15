import networkx as nx
from segments import Box,Segment, Point,Segments
from sklearn.cluster import KMeans
import numpy as np
from collections import defaultdict
from dataclasses import dataclass
from data_funcitons import latlon_to_xy,centroid

def make_graph(segments: Segments, K: int) -> nx.Graph:
    # Extract all unique points
    point_list = []
    point_index = {}  # Map each point to an index for clustering
    point_index2 = {}
    index = 0
    for segment in segments:
        for point in [segment.start, segment.end]:
            if (point.lat, point.lon) not in point_index:
                x,y = latlon_to_xy((point.lat,point.lon))
                point_index[(point.lat,point.lon)] = index
                point_index2[(x,y)] = index
                point_list.append([x, y])
                index += 1

    # Array of points for clustering
    points_array = np.array(point_list)

    # Clustering points
    kmeans = KMeans(n_clusters=K, random_state=0).fit(points_array)
    labels = kmeans.labels_

    # Create a graph
    G = nx.Graph()

    # Add nodes with cluster label as node attributes
    classificator = [[] for _ in range(K)]
    for i in range(len(point_list)):
        classificator[labels[i]].append(point_list[i])

    for l in range(K):
        G.add_node(l,center=centroid(classificator[l]), monument=False)
    # Add edges based on original segments, using cluster information
    for segment in segments:
        start_index = point_index[(segment.start.lat, segment.start.lon)]
        end_index = point_index[(segment.end.lat, segment.end.lon)]
        start_cluster = labels[start_index]
        end_cluster = labels[end_index]
        
        # Connect clusters if the original points had a segment between them
        if start_cluster != end_cluster:
            G.add_edge(start_index, end_index)
    return G





def simplify_graph(graph: nx.Graph, epsilon: float) -> nx.Graph:
    simplified_graph: nx.Graph = graph.copy()
    for g2,attributes2 in list(graph.nodes(data=True)):
        neighbours = list(graph.neighbors(g2,data=True))
        if len(neighbours) == 2:
            g1,g3 = neighbours
            pos2 = np.array(attributes2["center"])
            pos1 = np.array(graph.nodes[g1]["center"])
            pos3 = np.array(graph.nodes[g3]["center"])
            vector1 = pos2 - pos1
            vector3 = pos3 - pos2
            angle:float = np.degrees(np.arccos(np.clip(np.dot(vector1, vector3)\
                     / (np.linalg.norm(vector1) * np.linalg.norm(vector3)), -1.0, 1.0)))
            
            if abs(angle - 180) < epsilon:
                simplified_graph.remove_node(g2)
                simplified_graph.add_edge(g1,g3)
    
    return simplified_graph



