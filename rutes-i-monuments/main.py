# Segments

# Per poder llegir monuments.dat és necessari importar el tipu Segment
from segments import Point, Segment, Box, get_segments, show_segments

BOX_EBRE = Box(Point(0.5739316671, 40.5363713), Point(0.9021482, 40.79886535))

# show_segments(get_segments(BOX_EBRE, "ebre_filtrat.dat"), "ebre_segments_filtrat.png")


# Monuments

# Per poder llegir monuments.dat és necessari importar els tipus Monumen i Point
from monuments import get_monuments, filter_monuments, Monument, Point

monuments_filtrats = filter_monuments(get_monuments("monuments.dat"), BOX_EBRE)


# Graphmaker

from graphmaker import make_graph, simplify_graph

graph = make_graph(get_segments(BOX_EBRE, "ebre_filtrat.dat"), 160)
#graph_simplificat = simplify_graph(graph, 5)

"""
# Viewer

from viewer import export_KML, export_PNG

export_PNG(graph, "ebre_graph_filtrat.png")
export_PNG(graph_simplificat, "ebre_graph_simplificat_filtrat.png")
export_KML(graph, "ebre_graph_filtrat.kml")
export_KML(graph_simplificat, "ebre_graph_simplificat_filtrat.kml")
"""

# Monuments


# Routes

from rutes_biel import find_routes, routes_PNG, routes_KML

start = Point(lat=40.6683333, lon=0.5872222)

routes = find_routes(graph, start, monuments_filtrats)

routes_PNG(routes, "rutes.png")


# Per fer:

# comprovar el routes 
# interfaç del main.py
# readme
