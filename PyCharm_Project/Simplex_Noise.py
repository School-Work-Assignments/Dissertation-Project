# Definition of all input variables used
# width/height = dimensions of output
# scale        = noise frequency (smaller -> smoother, larger -> more detailed)
# octaves      = number of heightmap layers with differing amplitudes/frequencies
# persistence  = rate at which octave amplitude changes between each octave
# lacunarity   = rate at which octave frequency changes between each octave
# seed         = value that defines the random number generation

import os
import psutil
from timeit import default_timer as timer
import time
import random
import numpy as np
import matplotlib.pyplot as plt
from opensimplex import OpenSimplex

# Declaring input values
width = 100
height = 100
scale = 25.0
octaves = 4
persistence = 0.5
lacunarity = 2.0

# Starting timer
start = timer()

# Initialising and generating heightmap
heightmap = np.zeros((height, width))
simplex = OpenSimplex(seed=10)

# Generating a number of heightmaps based on number of octaves
for y in range(height):
    for x in range(width):
        amplitude = 1.0
        frequency = 1.0
        value = 0.0
        for i in range(octaves):
            sample_x = x / scale * frequency
            sample_y = y / scale * frequency
            noise = simplex.noise2(sample_x, sample_y)
            value += noise * amplitude
            amplitude *= persistence
            frequency *= lacunarity
        heightmap[y][x] = value

# Normalising heightmap
heightmap = (heightmap - np.min(heightmap)) / (np.max(heightmap) - np.min(heightmap))

# Ending timer
end = timer()
print("Execution time in MS:", (end-start) * 1000)
print("Memory usage in MB:", psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)

# Displaying and saving heightmap
plt.figure(figsize=(333, 333), dpi=1)
plt.imshow(heightmap, cmap='gray', interpolation='bilinear')
plt.setp(plt.gcf().get_axes(), xticks=[], yticks=[])
for pos in ['right', 'top', 'bottom', 'left']:
    plt.gca().spines[pos].set_visible(False)
plt.savefig('Outputs/Heightmaps/Simplex_Noise_Heightmap.png', bbox_inches='tight', pad_inches=0, dpi=1)
plt.show()