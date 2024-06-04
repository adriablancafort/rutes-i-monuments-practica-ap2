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

show_segments(segments, f"segments_{zone_name}.png")
print(f"Segments in {zone_name} saved to segments_{zone_name}.png")

print(f"Creating graph in {zone_name}...")
print("Introduce the desired number of clusters:")
clusters = read(int)
graph = make_graph(segments, clusters)

export_PNG(graph, f"{zone_name}_graph.png")
export_KML(graph, f"{zone_name}_graph.kml")
print(f"Graph in {zone_name} saved to {zone_name}_graph.png and {zone_name}_graph.kml")

print(f"Simplifying graph in {zone_name}...")
print("Introduce the desired epsilon value:")
epsilon = read(float)
graph_simplificat = simplify_graph(graph, epsilon)

export_KML(graph_simplificat, "ebre_graph_simplificat_filtrat.kml")
export_PNG(graph_simplificat, "ebre_graph_simplificat_filtrat.png")
print(f"Simplified graph in {zone_name} saved to {zone_name}_graph_simplificat.png and {zone_name}_graph_simplificat.kml")

print(f"Downloading monuments from catalunyamedieval.es...")
monuments = get_monuments("monuments.dat")
print(f"Filtering monuments to {zone_name}...")
monuments_filtrats = filter_monuments(monuments, BOX)
print(f"Monuments found in {zone_name}: {len(monuments_filtrats)}")

print("Introduce the coordinates of the start point:")
start = Point(read(float), read(float))
routes = find_routes(graph, start, monuments_filtrats)

print(f"Creating optimal routes from {start} to monuments inside {zone_name}...")
routes_PNG(routes, f"rutes_{zone_name}.png")
print(f"Optimal routes from {start} to monuments inside {zone_name} saved to rutes.png")
