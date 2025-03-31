import random
import matplotlib.pyplot as plt
import numpy as np

import time

def getData(num_data):
    return [random.randint(1, 10) for _ in range(num_data)]

settings = {
    "rows": 1,
    "cols": 3,
    "values": {"thrust": 0,             "altitude": 1,              "Some other shit": 2},
    "axis":   {"thrust":[0],            "altitude": [1],            "Some other shit": [2]},
    "limits": {"thrust": [0, 100, 50],  "altitude": [0, 100, 100],  "Some other shit": [0, 100, 100]}
}

# settings = {
#     "rows": 3,
#     "cols": 3,
#     "values": {
#         "thrust": 0, "altitude": 1, "velocity": 2,
#         "temperature": 3, "pressure": 4, "humidity": 5,
#         "acceleration": 6, "orientation": 7, "energy": 8
#     },
#     "axis": {
#         "thrust": [0, 0], "altitude": [0, 1], "velocity": [0, 2],
#         "temperature": [1, 0], "pressure": [1, 1], "humidity": [1, 2],
#         "acceleration": [2, 0], "orientation": [2, 1], "energy": [2, 2]
#     },
#     "limits": {
#         "thrust": [0, 100, 50], "altitude": [0, 100, 100], "velocity": [0, 500, 250],
#         "temperature": [-50, 50, 0], "pressure": [900, 1100, 1013], "humidity": [0, 100, 50],
#         "acceleration": [-10, 10, 0], "orientation": [0, 360, 180], "energy": [0, 1000, 500]
#     }
# }



if __name__ == '__main__':
    fig, ax = plt.subplots(nrows=settings["rows"], ncols=settings["cols"], figsize=(9, 5))
    plt.subplots_adjust(wspace=1, hspace=0.5)

    x = []
    y = [[] for _ in range(settings["rows"] * settings["cols"])]
    lines = []
    x_lim = 100


    # init
    for name, axis, limit in zip(settings["values"].keys(),
                                 settings["axis"].values(),
                                 settings["limits"].values()):
        
        # print(limit)
        # print(axis)

        line, = ax[*axis].plot([0], [0])
        ax[*axis].set_xlim(0, x_lim)
        ax[*axis].set_ylim(*limit[:-1])
        ax[*axis].set_xlabel(name)
        ax[*axis].set_ylabel("Time")
        lines.append(line)


    fig.canvas.draw()
    backgrounds = []

    IDK = tuple(enumerate(zip(
            settings["values"].values(),
            settings["axis"].values(),
            settings["values"].values(),
            settings["limits"].values(),
            lines,
        )))

    if isinstance(ax, np.ndarray):
        ax = ax.flat
        backgrounds = [fig.canvas.copy_from_bbox(a.bbox) for a in ax]

    else:
        backgrounds = [fig.canvas.copy_from_bbox(ax.bbox)]


    init_time = time.time()

    for step in range(1, 100):
        for background in backgrounds:
            fig.canvas.restore_region(background)

        data = getData(settings["rows"] * settings["cols"])
        x.append(step)

        for idx, (valIdx, axis, vals, limit, line) in IDK:

            y[idx].append(data[valIdx])
            line.set_xdata(x)
            line.set_ydata(y[idx])

            ax[idx].draw_artist(line)

            # expand if needed
            if y[idx][-1] > limit[1]:
                ax[idx].set_ylim(ax[idx].get_ylim()[-1] + limit[-1])
                fig.canvas.draw()
                backgrounds[idx] = fig.canvas.copy_from_bbox(ax[idx].bbox)
            
            if x[-1] > x_lim:
                # print(ax[idx].get_xlim())
                ax[idx].set_xlim(ax[idx].get_xlim()[-1] + x_lim)
                fig.canvas.draw()
                backgrounds[idx] = fig.canvas.copy_from_bbox(ax[idx].bbox)
            
            fig.canvas.blit(ax[idx].bbox)

        plt.pause(0.001)
    plt.pause(0.001)
    print("Time per frame:", (time.time() - init_time)/100)
    # plt.ion()
    
    plt.show()