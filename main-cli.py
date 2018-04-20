import matplotlib.pyplot as plt
import numpy as np
import sys
import os.path
from pprint import pprint
import myutil as myutil
import myutilwrite as myutilwrite
from face import Face
from block import Block

def addFace(faceName, face):
    if faceName in faces:
        if face not in faces[faceName]:
            faces[faceName].append(face)
    else: faces[faceName] = [face]

def addBlock(block):
    global blocks
    blocks.append(block)
    addFace('front', Face('front', 'empty', block.points))
    addFace('back', Face('back', 'empty', myutil.arraySum(list(reversed(block.points)), len(x))))


if len(sys.argv) <= 1:
    print('Missing data file as argument.')
elif sys.argv[1] in ['-h', '--help', 'help']:
    print('''
The command line is:
--> python main-cli.py filename

Example data file:

# x coordinate of points
x=0 1 2 3 3 2 1 0
# y coordiante of points
y=0 0 1 1 3 3 4 4
# z coordinate of points
# 2 items for front and back
z=0 1
plot=true
face=inlet patch 0 7
face=outlet patch 4 3
face=lowerWall wall 0 1 1 2 2 3
face=upperWall wall 7 6 6 5 5 4
block=0 1 6 7 1 2 5 6 2 3 4 5 
    ''')
else:
    filename = sys.argv[1]  # get filename from command-line
    if len(sys.argv) > 2:
        outputfile = sys.argv[2]  # get filename output from command-line
    else: outputfile = 'blockMeshDict'

    x, y, z, content = myutil.xyzFromFile(filename)

    faces = {}
    blocks = []
    cellsize = 0.1

    for c in content:
        if c.strip().lower().startswith('face'):
            faceStr = myutil.extractSetting(c, 'face')
            for f in Face.parse(faceStr):
                addFace(f.name, f)
        if c.strip().lower().startswith('block'):
            blockStr = myutil.extractSetting(c, 'block')
            for b in Block.parse(blockStr):
                addBlock(b)
        if c.strip().lower().startswith('cellsize'):
            cellsizeStr = myutil.extractSetting(c, 'cellsize')
            try:
                cellsize = float(cellsizeStr)
            except: pass

    myutilwrite.writeBlockMeshDict(x, y, z, faces, blocks, cellsize, filename=outputfile)

    fig, fig_num, ax = myutil.plotPoints(x, y, z, block=False)
    myutil.plotFacesAndBlocks(fig, fig_num, ax, x, y, z, faces, blocks)
    plt.show() # required