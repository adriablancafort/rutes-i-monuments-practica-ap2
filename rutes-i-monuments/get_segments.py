import requests
import gpxpy
from segments import Box,Segment, Point



def get_segments(box: Box):
    page = 0
    BOX = f"{box.bottom_left.lat},{box.bottom_left.lon},{box.top_right.lat},{box.top_right.lon}"

    with open("data.txt", "w") as file:
        while True:
            url = f"https://api.openstreetmap.org/api/0.6/trackpoints?bbox={BOX}&page={page}"
            response = requests.get(url)
            gpx_content = response.content.decode("utf-8")
            gpx = gpxpy.parse(gpx_content)

            if len(gpx.tracks) == 0:
                break
            
            for track in gpx.tracks:
                for segment in track.segments:
                    if all(point.time is not None for point in segment.points):
                        segment.points.sort(key=lambda p: p.time)
                        for i in range(len(segment.points) - 1):
                            p1, p2 = segment.points[i], segment.points[i + 1]
                            file.write(f"{p1.latitude},{p1.longitude},{p2.latitude},{p2.longitude}\n")
            page += 1



def read_segments_from_file()->list[Segment]:
    segments_returner:list[Segment] = []
    with open("data.txt", "r") as file:
        for line in file:
            lat1, lon1, lat2, lon2 = map(float, line.strip().split(","))
            start = Point(lat=lat1, lon=lon1)
            end = Point(lat=lat2, lon=lon2)
            segment = Segment(start=start, end=end)
            segments_returner.append(segment)
    return segments_returner


box = Box(bottom_left=Point(lat=0.5739316671, lon=40.5363713), top_right=Point(lat=0.9021482, lon=40.79886535))
get_segmentss(box)