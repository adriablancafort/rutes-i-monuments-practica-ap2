from staticmap import StaticMap, Line
from monuments import Monuments, Monument
from typing import TypeAlias
from dataclasses import dataclass
from staticmap import StaticMap, CircleMarker, Line
import simplekml
import networkx as nx
from haversine import haversine
from scipy.spatial import KDTree
from segments import Box, Point, get_segments
from graphmaker import make_graph, simplify_graph
from segments import Segments, Segment


@dataclass
class Route:
    name: str
    path: list[Point]


Routes: TypeAlias = list[Route]


@dataclass
class Routes2:
    start: Point
    edges: dict[Monument, Segments]


def closest_point(graph: nx.Graph, point: Point) -> int:
    """Returns the closest point of the graph to the given point."""
    closest_node = None
    closest_distance = float('inf')

    for node in graph.nodes(data=True):
        node_point = (node[1]['pos'][0], node[1]['pos'][1])
        distance = haversine(node_point, (point.lat, point.lon))
        if distance < closest_distance:
            closest_distance = distance
            closest_node = node[0]

    return closest_node


def find_routes(graph: nx.Graph, start: Point, endpoints: Monuments) -> Routes2:
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
        loc: Point = monu.location
        end_node = closest_point(graph, loc)
        list_of_nodes: Route = Route(monu.name, [Point(
            graph.nodes[item]['pos'][0], graph.nodes[item]['pos'][1]) for item in paths[end_node]])
        for item in paths[end_node]:
            graph.nodes[item]['color'] = 'yellow'
        routes_returner.append(list_of_nodes)

    classi: dict[Monument, Segments] = {}
    for index, monu in enumerate(endpoints):
        rut: Route = routes_returner[index].path
        all_seg: Segments = []
        if (len(rut) == 1):
            classi[monu] = [Segment(rut[0], rut[0])]
        else:
            all_seg.append(Segment(rut[0], rut[1]))
            for i in range(1, len(rut)-1):
                all_seg.append(Segment(rut[i], rut[i+1]))
            classi[monu] = all_seg

    return Routes2(Point(graph.nodes[start]['pos'][0], graph.nodes[start]['pos'][1]), classi)


def color_routes(graph: nx.Graph, routes: Routes) -> None:
    for route in routes:
        for i in range(len(route) - 1):
            node1, node2 = route[i], route[i + 1]
            graph[node1]['color'] = 'yellow'
            graph[node2]['color'] = 'yellow'
            graph[node1][node2]['color'] = 'red'
            graph[node2][node1]['color'] = 'red'


def routes_PNG(routes: Routes2, filename: str) -> None:
    """Show all routes in a PNG file using staticmap."""

    map = StaticMap(800, 800)

    # Add start point
    start_marker = CircleMarker(
        (routes.start.lon, routes.start.lat), 'green', 10)
    map.add_marker(start_marker)

    for monument, segments in routes.edges.items():
        for segment in segments:
            # Create a line for each segment
            line = Line(
                (
                    (segment.start.lon, segment.start.lat),
                    (segment.end.lon, segment.end.lat),
                ),
                "blue",
                3,
            )
            map.add_line(line)

        # Add monument end point
        end_marker = CircleMarker((monument.location.lon, monument.location.lat), 'black', 10)
        map.add_marker(end_marker)

    image = map.render()
    image.save(filename)


def routes_KML(groutes: Routes, filename: str) -> None:
    """Export the graph to a KML file."""

    kml_graph = simplekml.Kml()
    kml_graph.newpoint(name="START", coords=[(groutes.start.lon, groutes.start.lat)])

    for monument, segments in groutes.edges.items():

        # Add the names
        kml_graph.newpoint(name=monument.name.split('.')[1], coords=[(monument.location.lon, monument.location.lat)])

        # Add the edges
        for segment in segments:
            start_point = (segment.start.lon, segment.start.lat)
            end_point = (segment.end.lon, segment.end.lat)
            lin = kml_graph.newlinestring(coords=[start_point, end_point])
            lin.style.linestyle.color = simplekml.Color.red
            lin.style.linestyle.width = 5

    kml_graph.save(filename)


def routes_KML(groutes: Routes, filename: str) -> None:
    """Export the graph to a KML file."""
    kml_graph = simplekml.Kml()
    kml_graph.newpoint(name="START", coords=[(groutes.start.lon, groutes.start.lat)])

    for monument, segments in groutes.edges.items():
        
        # Add the names
        if '.' in monument.name:
            kml_graph.newpoint(name=monument.name.split('.')[1], coords=[(monument.location.lon, monument.location.lat)])
        else:
            kml_graph.newpoint(name=monument.name, coords=[(monument.location.lon, monument.location.lat)])
        
        # Add the edges
        for segment in segments:
            start_point = (segment.start.lon, segment.start.lat)
            end_point = (segment.end.lon, segment.end.lat)
            lin = kml_graph.newlinestring(coords=[start_point, end_point])
            lin.style.linestyle.color = simplekml.Color.red
            lin.style.linestyle.width = 5

    kml_graph.save(filename)
