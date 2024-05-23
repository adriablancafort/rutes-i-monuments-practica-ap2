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


def cleaner_printer(graph: nx.Graph) -> None:
    edges = list(graph.edges)
    m = len(edges)
    for i in range(m - 1, 0, -1):
        graph.remove_edge(edges[i][0], edges[i][1])
        name_plot = f"Edge number:{i} removed"
        export_KML(graph, name_plot)
