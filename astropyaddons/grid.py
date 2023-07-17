import numpy as np

class Grid:
    """
    Grid of pixels made from a 2-D numpy array, with 

    Parameters:
     - `array`: A 2-D numpy array to make a Grid object from.
    """
    def __init__(self, array: np.ndarray):
        if not isinstance(array, np.ndarray): raise TypeError("'array' must be a numpy array")
        if array.ndim != 2: raise ValueError("'array' must be 2-dimensional")

        #Transpose, so that the data is indexed as (x, y)
        self.pixels: np.ndarray = array.T 
        self.size_x, self.size_y = np.shape(self.pixels)

    @property
    def std(self) -> float:
        return np.std(self.pixels)

    @property
    def mean(self) -> float:
        return np.mean(self.pixels)

    @property
    def median(self) -> float:
        return np.median(self.pixels)



class EmptyGrid(Grid):
    """
    Empty grid of pixels of a given dimension 

    Parameters:
     - `size_x`: Size of empty grid in x-direction
     - `size_y`: Size of empty grid in y-direction
    """
    def __init__(self, size_x, size_y):
        if not isinstance(size_x, int): raise TypeError("size_x must be an integer")
        if not isinstance(size_y, int): raise TypeError("size_y must be an integer")

        # y then x, as it will be transposed in `Grid.__init__()`
        super().__init__(self, np.empty((size_y, size_x)))