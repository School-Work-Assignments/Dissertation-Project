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
from scipy.ndimage import gaussian_filter

# Function applying Perlin noise
def generate_noise(width, height, scale):
    heightmap = np.zeros((width, height))
    for i in range(width):
        for j in range(height):
            x = i / scale
            y = j / scale

            # Declaring 4 corner values
            x0 = int(x)
            x1 = x0 + 1
            y0 = int(y)
            y1 = y0 + 1

            # Declaring coordinates within each cell
            tx = x - x0
            ty = y - y0

            # Declaring corner gradient vectors
            g00 = gradient(x0, y0)
            g01 = gradient(x0, y1)
            g10 = gradient(x1, y0)
            g11 = gradient(x1, y1)

            # Applying lerp on x-axis
            v1 = lerp(dot(g00, [tx, ty]), dot(g10, [tx - 1, ty]), smoothstep(tx))
            v2 = lerp(dot(g01, [tx, ty - 1]), dot(g11, [tx - 1, ty - 1]), smoothstep(tx))

            # Applying lerp on y-axis
            heightmap[i][j] = lerp(v1, v2, smoothstep(ty))

    # heightmap = np.interp(heightmap, (heightmap.min(), heightmap.max()), (-1, 1))

    return heightmap

# Function to calculate gradient vectors
def gradient(x, y):
    # generate a random unit vector from the integer coordinates
    angle = np.random.uniform(0, 2 * np.pi)
    return [np.cos(angle), np.sin(angle)]

# Function to calculate dot products between vectors
def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]

# Function to perform linear interpolation
def lerp(a, b, t):
    return (1 - t) * a + t * b

# Function to smoothen values (used for cell transitions)
def smoothstep(t):
    return t * t * (3 - 2 * t)

# Function to generate heightmap
def generate_heightmap(width, height, scale, octaves, persistence, lacunarity, seed=None):
    # Setting seed
    if seed is not None:
        np.random.seed(seed)

    # Initialising heightmap + amplitude variables
    heightmap = np.zeros((width, height))
    amplitude = 1.0
    total_amplitude = 0.0

    # Generating a number of heightmaps based on number of octaves
    for i in range(octaves):
        octave_noise = generate_noise(width, height, scale * (lacunarity ** i))

        heightmap += octave_noise * amplitude
        total_amplitude += amplitude
        amplitude *= persistence

    heightmap /= total_amplitude

    # Normalising heightmap
    heightmap -= heightmap.min()
    heightmap /= heightmap.max()
    heightmap *= 1000
    heightmap = heightmap.astype(np.uint8)

    # Applying gaussian filter to further smoothen the heightmap
    heightmap = gaussian_filter(heightmap, sigma=2.5)

    return heightmap

# Declaring input values
width = 80
height = 80
scale = 32
octaves = 5
persistence = 0.5
lacunarity = 2.0

# Starting timer
start = timer()

# Generating heightmap
heightmap = generate_heightmap(width, height, scale, octaves, persistence, lacunarity, seed=10)

# Ending timer
end = timer()
print("Execution time in MS:", (end-start) * 1000)
print("Memory usage in MB:", psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)

# Displaying and saving heightmap
plt.figure(figsize=(333, 333), dpi=1)
plt.imshow(heightmap, cmap='gray')
plt.setp(plt.gcf().get_axes(), xticks=[], yticks=[])
for pos in ['right', 'top', 'bottom', 'left']:
    plt.gca().spines[pos].set_visible(False)
plt.savefig('Outputs/Heightmaps/Perlin_Noise_Heightmap.png', bbox_inches='tight', pad_inches=0, dpi=1)
plt.show()