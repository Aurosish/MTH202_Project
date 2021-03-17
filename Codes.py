import matplotlib.pyplot as plt
from math import dist, atan2, factorial
import numpy as np
from random import sample
import json
from scipy.optimize import curve_fit

#Create the Dataset
def FreqDegrees(ds) :
    freq = {}
    for i in ds :
        freq[i] = freq.get(i, 0) + 1/5
    return freq

def addToJson(file, data) :
    with open(file, 'w') as fileOpen :
        json.dump(data, fileOpen)
    return 'Done!'

rVal = [0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.2, 0.3]
NVal = [100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 450, 500, 550, 600, 700, 800, 900, 1000, 2000]
dataList = {}
for j in NVal :
    Val = []
    for i in rVal :
            sum = 0
            temp = []
             for _ in range(5) :
                u = simulation(5000, j, i)
                temp += u
                sum += len([k for k in u if k['pointsConnected'] == 0])
          
            Val.append({'Parameter (r)' : i, 'No. of Isolated Vertices(X)' : int(sum/5), 'pointsConnected' : FreqDegrees([k['pointsConnected'] for k in temp])})
            print(f'r:{i} and N:{j}')
    dataList[j] = Val
 addToJson('newData.json', dataList)
print('Done!')

#The data is stored in 'newData.json' file.


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
    

    
#Read the 'newData.json' for analysis of the Dataset
def getFromJson(file) :
    with open(file, 'r') as fileRead :
        x = fileRead.read()
    
    return json.loads(x)

dataDict = getFromJson('newData.json')


#X vs r plots:
save_results_to = 'D:/SEM 04/MTH 202/Project/CurvePlots/'
def X_vs_rPlot(finalDict) :
    
    plt.style.use('seaborn')
    

    for element in finalDict.keys() :
        plt.ylabel('No. of Isolated Vertices(X)')
        plt.xlabel('Parameter (r)')
        plt.title(f'X vs r with N = {element}')
        
        plt.plot([i['Parameter (r)'] for i in finalDict[element]], [j['No. of Isolated Vertices(X)'] for j in finalDict[element]], '-', color = '#737373')
        plt.plot([i['Parameter (r)'] for i in finalDict[element]], [j['No. of Isolated Vertices(X)'] for j in finalDict[element]], 'o',color = '#2e2eb8', markersize = 4.5)
        plt.savefig(save_results_to + f'N={element}.png',dpi = 2400)
        plt.clf()
    return "Done"


#Exponential Curve fitting to X vs r plots:
save_results_to = 'D:/SEM 04/MTH 202/Project/Curve_Fit_Plots/'

def g(x, a, b) :
    return a*np.exp(-b*x)

def f(x, a, b) :
    return a*pow(x, -b)

def fitPlotExp(finalDict, style, N) :
    parsed = finalDict
    r = [i['Parameter (r)'] for i in parsed[N]]
    X = [j['No. of Isolated Vertices(X)'] for j in parsed[N]]
    popt, pcov = curve_fit(g, r, X)
    
    plt.style.use(style)
    plt.ylabel('No. of Isolated Vertices(X)')
    plt.xlabel('Parameter (r)')
    plt.title(f'X vs r for N = {N}')
    
    plt.plot([i['Parameter (r)'] for i in parsed[N]], [j['No. of Isolated Vertices(X)'] for j in parsed[N]], '#471323', marker = 'o', label = 'Points', linestyle = '')
    x = np.linspace(0, 0.3, 500)
    plt.plot(x, g(x, popt[0], popt[1]), '#585563',label = f'Curve Fit: {round(popt[0], 2)}*exp({-round(popt[1], 2)}*x)')
    plt.legend()
    plt.savefig(save_results_to + f'expCurveFitN={N}.png', dpi = 600)
    plt.clf()
#Run the code as:
for N in [100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 450, 500, 550, 600, 700, 800, 900, 1000, 2000] :
    fitPlotExp(dataDict, 'seaborn', str(N))



#Degree Distribution:
save_results_to = 'D:/SEM 04/MTH 202/Project/DegDist/'

def DegDistribution(finalDict, style, r, N) :
    plt.style.use(style)
    for i in finalDict :
        if i == str(N) :
            plt.ylabel('P(X=k)')
            plt.xlabel('Degrees(k)')
            for j in finalDict[i] :
                if j["Parameter (r)"] == r :
                    plt.title(f'Degree Distribution for N = {i}, r = {j["Parameter (r)"]}.')

                    plt.bar([int(element) for element in j['pointsConnected'].keys()], [i/N for i in j['pointsConnected'].values()], color='#ff0066',edgecolor = 'black')
                    
                    plt.savefig(save_results_to + f'DegDisN,r={i},{j["Parameter (r)"]}.png')
                    plt.clf()

#Checking if Degree distribution follows Power law:
save_results_to = 'D:/SEM 04/MTH 202/Project/PwrDist/'
def PowerDist(finalDict,r, N) :
    
    for i in finalDict :
        if i == str(N) :
            plt.grid()
            plt.ylabel('P(X = k)')
            plt.xlabel('Degrees(k)')
            for j in finalDict[i] :
                if j["Parameter (r)"] == r :
                    plt.title(f'Degree Distribution for N = {i}, r = {j["Parameter (r)"]}.')
                    
                    elements = [element for element in sorted([int(el) for el in j['pointsConnected'].keys()])]
                    plt.plot(elements, [j['pointsConnected'][str(i)]/N for i in elements], color='#ff8000', label = 'Degree Distribution Curve')
                    # popt, pcov = curve_fit(f, elements, [j['pointsConnected'][str(i)]/N for i in elements])

                    
                    pts = np.linspace(0, max(elements)+1, 500)
                    # plt.plot(pts, f(pts, popt[0], popt[1]), label = f'Power curve: y = {round(popt[0], 2)}*x^{-round(popt[1], 2)}', color="#6320ee")
                    plt.plot(pts, [pow(i, -1.5) for i in pts], label = 'Power curve: y = x^-1.5', color="#33cc33")

                    plt.legend()
                    plt.xlim(-0.5, max(elements)+1)
                    plt.ylim(0, 1)
                    
                    
                    plt.savefig(save_results_to + f'N,r={N},{r}.png', dpi=600)
                    plt.clf()
