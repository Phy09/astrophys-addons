from .coordinates import Coordinates
from .pixel import Pixel

import numpy as np

class Grid:
    """
    Grid of pixels, essentially the 'counts' data of the CCD.
    """
    def __init__(self, size_x: int, size_y: int):
        assert isinstance(size_x, int), "size_x must be an integer"
        assert isinstance(size_y, int), "size_y must be an integer"

        self.size_x=size_x
        self.size_y=size_y

        self.pixels: dict[Coordinates, Pixel] = {
            Coordinates(x,y): Pixel(Coordinates(x,y), counts=0) 
            for x in range(size_x)
            for y in range(size_y)
        }

    @property
    def pixel_values(self) -> list[int]:
        values = [pixel.counts for pixel in self.pixels.values()]
        return values

    @property
    def median(self) -> float:
        return np.median(self.pixel_values)