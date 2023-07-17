from typing import Callable
import numpy as np
from scipy import integrate
from abc import ABC, abstractmethod

coord = tuple[float, float]

class PSF(ABC):
    """
    Abstract Class of Point Spread Function. 
    Used to calculate the counts each pixel on a CCD would have.
    """
    @property
    @abstractmethod
    def function(self):
        pass

    def counts_pixel(self, center: coord, pixel: coord, pixel_size: tuple=(1,1)):
        """
        Function to get the counts that a pixel on the CCD would have.
        The double integral of the PSF is calculated for the pixel in question.
         - `center`: tuple of the point light source.
         - `pixel`: tuple of the pixel's coordinates which we want the counts of.
         - `pixel_size`: Size of the pixel, assumed to be 1 in both directions
           (representing 1 pixel) 
        """
        radius_function = lambda x, y: self.function((x*x + y*y) ** .5)

        centerx, centery = center
        pixelx, pixely = pixel
        sizex, sizey = pixel_size

        integral, error = integrate.dblquad(
            radius_function,
                        pixely-centery,             pixely-centery+sizey, # BOUNDS FOR Y COORDINATE
            lambda _:   pixelx-centerx, lambda _:   pixelx-centerx+sizex, # BOUNDS FOR X COORDINATE
        )

        return integral



# GAUSSIAN FUNCTION
def gaussian(r, std: float, max: float):
    """
    Returns the value of the gaussian function:
     - `r`: Distance to mean of gaussian curve
     - `std`: Standard Deviation of gaussian curve
     - `max`: Maximum of gaussian curve at mean
    """
    return max * np.e**(-.5 * ((r)/std)**2)
class GaussianPSF(PSF):
    """
    Point Spread function using the Gaussian equation.
    Parameters:
     - `std`: Standard deviation of gaussian curve.
     - `max`: Max value of gaussian curve at mean.
    """

    def __init__(self, std: float, max: float):
        self.std: float = std
        self.max: float = max

    @property
    def function(self):
        return lambda r: moffat(r, self.std, self.max)



# MOFFAT FUNCTION
# https://www.ias.ac.in/article/fulltext/joaa/009/01/0017-0024
def moffat(r, alpha: float, beta: float, max: float):
    """
    Returns the value of the moffat distribution:
     - `r`: Distance to mean of gaussian curve
     - `alpha`, `beta`: Alpha and beta of the Moffat distribution.
     - `max`: Max value at mean of the distribution.
    """
    return max * (1 + ((r)/alpha)**2) ** (-beta)
class MoffatPSF(PSF):
    """
    Point Spread function using the Moffat distribution.
    Parameters:
     - `alpha`, `beta`: Alpha and beta of the standard Moffat distribution.
    """

    def __init__(self, alpha: float, beta: float, max: float):
        self.alpha: float = alpha
        self.beta: float = beta
        self.max: float = max

    @property
    def function(self):
        return lambda r: moffat(r, self.alpha, self.beta, self.max)