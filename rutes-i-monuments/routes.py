from monuments import Monuments
from typing import TypeAlias
from dataclasses import dataclass
from staticmap import StaticMap, Line
from simplekml import Kml
import numpy as np
import networkx as nx
from haversine import haversine
from scipy.spatial import KDTree


@dataclass
class Point:
    lat: float
    lon: float


# S'ha de decidir com ha de ser el dataclass Route per poder dibuixar-lo bé
@dataclass
class Route:
    list[Point]


Routes: TypeAlias = list[Route]


def closest_point(graph: nx.Graph, point: Point) -> int:
    """Returns the closest point of the graph to the given point."""

    # Create a list of all node positions
    node_positions = np.array([graph.nodes[node]['pos'] for node in graph.nodes()])

    # Create a KDTree from the node positions
    tree = KDTree(node_positions)

    # Query the KDTree for the closest point to the given point
    distance, index = tree.query(point)

    # Return the corresponding node
    return list(graph.nodes())[index]


# No definitiu. S'ha d'implementar amb haversine
def find_routes(graph: nx.Graph, start: Point, endpoints: Monuments) -> Routes:
    """Find the shortest route between the starting point and all the endpoints."""
    # Find the closest endpoint of the graph to the start
    start = closest_point(graph, start)

    # Add haversine distances as edge attributes
    for edge in graph.edges():
        start_node = graph.nodes[edge[0]]['pos']
        end_node = graph.nodes[edge[1]]['pos']
        distance = haversine(start_node, end_node)
        graph.edges[edge]['weight'] = distance
    # Initialize routes list

    _, paths = nx.single_source_dijkstra(graph, source=start)
    routes_returner: Routes = []
    for monu in endpoints:
        loc :Point = monu.location
        end_node = closest_point(graph,loc)
        routes_returner.append(paths[end_node])

    return routes_returner




# No definitiu
def export_PNG(routes: Routes, filename: str) -> None:
    """Export the routes to a PNG file using staticmap."""

    map = StaticMap(800, 800)

    for route in routes:
        for i in range(len(route) - 1):
            start_node = route[i]['pos']
            end_node = route[i + 1]['pos']

            line = Line([(start_node[1], start_node[0]), (end_node[1], end_node[0])], 'red', 3)
            map.add_line(line)

    image = map.render()
    image.save(filename)


# No definitiu
def export_KML(routes: Routes, filename: str) -> None:
    """Export the routes to a KML file."""

    kml = Kml()

    for route in routes:
        for i in range(len(route) - 1):
            start_node = route[i]['pos']
            end_node = route[i + 1]['pos']

            kml.newlinestring( coords=[(start_node[1], start_node[0]), (end_node[1], end_node[0])])

    kml.save(filename)


"""
graph = nx.Graph()
centr = [(1,2),(2,5),(4,2),(3,2),(1,5)]
for i, centroid in enumerate(centr):
    graph.add_node(i, pos=centroid)


graph.add_edge(0,1)
graph.add_edge(0,2)
graph.add_edge(2,3)
graph.add_edge(3,4)
graph.add_edge(4,1)
graph.add_edge(2,1)

for edge in graph.edges():
    start_node = graph.nodes[edge[0]]['pos']
    end_node = graph.nodes[edge[1]]['pos']
    distance = abs(end_node[0]-start_node[0]) + abs(end_node[1]-start_node[1])
    graph.edges[edge]['weight'] = distance


print(find_routes(graph,0,[4]))
"""