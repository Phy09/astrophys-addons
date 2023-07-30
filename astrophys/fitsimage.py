# Essential imports

from astropy.io import fits
from astropy.wcs import WCS
from astropy.time import Time
from astropy.coordinates import Angle
import astropy.units as u

from scipy import ndimage
from itertools import product
import numpy as np
import matplotlib.pyplot as plt

class FITSImage:
    """ Class to handle FITS images in general. """

    def __init__(self, filepath):
        """
        `filepath`: filepath of FITS image to load.
        """
        self.fp = filepath

        with fits.open(self.fp) as fits_image:
            if len(fits_image) != 1:
                print(f"Warning: FITS image with filepath {self.fp} has multiple images. Only the first one will be loaded.")

            self.header = fits_image[0].header
            self.data: np.ndarray[np.ndarray] = fits_image[0].data * 1.0 #turn into floating point
        
        # Useful header values
        self.date, self.time = self.header['DATE-OBS'].split("T")
        self.exptime = self.header['EXPTIME']
        self.filter = self.header['FILTER']
        self.JD = Time(self.header['DATE-OBS'], format='isot').jd
        self.x_max = self.header['NAXIS1']
        self.y_max = self.header['NAXIS2']

        # Setting WCS
        wcs = WCS(self.header)
        if all(wcs.pixel_to_world_values([0,1], [0,1])[0] != np.array([1,2])): # Detect if the image is plate-solved. Returns True if it is.
            self.wcs = wcs

            # Create a "coordinate grid" that can be indexed via self.coords[y, x]
            # For high level applications, access using self.coordinates(y, x)
            x_pixel, y_pixel = np.array(list(product(np.arange(0, self.x_max), np.arange(0, self.y_max)))).T
            self.coords: np.ndarray[np.ndarray[float, float]] = np.transpose(np.array(wcs.pixel_to_world_values(x_pixel, y_pixel)).T.reshape(self.x_max, self.y_max, 2),(1,0,2))
        else:
            self.wcs = None
            self.coords = None

    # Useful statistical quantities

    @property
    def median(self):
        return np.median(self.data)

    @property
    def mean(self):
        return np.mean(self.data)
    
    @property
    def std(self):
        return np.std(self.data)

    def coordinates(self, y: int, x: int, format: str='hms') -> dict:
        """
        Displays the right ascension and declination of a pixel (y, x).

          - `y`: y-coordinate of pixel
          - `x`: x-coordinate of pixel
          - `format`: format to return angles. `'hms'`: `str` hours, mins, seconds. 
                `'angle'`: `astropy.coordinates.Angle`. `'degrees'`: `float` value
        """
        assert self.coords is not None, "The image is not plate-solved, no coordinates available."

        ra, dec = self.coords[y, x]

        ra = Angle(ra * u.deg)
        dec = Angle(dec * u.deg)

        if format=='angle':
            pass
        elif format=='degrees':
            ra = ra.degree
            dec = dec.degree
        elif format=='hms':
            ra = ra.to_string(unit=u.hour, sep=("h ","m ","s"))
            dec = dec.to_string(unit=u.degree, sep=("° ","' ","''"))
        else:
            raise ValueError(f"Format provided {format} does not exist.")

        return {'RA': ra, 'DEC': dec}

    def __repr__(self):
        return f'FITSImage of [{self.filter}, {self.date}, {self.time}, exptime {self.exptime}s]'

    def quickplot(self, lo_phi: float=-1, hi_phi: float=3) -> None:
        """
        Displays a simple grayscale plot of the data, returning `None` 
        
        Parameters:
          - `lo_phi`: standard deviations from median to assign to black
          - `hi_phi`: standard deviations from median to assign to white
        """
        assert lo_phi < hi_phi, "lo_phi must be lower than hi_phi"

        lo = self.median + lo_phi*self.std
        hi = self.median + hi_phi*self.std

        plt.figure(figsize=(10,10))
        plt.title(self.__repr__())
        plt.imshow(self.data, cmap='gray', origin='lower', vmin=lo, vmax=hi)

    def get_star_coords(self, threshold: float=2.5) -> list[tuple[float, float]]:
        """
        Gets the coordinates of stars in the image, given a threshold.

        Parameters:
          - `threshold`: multiple of median for the minimum value for
              a star.

        Returns: 2D numpy array: `[[y_1, x_1], [y_2, x_2], ...]` 
        """
        threshold_data = (self.data > threshold*self.median) * self.data #Sets everything under the threshold to 0
        data_max = ndimage.maximum_filter(self.data, 5) #Sets each pixel value to the brightest pixel value nearby

        maxima = (threshold_data==data_max) #`True` for the local maxima

        labeled, _ = ndimage.label(maxima) #Assigns different values for each local maxima
        slices = ndimage.find_objects(labeled) #Gets positions of labels

        coords = []
        for dy, dx in slices:
            if dy.stop-dy.start != 1 or dx.stop-dx.start != 1:
                print(f"Warning: Star with position y={dy}, x={dx} was not identified as a single point.")

            y_center = (dy.start + dy.stop - 1) // 2
            x_center = (dx.start + dx.stop - 1) // 2
            coords.append([y_center, x_center])
            
        return np.array(coords)