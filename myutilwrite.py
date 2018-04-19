from face import Face
from block import Block


def writeBlockMeshDict(x, y, z, faces, blocks, cellsize, temp=False, filename='blockMeshDict'):
    if temp:
        filename = '.temp'
    with open(filename, 'w+') as file:
        writeInit(file)
        writePoints(file, x, y, z)
        writeEdges(file)
        writeFaces(file, faces, x, y, z)
        writeBlocks(file, blocks, x, y, z, cellsize)
        writePatchPairs(file)

def writeInit(file):
    s = """FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      blockMeshDict;
}

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
// Created by Andreee94
// -------> 2D Foam GUI
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

convertToMeters 1;
"""
    file.write(s + '\n\n')

def writePoints(file, x, y, z):
    file.write('vertices' + '\n')
    file.write('(' + '\n')
    file.write('   //Front points' + '\n')
    for i in range(0, len(x)):
        file.write('   (')
        file.write(str(x[i]) + '   ')
        file.write(str(y[i]) + '   ')
        file.write(str(z[0]))
        file.write(')' + ' ' + '//' + str(i) + '\n')

    file.write('   //Back points' + '\n')
    for i in range(0, len(x)):
        file.write('   (')
        file.write(str(x[i]) + '   ')
        file.write(str(y[i]) + '   ')
        file.write(str(z[1]))
        file.write(')' + ' ' + '//' + str(len(x) + i) + '\n')

    file.write(');\n\n')

def writeBlocks(file, blocks, x, y, z, cellsize):
    file.write('blocks\n(\n')
    file.write(Block.printBlocks(blocks, len(x), x, y, z, cellsize))
    file.write(');\n\n')

def writeEdges(file):
    file.write('edges\n(\n')
    file.write(');\n\n')

def writeFaces(file, faces, x, y, z):
    file.write('boundary\n(\n')
    for f in faces:
        file.write(Face.printFaces(faces[f], len(x)))
        file.write('\n\n')
    file.write(');\n\n')

def writePatchPairs(file):
    file.write('mergePatchPairs\n(\n')
    file.write(');\n\n')
