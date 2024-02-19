import numpy as np

class Grid:
    """
    Grid of pixels made from a 2-D numpy array. This grid contains
    useful, readily-accessible information for scientific computation,
    such as standard deviations or medians.

    Parameters:
     - `array`: A 2-D numpy array to make a Grid object from.
    """
    def __init__(self, array: np.ndarray):
        if not isinstance(array, np.ndarray): raise TypeError("'array' must be a numpy array")
        if array.ndim != 2: raise ValueError("'array' must be 2-dimensional")

        # Data is indexed as (y, x)
        self.grid: np.ndarray = array
        self.size_y, self.size_x = np.shape(self.grid)

    @property
    def std(self) -> float:
        return np.std(self.grid)

    @property
    def mean(self) -> float:
        return np.mean(self.grid)

    @property
    def median(self) -> float:
        return np.median(self.grid)



class EmptyGrid(Grid):
    """
    Empty grid of pixels of a given dimension 

    Parameters:
     - `size_y`: Size of empty grid in y-direction
     - `size_x`: Size of empty grid in x-direction
    """
    def __init__(self, size_y, size_x):
        if not isinstance(size_y, int): raise TypeError("size_y must be an integer")
        if not isinstance(size_x, int): raise TypeError("size_x must be an integer")

        # y then x, as it will be transposed in `Grid.__init__()`
        super().__init__(self, np.empty((size_y, size_x)))