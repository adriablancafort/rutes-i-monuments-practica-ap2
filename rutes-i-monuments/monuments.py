from typing import TypeAlias
from dataclasses import dataclass
from bs4 import BeautifulSoup
from requests import get
from re import findall
from pickle import dump, load


@dataclass
class Point:
    lat: float
    lon: float


@dataclass
class Monument:
    name: str
    location: Point


Monuments: TypeAlias = list[Monument]


def extract_numbers(text: str) -> list[float]:
    """Given a text, returns an array with the list of numbers in it."""

    return [float(num) for num in findall(r'\d+\.?\d*', text)]


def dms_to_decimal(degrees: float, minutes: float, seconds: float) -> float:
    """Convert degrees, minutes, and seconds to decimal degrees with 7 digits of precision."""

    decimal = degrees + minutes / 60 + seconds / 3600
    return round(decimal, 7)


def calculate_coordinates(text: str) -> Point | None:
    """Given the location text, returns a Point with the coordinates of the location."""

    numbers = extract_numbers(text)
    if len(numbers) < 2:
        # No s'han trobat coordenades
        return None
    elif len(numbers) < 6:
        # Test amb coordenades en format decimal
        lat, lon = numbers[:2]
    else:
        # Text amb coordenades en format DMS
        lat_deg, lat_min, lat_sec, lon_deg, lon_min, lon_sec = numbers[:6]
        lat = dms_to_decimal(lat_deg, lat_min, lat_sec)
        lon = dms_to_decimal(lon_deg, lon_min, lon_sec)
    return Point(lat, lon)


def scrape_monument(url: str) -> Monument | None:
    """Given the url of a monument, returns its title and coordinates."""

    response = get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the title of the monument
    title = soup.find("h1", class_="entry-title").text

    # Find the coordinates of the monument
    location_elements = soup.find_all("p")
    location = None
    for element in location_elements:
        if element.find("strong", string="Localització"):
            location_link = element.find("a")
            # The coordinates are inside a link
            if location_link:
                location = location_link.text
            # The coordinates are inside the paragraph
            else:
                location = element.text
    if location:
        coordinates = calculate_coordinates(location)
        if coordinates:
            return Monument(title, coordinates)
    return None


def download_monuments_page(url: str) -> Monuments:
    """Download monuments from a page of the sitemap."""

    print(f"Pàgina: {url}")

    monuments: Monuments = []

    response = get(url)
    soup = BeautifulSoup(response.content, features="xml")
    locs = soup.find_all("loc")
    monuments = []
    for loc in locs:
        monument = scrape_monument(loc.text)
        if monument:
            print(f"Monument: {monument}")
            monuments.append(monument)
    return monuments


def download_monuments() -> Monuments:
    """Download all monuments from Catalunya Medieval."""

    monuments: Monuments = []

    sitemap_url = "https://www.catalunyamedieval.es/sitemap.xml"
    response = get(sitemap_url)
    soup = BeautifulSoup(response.content, features="xml")
    locs = soup.find_all("loc")
    for loc in locs:
        if "post" in loc.text:
            monuments += (download_monuments_page(loc.text))
    return monuments
       

def read_monuments_from_file(filename: str) -> Monuments | None:
    """Read the list of monuments from a file."""

    try:
        with open(filename, 'rb') as f:
            monuments = load(f)
        return monuments
    except:
        return None


def write_monuments_to_file(monuments: Monuments, filename: str) -> None:
    """Write the list of monuments to a file."""

    with open(filename, 'wb') as f:
        dump(monuments, f)


def get_monuments(filename: str) -> Monuments | None:
    """
    Get all monuments in the box.
    If filename exists, load monuments from the file.
    Otherwise, download monuments and save them to the file.
    """
    
    monuments = read_monuments_from_file(filename)
    if not monuments:
        monuments = download_monuments()
        write_monuments_to_file(monuments, filename)
    return monuments


get_monuments("monuments.dat")