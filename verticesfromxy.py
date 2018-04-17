
# required to run over ssh
#import matplotlib
#matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import sys
import os.path
from pprint import pprint


filename = sys.argv[1]  # get filename from command-line
if len(sys.argv) > 1:
    outputfile = sys.argv[2]  # get filename output from command-line
else: outputfile = 'output.txt'

content = []
with open(filename, 'r') as f:
    content = f.readlines()
    f.close()
    #for c in content: print(c.strip())

content = list(filter(lambda c: not c.strip().startswith('#') and c.strip() != '\n' and len(c.strip()) > 0, content))
for c in content: print(c.strip())
xs = content[0]
ys = content[1]
#import pdb; pdb.set_trace()
if len(content) > 2:
    zs = content[2]
    z = [int(n) for n in zs.split()]
else: z = [-1, 1]

#print(z)

x = [int(n) for n in xs.split()]
y = [int(n) for n in ys.split()]

#print(x)
#print(y)

with open(outputfile, 'a+') as f:
    f.write('vertices' + '\n')
    f.write('(' + '\n')
    f.write('   #Front points' + '\n')
    for i in range(0, len(x)):
        f.write('   (')
        f.write(str(x[i]) + '   ')
        f.write(str(y[i]) + '   ')
        f.write(str(z[0]))
        f.write(')' + ' ' +'#' + str(i) + '\n')

    f.write('   #Back points' + '\n')
    for i in range(0, len(x)):
        f.write('   (')
        f.write(str(x[i]) + '   ')
        f.write(str(y[i]) + '   ')
        f.write(str(z[1]))
        f.write(')'  + ' ' +'#' + str(len(x) + i) + '\n')

    f.write(');')
    f.close()

def getSetting(strings, name):
    for s in strings:
        s = s.strip().lower()
        if s.strip().lower().startswith(name):
            s = s.replace('=', '')
            s = s.replace(' = ', '')
            s = s.replace(name, '').strip()
            #print(s)
            return s

def arraySum(array, delta):
    array[:] = [x + delta for x in array]
    return array

if getSetting(content, 'plot') == 'true':

    fig = plt.figure()
    #ax = fig.gca(projection='3D')
    ax = fig.add_subplot(111)
    ax.set_aspect("equal")
    x.append(x[0])
    y.append(y[0])
    plt.figure(1)
    line = plt.plot(x, y, z[1], zorder = 10)
    color = line[0].get_c()
    #print(color)

    plt.fill(x, y, alpha=0.6, zorder = 10)
    tr = 0 # max(x) / 10
    for i in range(0, len(x) - 1):
        ax.annotate(str(i+ len(x)), xy = (x[i] + tr, y[i] + tr))
        #ax.annotate(str(i), xy = (x[i] + tr, y[i] + tr))


    #z = ([z[1]] * len(x)).append([z[0]] * len(x))

    delta = max(x) / 10
    #x.append(arraySum(x, -delta))
    #y.append(arraySum(y, delta))

    #ax.plot3D(x, y, z)

    plt.figure(1)
    xback = arraySum(x, -delta)
    yback = arraySum(y, delta)
    plt.plot(xback, yback, color = color, zorder = 5)
    plt.fill(xback, yback, color = color, alpha = 0.6 , zorder = 5)

    for i in range(0, len(x) - 1):
        ax.annotate(str(i), xy = (xback[i] + tr, yback[i] + tr))

    #plt.plot(arraySum(x, -delta), arraySum(y, delta), color = color, zorder = 5)

    fig.savefig(outputfile + '.png')
    plt.show()
