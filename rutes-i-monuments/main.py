"""
Llegeix les entrades, pregunta què fer i crida les funcions adequades
"""

from segments import Box, Point
BOX_EBRE = Box(Point(0.5739316671, 40.5363713), Point(0.9021482, 40.79886535))


# Segments

# Per poder llegir monuments.dat és necessari importar el tipu Segment
from segments import Segment, get_segments, show_segments

BOX_EBRE = Box(Point(0.5739316671, 40.5363713), Point(0.9021482, 40.79886535))

#print(get_segments(BOX_EBRE, "ebre.dat"))
show_segments(get_segments(BOX_EBRE, "../ebre_filtrat.dat"), "./imatges/ebre_test_filtrat.png")


# Monuments

## Per poder llegir monuments.dat és necessari importar els tipus Monumen i Point
from monuments import get_monuments, Monument, Point

#print(get_monuments("monuments.dat"))

# Graphmaker

from graphmaker import make_graph, simplify_graph

from segments import Segment, get_segments # temporal

graph = make_graph(get_segments(BOX_EBRE, "../ebre_filtrat.dat"), 150)
graph_simplificat = simplify_graph(graph, 5)
#for node,atrr in graph.nodes(data=True):
 #   print(atrr)
#for edge in graph.edges():
 #   print(graph.nodes[edge[0]])

from viewer import export_KML, export_PNG
export_PNG(graph, "./imatges/ebre_graph_filtrat.png")
export_PNG(graph_simplificat, "./imatges/ebre_graph_simplificat_filtrat.png")
export_KML(graph, "./imatges/ebre_graph_filtrat.kml")
export_KML(graph_simplificat, "./imatges/ebre_graph_simplificat_filtrat.kml")


# Per fer:

# comprovar make graph i simplify graph
# netejar ebre.dat (els graph i graph simplificat no serveixen perquè no es guarden)
# comprovar routes
# filtrar monuments per Box
# comprovar el routes 
# interfaç del main.py
# readme

