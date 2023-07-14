from ..pixel import Pixel
from ..coordinates import Coordinates
from ..grid import Grid
from .psf import PSF

import numpy as np
import matplotlib.pyplot as plt

class CCD:
    """
    Class encompassing the CCD, used for PSF calculations.
    """
    def __init__(self, size_x: int, size_y: int):
        """
        Parameters:
         - `size_x`: width of the CCD
         - `size_y`: height of the CCD
        """
        self.grid: Grid = Grid(size_x, size_y)
        self.PSFs: list[PSF] = []
    
    def add_point_source(self, PSF: PSF, center: Coordinates, radius_pixels: int=25):
        """
        Adds a point source to the CCD and adds its brightness
        to the respective pixels on the grid.

        Parameters:
         - `PSF`: `PSF` object.
         - `center`: `Coordinates` object, of where the PSF source
            originates from.
         - `radius_pixels`: Radius of pixels to add brightness to.
            This is so that the function does not run too slow.
            Default: 15.
        """

        # Gather which pixels we should calculate the PSF for,
        # as a circle of radius `radius_pixels` around `center`
        enclosed_pixels: list[Pixel] = []
        for x in range(int(center.x-radius_pixels)-1, int(center.x+radius_pixels)+2):
            for y in range(int(center.y-radius_pixels)-1, int(center.y+radius_pixels)+2):
                # Check if pixel is out of bounds.
                if x<0 or y<0 or x>=self.grid.size_x or y>=self.grid.size_y:
                    continue

                # Check if pixel is in circle.
                if (center.x-x)**2 + (center.y-y)**2 <= radius_pixels**2:
                    enclosed_pixels.append(
                        self.grid.pixels[Coordinates(x, y)]
                    )

        for pixel in enclosed_pixels:
            pixel.counts += PSF.counts_pixel(center, pixel.coordinates, 1)

    def quickplot(self, corner_1: Coordinates=None, corner_2: Coordinates=None, phi_lo: float=-1, phi_hi: float=2.5):
        """
        Does a quick, simple plot of the CCD.

        Parameters:
         - `corner_1`: Optional. First corner of the plot.
         - `corner_2`: Optional. Second corner of the plot. 
        """
        corner_1 = corner_1 if corner_1 is not None else Coordinates(0, 0)
        corner_2 = corner_2 if corner_2 is not None else Coordinates(self.grid.size_x-1, self.grid.size_y-1)

        min_x, max_x = sorted([corner_1.x, corner_2.x])
        min_y, max_y = sorted([corner_1.y, corner_2.y])

        pixel_counts = np.array([
            [self.grid.pixels[Coordinates(x, y)].counts for x in range(min_x, max_x+1)]
            for y in range(min_y, max_y+1) 
        ])
        
        plt.figure(figsize=(10,10))
        plt.imshow(pixel_counts, cmap='gray', vmin=phi_lo, vmax=phi_hi)
        