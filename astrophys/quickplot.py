import numpy as np
from matplotlib import pyplot as plt

from .region import Region
from .star import Star

def quickplot(data, lo_phi=-1, hi_phi=3, median=None, std=None, slice: list[tuple, tuple]=None) -> None:
    """ 
    Displays a quick plot of given data, returning `None`.
    
    Parameters:
      - `data`: 2D numpy array containing data to be plotted (ideally from FITS image)
      - `lo_phi`: standard deviations from median to assign to black
      - `hi_phi`: standard deviations from median to assign to white
      - `median`: median for lo_phi, hi_phi. If not provided, takes median of data.
      - `std`: standard deviation for lo_phi, hi_phi. If not provided, takes standard deviation of data.
      - `slice`: slice of data to plot. This is preferred compared to directly slicing the data.
          `slice` should be expressed as [(ymin, ymax), (xmin, xmax)]

    Returns: `None`
    """
    assert lo_phi < hi_phi, "lo_phi must be lower than hi_phi"

    # Defaults
    slicey, slicex = slice if slice is not None else list(zip([0,0],np.shape(data)))
    median = median if median is not None else np.median(data)
    std = std if std is not None else np.std(data)

    assert (slicey[0] < slicey[1]) and (slicex[0] < slicex[1]), "Invalid slice"

    # Get lower and upper bound for grayscale coloring
    lo = median + lo_phi * std
    hi = median + hi_phi * std

    # Plot data in grayscale
    plt.figure(figsize=(10,10))
    plt.imshow(data[slicey[0]:slicey[1], slicex[0]:slicex[1]], origin='lower', cmap='gray', vmin=lo, vmax=hi)

    # Adjust axis for slice
    if slice is not None:
        # Get xticks and yticks from current graph
        yticks, _ = plt.yticks()
        xticks, _ = plt.xticks()

        # Offset ticks by slice
        plt.yticks(yticks[1:-1], yticks[1:-1] + slicey[0])   
        plt.xticks(xticks[1:-1], xticks[1:-1] + slicex[0])

        # Set limits
        plt.xlim(0,slicex[1]-slicex[0])
        plt.ylim(0,slicey[1]-slicey[0])
    
def quickplot_with_regions(data, lo_phi, hi_phi, regions: list[Region], median=None, std=None, slice: list[tuple, tuple]=None, regiondotsize=1) -> None:
    """ 
    Displays a quick plot of given data, returning `None`.
    
    Parameters:
      - `data`: 2D numpy array containing data to be plotted (ideally from FITS image)
      - `lo_phi`: standard deviations from median to assign to black
      - `hi_phi`: standard deviations from median to assign to white
      - `region`: list of `Region`s to plot on data
      - `median`: median for lo_phi, hi_phi. If not provided, takes median of data.
      - `std`: standard deviation for lo_phi, hi_phi. If not provided, takes standard deviation of data.
      - `slice`: slice of data to plot. This is preferred compared to directly slicing the data.
          `slice` should be expressed as [(ymin, ymax), (xmin, xmax)]

    Returns: `None`
    """
    assert lo_phi < hi_phi, "lo_phi must be lower than hi_phi"

    # Defaults
    slicey, slicex = slice if slice is not None else list(zip([0,0],np.shape(data)))
    median = median if median is not None else np.median(data)
    std = std if std is not None else np.std(data)

    assert (slicey[0] < slicey[1]) and (slicex[0] < slicex[1]), "Invalid slice"

    # Get lower and upper bound for grayscale coloring
    lo = median + lo_phi * std
    hi = median + hi_phi * std

    # Plot data in grayscale
    plt.figure(figsize=(10,10))
    plt.imshow(data[slicey[0]:slicey[1], slicex[0]:slicex[1]], origin='lower', cmap='gray', vmin=lo, vmax=hi)

    for region in regions:
        # Get x and y coordinates of the edge of the region.
        y, x = zip(*region.enclosed_pixels)
        # Offset by slice
        y = [i-slicey[0] for i in y]
        x = [i-slicex[0] for i in x]

        # Plot region.
        plt.plot(x, y, ".", alpha=1, markersize=0.5*regiondotsize)

    # Adjust axis for slice
    if slice is not None:
        # Get xticks and yticks from current graph
        yticks, _ = plt.yticks()
        xticks, _ = plt.xticks()

        # Offset ticks by slice
        plt.yticks(yticks[1:-1], yticks[1:-1] + slicey[0])   
        plt.xticks(xticks[1:-1], xticks[1:-1] + slicex[0])
        
        # Set limits
        plt.xlim(0,slicex[1]-slicex[0])
        plt.ylim(0,slicey[1]-slicey[0])

def quickplot_with_stars(data, lo_phi, hi_phi, stars: list[Star], median=None, std=None, slice: list[tuple, tuple]=None, regiondotsize=1) -> None:
    """
    Displays a quick plot of given data, returning `None`.
    
    Parameters:
      - `data`: 2D numpy array containing data to be plotted (ideally from FITS image)
      - `lo_phi`: standard deviations from median to assign to black
      - `hi_phi`: standard deviations from median to assign to white
      - `stars`: list of `Star`s to plot on data
      - `median`: median for lo_phi, hi_phi. If not provided, takes median of data.
      - `std`: standard deviation for lo_phi, hi_phi. If not provided, takes standard deviation of data.
      - `slice`: slice of data to plot. This is preferred compared to directly slicing the data.
          `slice` should be expressed as [(ymin, ymax), (xmin, xmax)]

    Returns: `None`
    """
    regions = []
    for star in stars:
        regions.append(star.aperture)
        regions.append(star.annulus)

    quickplot_with_regions(data, lo_phi, hi_phi, regions, median, std, slice, regiondotsize)