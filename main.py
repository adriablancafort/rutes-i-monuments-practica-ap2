from yogi import read

# Per poder llegir monuments.dat és necessari importar el tipu Segment
from segments import Point, Segment, Box, get_segments, show_segments

# Per poder llegir monuments.dat és necessari importar els tipus Monumen i Point
from monuments import get_monuments, filter_monuments, Monument, Point
from graphmaker import make_graph, simplify_graph
from viewer import export_KML, export_PNG
from routes import find_routes, routes_PNG, routes_KML


print("Welcome to Routes and Monuments!")
print("Which zone would you like to explore?")

print("Introduce the coordinates of the bottom left corner:")
bottom_left = Point(read(float), read(float))
print("Introduce the coordinates of the top right corner:")
top_right = Point(read(float), read(float))

BOX = Box(bottom_left, top_right)
# BOX = Box(Point(0.5739316671, 40.5363713), Point(0.9021482, 40.79886535))

print("How would you like to name this zone? (e.g. ebre)")
zone_name = read(str)

print(f"Downloading segments in {zone_name}...")
segments = get_segments(BOX, f"segments_{zone_name}.dat")
print(f"Segments in {zone_name} downloaded: {len(segments)}")

print(f"Exporting segments in {zone_name} to segments_{zone_name}.png")
show_segments(segments, f"segments_{zone_name}.png")

print("Introduce the desired number of clusters:")
clusters = read(int)

print(f"Creating graph in {zone_name}...")
graph = make_graph(segments, clusters)

print(f"Exporting graph of {zone_name} to {zone_name}_graph.png and {zone_name}_graph.kml")
export_PNG(graph, f"{zone_name}_graph.png")
export_KML(graph, f"{zone_name}_graph.kml")

print("Introduce the desired epsilon value used to simplify the graph:")
epsilon = read(float)
print(f"Simplifying graph in {zone_name}...")
graph_simplificat = simplify_graph(graph, epsilon)

print(f"Exporting simplified graph of {zone_name} to {zone_name}_graph.png and {zone_name}_graph.kml")
export_KML(graph_simplificat, "ebre_graph_simplificat_filtrat.kml")
export_PNG(graph_simplificat, "ebre_graph_simplificat_filtrat.png")

print(f"Downloading monuments from catalunyamedieval.es...")
monuments = get_monuments("monuments.dat")
print(f"Filtering monuments to {zone_name}...")
monuments_filtrats = filter_monuments(monuments, BOX)
print(f"Monuments found in {zone_name}: {len(monuments_filtrats)}")

print("Introduce the coordinates of the start point:")
start = Point(read(float), read(float))
print("Creating optimal routes...")
routes = find_routes(graph_simplificat, start, monuments_filtrats)

print(f"Exporting optimal routes from {start} to monuments inside {zone_name} saved to rutes_{zone_name}.png and rutes_{zone_name}.kml")
routes_PNG(routes, f"rutes_{zone_name}.png")
routes_KML(routes, f"rutes_{zone_name}.kml")
