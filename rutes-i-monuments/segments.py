from typing import TypeAlias, Optional
from dataclasses import dataclass
from requests import get
from gpxpy import parse
from pickle import dump, load
from haversine import haversine  # type: ignore
from staticmap import StaticMap, Line  # type: ignore


@dataclass
class Point:
    lat: float
    lon: float


@dataclass
class Segment:
    start: Point
    end: Point


@dataclass
class Box:
    bottom_left: Point
    top_right: Point


Segments: TypeAlias = list[Segment]


# The type of p1 and p2 depends on the result of the openstreetmap API.
# We left it with type any to avoid future type conflicts in case of API changes.
def filter_segment(p1: any, p2: any) -> bool:  # type: ignore
    """Validate a segment based on time and distance."""

    max_distance = 500.0  # meters
    max_time = 15  # seconds
    time_epsilon = 0.000001  # seconds

    dist = haversine((p1.latitude, p1.longitude), (p2.latitude, p2.longitude))  # type: ignore
    time_delta = (p2.time - p1.time).total_seconds()  # type: ignore

    # The time difference between two points is more than the maximum allowed time
    if time_delta > max_time:
        return False

    # The distance between two points is more than the maximum allowed distance
    if dist > max_distance:
        return False

    # The time difference between two points is effectively zero (less than a very small number)
    if time_delta < time_epsilon:
        return False

    return True


def download_segments(box: Box) -> Segments:
    """Download all segments in the box."""

    segments: Segments = []

    BOX = f"{box.bottom_left.lat},{box.bottom_left.lon},{box.top_right.lat},{box.top_right.lon}"
    page = 0

    while True:
        url = (
            f"https://api.openstreetmap.org/api/0.6/trackpoints?bbox={BOX}&page={page}"
        )
        response = get(url)
        gpx_content = response.content.decode("utf-8")
        gpx = parse(gpx_content)

        if len(gpx.tracks) == 0:
            break
        for track in gpx.tracks:
            for segment in track.segments:
                if all(point.time is not None for point in segment.points):
                    # Sort points consecutively
                    segment.points.sort(key=lambda p: p.time)  # type: ignore
                    for i in range(len(segment.points) - 1):
                        # Add segments of consecutive points
                        p1, p2 = segment.points[i], segment.points[i + 1]
                        if filter_segment(p1, p2):
                            segments.append(
                                Segment(
                                    Point(p1.latitude, p1.longitude),
                                    Point(p2.latitude, p2.longitude),
                                )
                            )
        page += 1

    return segments


def write_segments_to_file(segments: Segments, filename: str) -> None:
    """Write the list of segments to a file."""

    with open(filename, "wb") as f:
        dump(segments, f)


def read_segments_from_file(filename: str) -> Optional[Segments]:
    """Read the list of segments from a file."""

    try:
        with open(filename, "rb") as f:
            monuments = load(f)
        return monuments
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return None


def get_segments(box: Box, filename: str) -> Segments:
    """
    Get all segments in the box.
    If filename exists, load segments from the file.
    Otherwise, download segments in the box and save them to the file.
    """

    segments = read_segments_from_file(filename)
    if not segments:
        segments = download_segments(box)
        write_segments_to_file(segments, filename)
    return segments


def show_segments(segments: Segments, filename: str) -> None:
    """Show all segments in a PNG file using staticmap."""

    map = StaticMap(800, 800)

    for segment in segments:
        # Create a line for each segment
        line = Line(
            (
                (segment.start.lon, segment.start.lat),
                (segment.end.lon, segment.end.lat),
            ),
            "blue",
            3,
        )
        map.add_line(line)  # type: ignore

    image = map.render()  # type: ignore
    image.save(filename)  # type: ignore
