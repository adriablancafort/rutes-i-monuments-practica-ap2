from monuments import Monuments
from typing import TypeAlias
from dataclasses import dataclass
from staticmap import StaticMap, Line
from simplekml import Kml
import networkx as nx
from haversine import haversine


@dataclass
class Point:
    lat: float
    lon: float


# S'ha de decidir com ha de ser el dataclass Route per poder dibuixar-lo bé
@dataclass
class Route:


Routes: TypeAlias = list[Route]


# No definitiu. S'ha d'implementar amb haversine
def find_routes(graph: nx.Graph, start: Point, endpoints: Monuments) -> Routes:
    """Find the shortest route between the starting point and all the endpoints."""

    # Add haversine distances as edge attributes
    for edge in graph.edges():
        start_node = graph.nodes[edge[0]]['pos']
        end_node = graph.nodes[edge[1]]['pos']
        distance = haversine(start_node, end_node)
        graph.edges[edge]['distance'] = distance

    # Convert Monuments to list of nodes
    endpoints = list(endpoints)

    # Initialize routes list
    routes: Routes = []

    # Find shortest path to each endpoint
    for endpoint in endpoints:
        try:
            path = nx.dijkstra_path(graph, start, endpoint, weight='distance')
            routes.append(path)
        except nx.NetworkXNoPath:
            print(f"No path found from {start} to {endpoint}")

    return routes


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
