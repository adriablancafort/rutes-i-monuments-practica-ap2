from dataclasses import dataclass
from staticmap import StaticMap, CircleMarker, Line
from haversine import haversine
from typing import Callable, Any, TypeAlias
import networkx as nx
from scipy.spatial import KDTree
import simplekml
import heapq


@dataclass
class Point:
    lat: float
    lon: float

    def __hash__(self):
        return hash((self.lon, self.lat))


@dataclass
class Segment:
    start: Point
    end: Point


Segments: TypeAlias = list[Segment]


@dataclass
class Monument:
    name: str
    location: Point

    def __hash__(self):
        return hash((self.name, self.location))


Monuments: TypeAlias = list[Monument]


@dataclass
class Routes:
    start: Point
    edges: dict[Monument, Segments]


def nearest_node(graph: nx.Graph, point: Point) -> Point:
    """Returns the closest Point of the graph to another given point."""

    nodes = list(graph.nodes(data=True))
    tree = KDTree([data['pos'] for _, data in nodes])
    closest_node_index = tree.query([point.lat, point.lon])[1]
    closest_node_pos = nodes[closest_node_index][1]['pos']
    return Point(closest_node_pos[0], closest_node_pos[1])


def astar_search(graph: nx.Graph, start: Point, end: Point) -> Segments:
    """Find the shortest path between two points using the A* algorithm."""

    g: dict[Point, float] = dict()    # Distance to the start point
    f: dict[Point, float] = dict()    # Distance start-end visiting that point
    pred: dict[Point, Point] = dict()  # Predecesor of a point

    g[start] = 0
    f[start] = haversine((start.lat, start.lon), (end.lat, end.lon))
    Q: list[tuple[float, Point]] = []
    heapq.heappush(Q, (f[start], start))

    while Q:
        f_u, u = heapq.heappop(Q)
        if u == end:
            break
        # Check that it is the most updated tuple of that node
        if f_u != f[u]:
            continue
        for v in graph.neighbors(u):  # type: ignore
            cost = haversine((u.lat, u.lon), (v.lat, v.lon))
            if v not in g or g[v] > g[u] + cost:
                g[v] = g[u] + cost
                f[v] = g[v] + haversine((v.lat, v.lon), (end.lat, end.lon))
                pred[v] = u
                heapq.heappush(Q, (f[v], v))

    if end not in pred:
        return []
    segments: Segments = []
    current = end
    while current != start:
        segments.append(Segment(current, pred[current]))
        current = pred[current]

    # Segments are in inverse order, but the is no direction in this graph
    return segments


def find_routes(graph: nx.Graph, start: Point, endpoints: Monuments) -> Routes:
    """Find the shortest route between the starting point and all the
    endpoints. Precondition: The monuments and start point will be inside
    the boundaries of the graph"""

    start_point = nearest_node(graph, start)

    # Add the start point to the graph
    if start_point not in graph:
        graph.add_node(start_point, pos=(start_point.lat, start_point.lon))

    print("Start point:", start_point)

    routes: Routes = Routes(start_point, dict())

    for monument in endpoints:
        print("calculating endpoint of", monument.name, "at", monument.location)

        end_point = nearest_node(graph, monument.location)
        print(
            f"End point for {monument.name}: {end_point}, Location {monument.location}")

        route = astar_search(graph, start_point, end_point)
        if route:
            routes.edges[monument] = route
        else:
            print(
                f"There is not a connected path from {start_point} to {monument.name}")

    return routes


def routes_PNG(routes: Routes, filename: str) -> None:
    """Export the graph to a PNG file using staticmap."""

    graph = StaticMap(800, 800)
    marker = CircleMarker((routes.start.lon, routes.start.lat), "yellow", 10)
    graph.add_marker(marker)
    for segments in routes.edges.values():
        # The monument node is the first point of the first segment
        marker = CircleMarker(
            (segments[0].start.lon, segments[0].start.lat), "blue", 10
        )
        graph.add_marker(marker)

        for segment in segments:
            start_point = (segment.start.lon, segment.start.lat)
            end_point = (segment.end.lon, segment.end.lat)
            line = Line([start_point, end_point], "black", 2)
            graph.add_line(line)

    image = graph.render()
    image.save(filename)


def routes_KML(groutes: Routes, filename: str) -> None:
    """Export the graph to a KML file."""
    kml_graph = simplekml.Kml()
    kml_graph.newpoint(name="START", coords=[
                       (groutes.start.lon, groutes.start.lat)])

    for monument, segments in groutes.edges.items():
        # Add the names
        kml_graph.newpoint(
            name=monument.name.split(".")[1],
            coords=[(monument.location.lon, monument.location.lat)],
        )
        # Add the edges
        for segment in segments:
            start_point = (segment.start.lon, segment.start.lat)
            end_point = (segment.end.lon, segment.end.lat)
            lin = kml_graph.newlinestring(coords=[start_point, end_point])
            lin.style.linestyle.color = simplekml.Color.red
            lin.style.linestyle.width = 5

    kml_graph.save(filename)
