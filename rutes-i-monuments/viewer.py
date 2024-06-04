from staticmap import StaticMap, Line
from simplekml import Kml
import networkx as nx


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
