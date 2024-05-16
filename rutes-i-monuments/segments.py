from typing import TypeAlias
from dataclasses import dataclass
from requests import get
from gpxpy import parse
from pickle import dump, load
from staticmap import StaticMap, Line


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


def read_segments_from_file(filename: str) -> Segments | None:
    """Read the list of segments from a file."""

    try:
        with open(filename, "rb") as f:
            segments = load(f)
        return segments
    except:
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
        map.add_line(line)

    image = map.render()
    image.save(filename)


# BOX_EBRE = Box(Point(0.5739316671, 40.5363713), Point(0.9021482, 40.79886535))
# print(download_segments(BOX_EBRE))
# print(get_segments(BOX_EBRE, "ebre.dat"))
# show_segments(get_segments(BOX_EBRE, "ebre.dat"), "ebre.png")
