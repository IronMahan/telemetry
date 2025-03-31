import random
import matplotlib.pyplot as plt
import numpy as np
import time
from matplotlib.animation import FuncAnimation

def getData(num_data):
    return [random.randint(1, 10) for _ in range(num_data)]

settings = {
    "rows": 1,
    "cols": 3,
    "values": {"thrust": 0, "altitude": 1, "Some other shit": 2},
    "axis": {"thrust": [0], "altitude": [1], "Some other shit": [2]},
    "limits": {"thrust": [0, 100, 50], "altitude": [0, 100, 100], "Some other shit": [0, 100, 100]}
}

settings = {
    "rows": 3,
    "cols": 3,
    "values": {
        "thrust": 0, "altitude": 1, "velocity": 2,
        "temperature": 3, "pressure": 4, "humidity": 5,
        "acceleration": 6, "orientation": 7, "energy": 8
    },
    "axis": {
        "thrust": [0, 0], "altitude": [0, 1], "velocity": [0, 2],
        "temperature": [1, 0], "pressure": [1, 1], "humidity": [1, 2],
        "acceleration": [2, 0], "orientation": [2, 1], "energy": [2, 2]
    },
    "limits": {
        "thrust": [0, 100, 50], "altitude": [0, 100, 100], "velocity": [0, 500, 250],
        "temperature": [-50, 50, 0], "pressure": [900, 1100, 1013], "humidity": [0, 100, 50],
        "acceleration": [-10, 10, 0], "orientation": [0, 360, 180], "energy": [0, 1000, 500]
    }
}


fig, ax = plt.subplots(nrows=settings["rows"], ncols=settings["cols"], figsize=(9, 5))
plt.subplots_adjust(wspace=1, hspace=0.5)

x = []
y = [[] for _ in range(settings["rows"] * settings["cols"])]
lines = []
x_lim = 100

if isinstance(ax, np.ndarray):
    ax = ax.flat

# Initialize plots
for name, axis, limit in zip(settings["values"].keys(), settings["axis"].values(), settings["limits"].values()):
    line, = ax[*axis].plot([], [])
    ax[*axis].set_xlim(0, x_lim)
    ax[*axis].set_ylim(*limit[:-1])
    ax[*axis].set_xlabel(name)
    ax[*axis].set_ylabel("Time")
    lines.append(line)

def update(frame):
    init = time.time()
    data = getData(settings["rows"] * settings["cols"])
    x.append(frame)
    
    for idx, (valIdx, axis, vals, limit, line) in enumerate(zip(
            settings["values"].values(),
            settings["axis"].values(),
            settings["values"].values(),
            settings["limits"].values(),
            lines)):
        
        y[idx].append(data[valIdx])
        line.set_xdata(x)
        line.set_ydata(y[idx])
        
        # Expand axes if needed
        if y[idx][-1] > limit[1]:
            ax[idx].set_ylim(ax[idx].get_ylim()[0], y[idx][-1] + limit[-1])
        
        if x[-1] > ax[idx].get_xlim()[1]:
            ax[idx].set_xlim(x[-1] - x_lim, x[-1])
    print(time.time() - init)
    return lines

ani = FuncAnimation(fig, update, frames=range(1, 100), blit=True, interval=10)
plt.show()
