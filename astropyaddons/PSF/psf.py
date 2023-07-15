from typing import Callable
import numpy as np
from scipy import integrate

from ..coordinates import Coordinates

class PSF:
    """
    Point Spread Function. 
    Used to calculate the counts each pixel on a CCD would have.

    Parameters:
     - `function`: Callable function with one input argument,
        that being the distance from the center of the PSF.
    """

    def __init__(self, function: Callable):
        self.function: Callable = function

    def counts_pixel(self, center: Coordinates, pixel: Coordinates, pixel_size: int or float = 1):
        """
        Function to get the counts that a pixel on the CCD would have.
        The double integral of the PSF is calculated for the pixel in question.
         - `center`: `Coordinates` object of the point light source.
         - `pixel`: `Coordaintes` object of the pixel which we want the counts of.
         - `pixel_size`: Size of the pixel, assumed to be 1 (representing 1 pixel) 
        """
        radius_function = lambda x, y: self.function((x*x + y*y) ** .5)

        integral, error = integrate.dblquad(
            radius_function,
            pixel.y-center.y, pixel.y-center.y+pixel_size, # BOUNDS FOR Y COORDINATE
            lambda _: pixel.x-center.x, lambda _: pixel.x-center.x+pixel_size, # BOUNDS FOR X COORDINATE
        )

        return integral



# GAUSSIAN FUNCTION
def gaussian(x, sd: float, max: float):
    """
    Returns the value of the gaussian function:
     - `distance`: Distance to mean of gaussian curve
     - `sd`: Standard Deviation of gaussian curve
     - `max`: Maximum of gaussian curve at mean
    """
    return (np.e**(-.5 * ((x)/sd)**2) * max)
class GaussianPSF(PSF):
    """
    Point Spread function using the Gaussian equation.
    Parameters:
     - `sd`: Standard deviation of gaussian curve.
     - `max`: Max value of gaussian curve at mean.
    """

    def __init__(self, sd: float, max: float):
        self.alpha: float = sd
        self.beta: float = max
    
    @property
    def function(self):
        return lambda r: moffat(r, self.alpha, self.beta)



# MOFFAT FUNCTION
# https://www.ias.ac.in/article/fulltext/joaa/009/01/0017-0024
def moffat(x, alpha: float, beta: float):
    F_0 = (beta - 1) * np.pi * alpha**2
    return F_0 * (1 + ((x)/alpha)**2) ** (-beta)
class MoffatPSF(PSF):
    """
    Point Spread function using the Moffat distribution.
    Parameters:
     - `alpha`, `beta`: Alpha and beta of the standard Moffat distribution.
    """

    def __init__(self, alpha: float, beta: float):
        self.alpha: float = alpha
        self.beta: float = beta
     
    @property
    def function(self):
        return lambda r: moffat(r, self.alpha, self.beta)