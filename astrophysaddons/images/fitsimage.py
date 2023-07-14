from astropy.io import fits
from astropy.wcs import WCS
from astropy.time import Time

import numpy as np
from itertools import product

from ..grid import DataGrid

class FITSImage:
    """
    Class to handle FITS images. Load with `FITSImage(filepath)`.
    """

    def __init__(self, filepath, image_to_load: int=None):
        """
        Parameters:
         - `filepath`: filepath of FITS image to load.
         - `image_to_load`: which image to load of the file.
            If none specified, will load the first image.
        """

        # LOAD FITS FILE
        with fits.open(filepath) as fits_image:
            if image_to_load is None:
                image_to_load = 0
                if len(fits_image) != 1:
                    print(f"Warning: FITS image with filepath {self.fp}"\
                            "has multiple images."\
                            "Only the first one will be loaded.")
            
            self.header = fits_image[image_to_load].header
            self.grid: DataGrid = DataGrid(fits_image[image_to_load].data)


        # EXTRACTING USEFUL HEADERS
        self.JD = Time(self.header['DATE-OBS'], format='isot').jd
        self.date, self.time = self.header['DATE-OBS'].split("T")
        self.exptime = self.header['EXPTIME']
        self.filter = self.header['FILTER']
        self.size_x = self.header['NAXIS1']
        self.size_y = self.header['NAXIS2']


        # SETTING WCS
        wcs = WCS(self.header)
        # Detect if the image is plate-solved. Returns True if it is.
        if all(wcs.pixel_to_world_values([0,1], [0,1])[0] != np.array([1,2])):
            self.wcs = wcs

            # Create a "coordinate grid" that can be indexed via self.coords[y, x]
            # For high level applications, access using self.coordinates(y, x)
            x_pixel, y_pixel = np.array(list(product(np.arange(0, self.size_x), np.arange(0, self.size_y)))).T
            self.coords: np.ndarray[np.ndarray[float, float]] = \
                np.transpose(np.array(wcs.pixel_to_world_values(x_pixel, y_pixel)).T.reshape(self.size_x, self.size_y, 2),(1,0,2))
        else:
            self.wcs = None
            self.coords = None