from segments import Box, Point, Segment, get_segments, show_segments
import re


def write_segments_to_file(segments: list[Segment], filename: str):
    with open(filename, 'w') as f:
        for segment in segments:
            f.write(
                f"{segment.start.lat},{segment.start.lon} - {segment.end.lat},{segment.end.lon}\n")


def read_segments_from_file(filename: str) -> list[Segment]:
    segments = []
    with open(filename, 'r') as f:
        for line in f:
            lat1, lon1, lat2, lon2 = map(float, re.findall(r"[\d\.]+", line))
            segments.append(Segment(Point(lat1, lon1), Point(lat2, lon2)))
    return segments


BOX_EBRE = Box(Point(0.5739316671, 40.5363713), Point(0.9021482, 40.79886535))

#segments = get_segments(BOX_EBRE, "ebre.dat")
#write_segments_to_file(segments, "segments.txt")


segments = read_segments_from_file("segments.txt")
show_segments(segments, "ebre_test.png")
