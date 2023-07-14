import numpy as np

from .fitsimage import FITSImage

class Region:
    """ Overarching class to define a region. """
    def __init__(self, fits_image: FITSImage):
        self.fits_image = fits_image
        self.enclosed_pixels: list[tuple] = [] #list of coordinates of pixels enclosed in fits_image. Form: (y, x)

    @property
    def pixel_values(self) -> list[float]:
        return [self.fits_image.data[coords] for coords in self.enclosed_pixels]
    @property
    def sum(self) -> float:
        return sum(self.pixel_values)
    @property
    def n(self) -> int:
        return len(self.enclosed_pixels)
    @property
    def mean(self):
        return np.mean(self.pixel_values)
    @property
    def median(self):
        return np.median(self.pixel_values)
    @property
    def std(self):
        return np.std(self.pixel_values)
    

class CircleRegion(Region):
    """ Region defined as a circle """
    def __init__(self, fits_image: FITSImage, center: tuple, radius: float):
        """
        Parameters:
          - `fits_image`: `FITSImage` object that the region belongs to
          - `center`: Center of the circle, (y, x)
          - `radius`: Radius of the circle.
        """
        super().__init__(fits_image)

        self.center = center

        # Defining included pixels
        center_y, center_x = center
        r = int(radius+1)

        for y in range(int(center_y)-r, int(center_y)+r):
            for x in range(int(center_x)-r, int(center_x)+r):

                distance_squared = (y-center_y)**2 + (x-center_x)**2
                if distance_squared <= radius**2:
                    self.enclosed_pixels.append((y, x))

        # Additional parameters of interest
        self.mean_err = None
        self.median_err = None

class AnnulusRegion(Region):
    """ Region defined as an annulus """
    def __init__(self, fits_image: FITSImage, center: tuple, inner_radius: float, outer_radius: float):
        """
        Parameters:
          - `fits_image`: `FITSImage` object that the region belongs to
          - `center`: Center of the Annulus, (y, x)
          - `inner_radius`: Inner radius of the Annulus.
          - `outer_radius`: Outer radius of the Annulus.
        """

        assert inner_radius < outer_radius, "Inner radius must be greater or equal to outer radius"

        super().__init__(fits_image)

        self.center = center

        # Defining included pixels
        center_y, center_x = center
        r = int(outer_radius+1)

        for y in range(int(center_y)-r, int(center_y)+r):
            for x in range(int(center_x)-r, int(center_x)+r):

                distance_squared = (y-center_y)**2 + (x-center_x)**2
                if inner_radius**2 <= distance_squared <= outer_radius**2:
                    self.enclosed_pixels.append((y, x))
        
        # Additional parameters of interest
        self.mean_err = None
        self.median_err = None

class SubAnnulusRegion(AnnulusRegion):
    """ Subsection of an Annulus Region """
    def __init__(self, fits_image: FITSImage, center: tuple, inner_radius: float, outer_radius: float, angle_min: float, angle_max: float):
        """
        Parameters:
          - `fits_image`: `FITSImage` object that the region belongs to
          - `center`: Center of the Annulus, (y, x)
          - `inner_radius`: Inner radius of the Annulus.
          - `outer_radius`: Outer radius of the Annulus.
          - `angle_min`: Minimum angle for pixels in the subsection of the annulus (in degrees)
          - `angle_max`: Maximum angle for pixels in the subsection of the annulus (in degrees)
        """
        from math import pi, atan2 

        assert inner_radius < outer_radius, "Inner radius must be greater or equal to outer radius"
        assert angle_min < angle_max, "Minimum angle must be smaller than maximum angle"

        super().__init__(fits_image, center, inner_radius, outer_radius)

        centery, centerx = center

        subsection_pixels = []
        for pixel in self.enclosed_pixels:
            pixely, pixelx = pixel
            diffy, diffx = pixely-centery, pixelx-centerx

            angle = (atan2(diffy, diffx)/pi * 180) % 360
            if angle_min <= angle < angle_max:
                subsection_pixels.append(pixel)
        
        self.enclosed_pixels = subsection_pixels