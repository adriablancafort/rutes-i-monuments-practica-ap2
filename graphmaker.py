from segments import Segments
import numpy as np
import networkx as nx
from sklearn.cluster import KMeans
from scipy.spatial import KDTree
import networkx as nx


def make_graph(segments: Segments, clusters: int) -> nx.Graph:
    """Make a graph from the segments."""

    # Extract points from segments
    points = np.array(
        [
            (point.lat, point.lon)
            for segment in segments
            for point in [segment.start, segment.end]
        ]
    )

    # Fit KMeans model
    kmeans = KMeans(n_clusters=clusters, random_state=0).fit(points)

    # Create a KDTree for efficient nearest centroid lookup
    tree = KDTree(kmeans.cluster_centers_)

    # Create a graph
    G = nx.Graph()

    # Add nodes to the graph
    for i, centroid in enumerate(kmeans.cluster_centers_):
        G.add_node(i, pos=centroid, color="blue")

    # Add edges to the graph
    for segment in segments:
        start_cluster = tree.query([segment.start.lat, segment.start.lon])[1]
        end_cluster = tree.query([segment.end.lat, segment.end.lon])[1]
        if start_cluster != end_cluster:
            G.add_edge(start_cluster, end_cluster, color="black")

    return G


def simplify_graph(graph: nx.Graph, epsilon: float) -> nx.Graph:
    """Simplify the graph."""

    # Create a copy of the graph to modify
    simplified_graph = graph.copy()

    # Iterate over all nodes in the graph
    for node in graph.nodes():
        # Check if the node has exactly two neighbors
        if len(list(graph.neighbors(node))) == 2:
            neighbors = list(graph.neighbors(node))
            # Calculate the vector between the node and its neighbors
            v1 = np.array(graph.nodes[neighbors[0]]["pos"]) - np.array(
                graph.nodes[node]["pos"]
            )
            v2 = np.array(graph.nodes[neighbors[1]]["pos"]) - np.array(
                graph.nodes[node]["pos"]
            )
            # Calculate the angle between the vectors
            angle = angle_between(v1, v2)
            # If the angle is close to 180 degrees, remove the node and add an edge between its neighbors
            if abs(180 - angle) < epsilon:
                simplified_graph.remove_node(node)
                simplified_graph.add_edge(neighbors[0], neighbors[1])
    return simplified_graph


def angle_between(v1, v2):
    """Return the angle in degrees between vectors 'v1' and 'v2'."""

    v1_u = v1 / np.linalg.norm(v1)
    v2_u = v2 / np.linalg.norm(v2)
    return np.degrees(np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)))
