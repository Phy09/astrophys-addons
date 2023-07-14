from .coordinates import Coordinates
from .pixel import Pixel

import numpy as np

class Grid:
    """
    Grid of pixels, essentially the 'counts' data of the CCD/image.

    Parameters:
     - `size_x`: number of pixels in the x-dimension.
     - `size_y`: number of pixels in the y-direction.
    """
    def __init__(self, size_x: int, size_y: int):
        if not isinstance(size_x, int): raise TypeError("'size_x' must be an integer")
        if not isinstance(size_y, int): raise TypeError("'size_y' must be an integer")

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
    
class DataGrid(Grid):
    """
    Grid of pixels made from a 2-D numpy array.

    Parameters:
     - `array`: A 2-D numpy array to make a Grid object from.
    """
    def __init__(self, array: np.ndarray[np.ndarray]):
        if not isinstance(array, np.ndarray): raise TypeError("'array' must be a numpy array")
        if array.ndim != 2: raise ValueError("'array' must be 2-dimensional")

        size_y, size_y = np.shape(array)