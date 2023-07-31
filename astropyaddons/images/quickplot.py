from .fitsimage import FITSImage
from matplotlib import pyplot as plt

coord = tuple(int, int)

def quickplot(img: FITSImage, phi_lo: float=-1, phi_hi: float=3, corners: tuple[coord, coord]=None) -> None:
    """ 
    Displays a quick plot of given data.
    
    Parameters:
      - `img`: `FITSImage` object to plot.
      - `phi_lo`: standard deviations from median to assign to black.
      - `phi_hi`: standard deviations from median to assign to white.
      - `corners`: Optional. tuple containing 2 `coords`, each written as `(x, y)`.
        Data between the two corners (inclusive) will be plotted. Ex. `((x1, y1), (x2, y2))`
    """
    if phi_lo <= phi_hi: raise ValueError("phi_lo must be smaller than phi_hi")

    # Getting values for convenience
    size_y, size_x = img.grid.size_y, img.grid.size_x
    median, std = img.grid.median, img.grid.std

    ### EXTRACTING `CORNERS` DATA
    # Extracting default
    ((y1, x1), (y2, x2)) = corners if corners is not None \
        else ((0, 0), (size_y-1, size_x-1))
    
    # Check that corners given are ints
    for value in (y1, y2, x1, x2):
        if not isinstance(value, int): 
            raise TypeError("Invalid values for 'corners' given. Are they all 'int's?")

    # Getting min/max x and y values
    y_min, y_max = sorted([y1, y2])
    x_min, x_max = sorted([x1, x2])

    # Check that values are within bounds
    if y_min < 0 or x_min < 0 or y_max > size_y-1 or x_max > size_x-1:
        raise IndexError(f"Corners given are out of range (MAX y={size_y-1}, x={size_y-1})")

    ### PLOTTING
    # Get upper and lower bounds
    lo = median + std * phi_lo
    hi = median + std * phi_hi

    # Plot data in grayscale
    plt.figure(figsize=(10, 10))
    plt.title(img.__repr__())
    plt.imshow(
        img.grid.grid[y_min:y_max+1, x_min:x_max+1], 
        origin='lower', 
        cmap='gray',
        vmin=lo,
        vmax=hi
        )
    
    # Adjust the axis for the corners provided
    if y_min > 0 or x_min > 0:
        # Get xticks and yticks from current graph
        yticks, _ = plt.yticks()
        xticks, _ = plt.xticks()

        # Offset ticks by the x_min, y_min
        plt.yticks(yticks[1:-1], yticks[1:-1] + y_min)
        plt.xticks(xticks[1:-1], xticks[1:-1] + x_min)

        # Set limits
        plt.ylim(0, y_max-y_min)
        plt.xlim(0, x_max-x_min)


