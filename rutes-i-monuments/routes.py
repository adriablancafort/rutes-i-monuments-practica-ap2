from monuments import Monuments, Monument
from typing import TypeAlias
from dataclasses import dataclass
from staticmap import StaticMap, Line
from simplekml import Kml
import numpy as np
import networkx as nx
from haversine import haversine
from scipy.spatial import KDTree
from segments import Box, Point, get_segments
from graphmaker import make_graph, simplify_graph


@dataclass
class Point:
    lat: float
    lon: float


# S'ha de decidir com ha de ser el dataclass Route per poder dibuixar-lo bé
@dataclass
class Route:
    name: str
    path: list[Point]


Routes: TypeAlias = list[Route]


def closest_point(graph: nx.Graph, point: Point) -> int:
    """Returns the closest point of the graph to the given point."""

    # Create a list of all node positions
    node_positions:list[tuple[int,int]] = np.array([graph.nodes[node]['pos'] for node in graph.nodes()])
    #print(node_positions)
    # Create a KDTree from the node positions
    tree = KDTree(node_positions)
    # Query the KDTree for the closest point to the given point
    distance, index = tree.query([point.lat,point.lat])

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
        graph.edges[edge]['weight'] = distance/1000
        graph.edges[edge]['col'] = "black"
    # Initialize routes list

    _, paths = nx.single_source_dijkstra(graph, source=start)
    routes_returner: Routes = []
    for monu in endpoints:
        loc :Point = monu.location
        end_node = closest_point(graph,loc)
        list_of_nodes:Route = Route(monu.name,[Point(graph.nodes[item]['pos'][0],graph.nodes[item]['pos'][1]) for item in paths[end_node]])
        for item in paths[end_node]:
            graph.nodes[item]['color'] = 'yellow'
        routes_returner.append(list_of_nodes)
        
    return routes_returner

def color_routes(graph: nx.Graph, routes:Routes) -> None:
    for route in routes:
        for i in range(len(route) - 1):
            node1, node2 = route[i], route[i + 1]
            graph[node1]['color'] = 'yellow'
            graph[node2]['color'] = 'yellow'
            graph[node1][node2]['color'] = 'red'
            graph[node2][node1]['color'] = 'red'


graph = nx.Graph()
centr = [(1,2),(2,5),(4,2),(3,2),(1,5)]
for i, centroid in enumerate(centr):
    graph.add_node(i, pos=centroid,col="black")


graph.add_edge(0,1,col="blue",weight = 0)
graph.add_edge(0,2,col="blue",weight = 0)
graph.add_edge(2,3,col="blue",weight = 0)
graph.add_edge(3,4,col="blue",weight = 0)
graph.add_edge(4,1,col="blue",weight = 0)
graph.add_edge(2,1,col="blue",weight = 0)

for edge in graph.edges():
    start_node = graph.nodes[edge[0]]['pos']
    end_node = graph.nodes[edge[1]]['pos']
    distance = abs(end_node[0]-start_node[0]) + abs(end_node[1]-start_node[1])
    graph.edges[edge]['weight'] = distance


print(find_routes(graph,Point(1,2),[Monument("hla",Point(3,2)),Monument("hla",Point(4,1))]))

