# import matplotlib.pyplot as plt
# import numpy as np

# # Initializing the background
# fig, ax = plt.subplots()
# background = fig.canvas.copy_from_bbox(ax.bbox)

# # Updating plot elements
# num_frames = 100
# x = np.linspace(0, 2 * np.pi, 100)
# line, = ax.plot(x, np.sin(x))

# for i in range(num_frames):
#     # Restoring background
#     fig.canvas.restore_region(background)

#     # Updating plot elements (Redrawing modified elements)
#     line.set_ydata(np.sin(x + i * 0.1))
#     ax.draw_artist(line)

#     # Blitting to the screen
#     fig.canvas.blit(ax.bbox)

#     plt.pause(0.01)

# # Displaying the final plot
# plt.show()

import matplotlib.pyplot as plt
import random
import time

print("hi")

# Initialize the figure and axis
fig, ax = plt.subplots()

# Initial x-range
x_min, x_max = 0, 50
x = list(range(x_min, x_max))
y_max = 50
y = [i + random.randint(-10, 10) for i in range(len(x))]
line, = ax.plot(x, y)
ax.set_xlim(x_min, x_max)
ax.set_ylim(-100, 100)

# Copy background
fig.canvas.draw()
background = fig.canvas.copy_from_bbox(ax.bbox)

num_frames = 1000
for i in range(x_max, x_max + num_frames):
    # Restore background
    fig.canvas.restore_region(background)
    
    # Update data
    x.append(i)
    y.append(x[-1] + random.randint(-x[-1], x[-1]))
    line.set_xdata(x)
    line.set_ydata(y)
    ax.draw_artist(line)
    
    # Expand x-axis if needed
    if x[-1] > x_max:
        x_max += 25
        ax.set_xlim(x_min, x_max)
        fig.canvas.draw()
        background = fig.canvas.copy_from_bbox(ax.bbox)
    
    if y[-1] > y_max:
        y_max += 25
        ax.set_ylim(0, y_max)
        fig.canvas.draw()
        background = fig.canvas.copy_from_bbox(ax.bbox)
    
    # Blit to screen
    fig.canvas.blit(ax.bbox)
    plt.pause(0.001)

plt.show()
