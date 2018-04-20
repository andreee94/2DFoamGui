import matplotlib.pyplot as plt
import numpy as np
import sys
import os.path
from pprint import pprint

zorder_bg = 5
zorder_lines = 10
zorder_blocks = 50
zorder_faces = 55
zorder_numbers = 100


def extractSetting(s, name):
    s = s.replace(' = ', '')
    s = s.replace('=', '')
    s = s.replace(name, '').strip()
    return s;

def xyzFromFile(filename):
    content = []
    with open(filename, 'r') as f:
        content = f.readlines()
        f.close()
        #for c in content: print(c.strip())
    content = list(filter(lambda c: not c.strip().startswith('//') and c.strip() != '\n' and len(c.strip()) > 0, content))

    xs, ys, zs = None, None, None

    for c in content:
        print(c.strip())
        if c.lower().startswith('x'):
            xs = extractSetting(c, 'x')
            #content.remove(c)
        elif c.lower().startswith('y'):
            ys = extractSetting(c, 'y')
            #content.remove(c)
        elif c.lower().startswith('z'):
            zs = extractSetting(c, 'z')
            #content.remove(c)

    if xs == None or ys == None:
        raise Exception('X or Y lines is missing.')

    # xs = content[0]
    # ys = content[1]
    # #import pdb; pdb.set_trace()
    # if len(content) > 2:
    #     zs = content[2]
    #     z = [int(n) for n in zs.split()]
    # else: z = [-1, 1]

    x = [int(n) for n in xs.split()]
    y = [int(n) for n in ys.split()]

    if zs == None:
        z = [-1, 1]
    else: z = [int(n) for n in zs.split()]

    #print(x)
    #print(y)
    #print(z)
    return x, y, z, content

def arraySum(array, delta):
    array[:] = [x + delta for x in array]
    return array

def plotPoints(x, y, z, savefig=False, outputFile='output', block=False):
    fig = plt.figure()
    #ax = fig.gca(projection='3D')
    ax = fig.add_subplot(111)
    ax.set_aspect("equal")
    x.append(x[0])
    y.append(y[0])
    plt.figure(1)
    line = plt.plot(x, y, z[1], zorder=zorder_lines)
    color = line[0].get_c()
    #print(color)

    tr = 0 # max(x) / 10
    # plt.fill(x, y, alpha=0.6, zorder = 10)
    # for i in range(0, len(x) - 1):
    #     ax.annotate(str(i+ len(x)), xy = (x[i] + tr, y[i] + tr))
    #     #ax.annotate(str(i), xy = (x[i] + tr, y[i] + tr))

    #z = ([z[1]] * len(x)).append([z[0]] * len(x))

    delta = max(x) / 10
    #x.append(arraySum(x, -delta))
    #y.append(arraySum(y, delta))

    #ax.plot3D(x, y, z)

    fig = plt.figure(1)
    xback = arraySum(x, -delta)
    yback = arraySum(y, delta)
    plt.plot(xback, yback, color = color, zorder=zorder_bg)
    plt.fill(xback, yback, color = color, alpha = 0.6 , zorder=zorder_bg)

    for i in range(0, len(x) - 1):
        ax.annotate(str(i), xy = (xback[i] + tr, yback[i] + tr), zorder=zorder_numbers)

    #plt.plot(arraySum(x, -delta), arraySum(y, delta), color = color, zorder = 5)
    
    if savefig:
        fig.savefig(outputFile + '.png')
    plt.show(block=block)
    return  fig, 1, ax

def plotFacesAndBlocks(fig, fig_num,  ax, x, y, z, faces, blocks):
    #plt.figure(fig_num)
    for f in faces:
        for ff in faces[f]:
            if len(ff.points) == 2:
                xx = [x[i] for i in ff.points]
                yy = [y[i] for i in ff.points]
                ax.plot(xx, yy, color='r', zorder=zorder_faces)
                plt.draw()
                #ax.show()

    for b in blocks:
        if len(b.points) == 4:
            xx = [x[i] for i in b.points]
            yy = [y[i] for i in b.points]
            ax.fill(xx, yy, color='g', alpha = 0.6 , zorder=zorder_blocks)
            ax.plot(xx, yy, color='g', zorder=zorder_blocks)
            plt.draw()
            #ax.show()