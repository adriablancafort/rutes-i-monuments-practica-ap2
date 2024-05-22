from staticmap import StaticMap, Line
from simplekml import Kml
import networkx as nx
from segments import Box, Point, get_segments
from graphmaker import make_graph, simplify_graph



def export_PNG(graph: nx.Graph, filename: str) -> None:
    """Export the graph to a PNG file using staticmap."""

    map = StaticMap(800, 800)

    for edge in graph.edges():
        start_node = graph.nodes[edge[0]]["pos"]
        end_node = graph.nodes[edge[1]]["pos"]

        line = Line(
            [(start_node[1], start_node[0]), (end_node[1], end_node[0])], "red", 3
        )
        map.add_line(line)

    image = map.render()
    image.save(filename)


def export_KML(graph: nx.Graph, filename: str) -> None:
    """Export the graph to a KML file."""

    kml = Kml()

    for edge in graph.edges():
        start_node = graph.nodes[edge[0]]["pos"]
        end_node = graph.nodes[edge[1]]["pos"]

        kml.newlinestring(
            coords=[(start_node[1], start_node[0]), (end_node[1], end_node[0])]
        )

    kml.save(filename)


BOX_EBRE = Box(Point(0.5739316671, 40.5363713), Point(0.9021482, 40.79886535))
graph = simplify_graph(make_graph(get_segments(BOX_EBRE, "ebre.dat"), 100), 5)
export_KML(graph, "ebre_simplificat.kml")
