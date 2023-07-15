from .coordinates import Coordinates
from dataclasses import dataclass

@dataclass
class Pixel:
    """
    Class encompassing a pixel in the CCD

    Parameters:
     - `coordinates`: `Coordinates` object, expressing the relative
        position of the pixel in the CCD.
     - `counts`: Light counts of the pixel.
    """
    coordinates: Coordinates
    counts: float=None