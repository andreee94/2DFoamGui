import matplotlib.pyplot as plt
import numpy as np
import sys
import os.path
from pprint import pprint
import myutil as myutil
import myutilwrite as myutilwrite
from face import Face
from block import Block

if len(sys.argv) == 0:
    print('Missing data file as argument.')

filename = sys.argv[1]  # get filename from command-line
if len(sys.argv) > 2:
    outputfile = sys.argv[2]  # get filename output from command-line
else: outputfile = 'blockMeshDict'

x, y, z, content = myutil.xyzFromFile(filename)

cellsize = 0.1


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

faces = {}
blocks = []
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

