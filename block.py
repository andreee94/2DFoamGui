import math

class Block(object):

    def __init__(self, zonename, points):
        self.zonename = zonename
        self.points = points

    @classmethod
    def printBlocks(self, blocks, numPoints, x, y, z, cellsize):
        for f in blocks:
            if len(f.points) != 4:
                return 'All blocks must have 4 points'
        string = ''
        #string = blocks[0].name
        #string += '\n{\n'
        #string += ' type ' + blocks[0].type + ';\n'
        #string += ' faces\n'
        #string += ' (\n'
        for f in blocks:
            if f.zonename == None: f.zonename = ''
            x_cells = int(math.ceil((x[f.points[0]] - x[f.points[1]]) / cellsize))
            y_cells = int(math.ceil((y[f.points[1]] - y[f.points[2]]) / cellsize))
            z_cells = 1
            print(f.points)
            string += '     hex (' + str(f.points[0]) + '  ' + str(f.points[1]) + '  ' + str(f.points[2]) + '  ' + str(f.points[3]) + '  '
            string += str(f.points[0]+numPoints) + '  ' + str(f.points[1]+numPoints) + '  ' + str(f.points[2]+numPoints) + '  ' + str(f.points[3]+numPoints) + ')'
            string += '    ' + f.zonename + ' (' + (str(x_cells) + '  ' + str(y_cells) + '  ' +str(z_cells) + ')' )
            string += '    simpleGrading (1 1 1)'
            string += '\n'
        #string += ' );\n'
        #string += '}'

        return string
