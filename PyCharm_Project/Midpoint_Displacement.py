# Definition of all input variables used
# start_points = starting position of point generation
# iterations   = number of times the line is subdivided
# rand_value   = value that represents the amount of randomness applied
# roughness    = value that defines the level of detail and roughness (non-smoothness) of output

import os
import psutil
from timeit import default_timer as timer
import random
from matplotlib import pyplot as plt

# Function to generate points via midpoint-displacement (using recursion)
def Generate_Points(iterations, points, rand_value, roughness):
    if iterations == 0:
        return points

    new_points = [points[0]]
    for i in range(len(points) - 1):
        mid_x = (points[i][0] + points[i + 1][0]) / 2
        mid_y = (points[i][1] + points[i + 1][1]) / 2

        rand_y = mid_y + random.uniform(-rand_value, rand_value)
        rand_y = max(rand_y, 0)

        new_points.append([mid_x, rand_y])
        new_points.append(points[i+1])

    return Generate_Points(iterations-1, new_points, rand_value * (2**-roughness), roughness)

# Declaring input values
start_points = [[0.0, 0.0], [1.0, 0.0]]
iterations = 16
rand_value = 0.25
roughness = 0.5

# Starting timer
start = timer()

# Generating final points
final_points = Generate_Points(16, start_points, 0.25, 1)

# Ending timer
end = timer()
print("Execution time in MS:", (end-start) * 1000)
print("Memory usage in MB:", psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)

# Displaying and saving plot
x, y = zip(*final_points)
plt.plot(x, y)
plt.setp(plt.gcf().get_axes(), xticks=[], yticks=[])
plt.title('Midpoint Displacement')
plt.savefig('Outputs/Midpoint_Displacement.png')
plt.show()