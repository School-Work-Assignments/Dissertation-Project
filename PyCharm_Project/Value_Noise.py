# Definition of all input variables used
# width/height = dimensions of output
# octaves      = number of heightmap layers with differing amplitudes/frequencies
# persistence  = rate at which octave amplitude changes between each octave

import os
import psutil
from timeit import default_timer as timer
import numpy as np
import matplotlib.pyplot as plt

# Function to generate heightmap
def value_noise(shape, octaves=1, persistence=0.5, seed=None):
    # Setting Seed
    if seed is not None:
        np.random.seed(seed)

    # Generting a grid of random values based off the image shape
    heightmap = np.zeros(shape)

    # Generating a number of heightmaps all based off of each other according to the number of octaves
    weight = 1.0
    for octave in range(octaves):
        octave_grid = np.random.rand(*shape)
        octave_heightmap = np.interp(octave_grid, (0, 1), (-1, 1))
        heightmap += weight * octave_heightmap
        weight *= persistence

    # Scaling heightmap values to range from -1 to 1 via linear interpolation
    heightmap = np.interp(heightmap, (heightmap.min(), heightmap.max()), (-1, 1))

    return heightmap

# Declaring variables required to generate heightmap
width = 20
height = 20
octaves = 6
persistence = 0.5

# Starting timer
start = timer()

#Generating heightmap
heightmap = value_noise((width, height), octaves=octaves, persistence=persistence, seed=10)

# Ending timer
end = timer()
print("Execution time in MS:", (end-start) * 1000)
print("Memory usage in MB:", psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)

# Displaying and saving heightmap
plt.figure(figsize=(333, 333), dpi=1)
plt.imshow(heightmap, cmap='gray', interpolation='bicubic')
plt.setp(plt.gcf().get_axes(), xticks=[], yticks=[])
for pos in ['right', 'top', 'bottom', 'left']:
    plt.gca().spines[pos].set_visible(False)
plt.savefig('Outputs/Heightmaps/Value_Noise_Heightmap.png', bbox_inches='tight', pad_inches=0, dpi=1)
plt.show()