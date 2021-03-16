import matplotlib.pyplot as plt
from math import dist, atan2
import numpy as np
from random import sample
import json

#Simulation fo our model:
x = [[np.cos(x), np.sin(x)] for x in np.linspace(0, 2*np.pi, 2000)]

y = sample(x, 500)
def initialDict(arr) :
    return [{ 'coor' : i, 'pointsConnected' : 0} for i in arr]

def Connect(arr, r) :
    for point in arr :
        if point['pointsConnected'] == 0 :
            for other in [i for i in arr if i != point] :
                if dist(point['coor'], other['coor']) <= r :
                    point['pointsConnected'] += 1
    return arr

def simulation(N, r, pts = 5000) :   
    theta = np.linspace(0, 2*np.pi, pts)
    points = [(np.cos(i), np.sin(i)) for i in theta]
    plt.figure(dpi=240)
    plt.style.use('ggplot')
    plt.title(f'Simulation for N={N}, r = {r}')
    plt.plot(np.cos(theta), np.sin(theta), color = 'purple')
    randomPoints = sample(points, N)

    delta = Connect(initialDict(randomPoints), r) 
    plt.scatter([i['coor'][0] for i in delta], [i['coor'][1] for i in delta], marker = 'o', color = 'purple', s = 40)
    con = [i['coor'] for i in delta if i['pointsConnected'] != 0]

    for i in con :
        for j in [k for k in con if k != i] :
            if dist(i, j) <= r :
                plt.plot([i[0], j[0]], [i[1], j[1]], '-', color = '#ff6600', linewidth = 0.4)
    plt.axis('equal')
    plt.show()
