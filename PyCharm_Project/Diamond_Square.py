import os
import psutil
from timeit import default_timer as timer
import numpy as np
import matplotlib.pyplot as plt

# Function to perform the diamond step
def diamond_step(heightmap, size, half, step, scale):
    for y in range(half, size, step):
        for x in range(half, size, step):
            heightmap[y][x] = (heightmap[y - half][x - half] +
                               heightmap[y + half][x - half] +
                               heightmap[y - half][x + half] +
                               heightmap[y + half][x + half]) * 0.25 + np.random.uniform(-scale, scale)
    return heightmap

# Function to perform the square step
def square_step(heightmap, size, half, step, scale):
    for y in range(0, size, half):
        for x in range((y + half) % step, size, step):
            heightmap[y][x] = (heightmap[(y - half + size - 1) % (size - 1)][x] +
                               heightmap[(y + half) % (size - 1)][x] +
                               heightmap[y][(x + half) % (size - 1)] +
                               heightmap[y][(x - half + size - 1) % (size - 1)]) * 0.25 + np.random.uniform(-scale, scale)
    return heightmap

# Function that repeatedly performs the diamond/square steps to form the diamond-square algorithm
def diamond_square(size, hs):
    # Initialising heightmap variables
    heightmap = np.zeros((size, size), dtype=np.float32)
    step = size - 1
    scale = hs

    while step > 1:
        half = step // 2
        scale *= 0.5

        heightmap = diamond_step(heightmap, size, half, step, scale)
        heightmap = square_step(heightmap, size, half, step, scale)
        step //= 2

    return heightmap

# Function to generate and output a heightmap via the diamond-square algorithm
def generate_heightmap_image(size, hs, seed=None):
    # Setting seed
    if seed is not None:
        np.random.seed(seed)

    # Generating the heightmap and declaring appropriate boundaries (normalising)
    map = diamond_square(size, hs)
    map -= map.min()
    map /= map.max()
    map *= 255
    map = map.astype(np.uint8)

    return map

# Starting timer
start = timer()

# Generating heightmap (value of n (size of heightmap) has to be a power of 2 then +1, example: 129 (128+1))
heightmap = generate_heightmap_image(257, 1000, seed=10)

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
plt.savefig('Outputs/Heightmaps/Diamond_Square_Heightmap.png', bbox_inches='tight', pad_inches=0, dpi=1)
plt.show()