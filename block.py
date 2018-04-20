import math

class Block(object):

    def __init__(self, zonename=None, points=None):
        self.zonename = zonename
        self.points = points

    @classmethod
    def parse(self, s):
        # string in the form:
        # "name type 0 1 2 3"
        params = s.split()

        try:
            int(params[0])
            hasName = False
        except: hasName = True

        # params length must be 2 + a multiple of 2 or 4 so even
        if (len(params)-hasName) % 4 != 0:
            raise Exception('4 points for each block are required')
        if hasName and len(params) < 5:
            raise Exception('At least 5 parameters are required')
        if not hasName and len(params) < 4:
            raise Exception('At least 4 parameters are required')
        blocks = []
        for i in range(0, (len(params) - hasName) / 4):
            block = Block()
            block.zonename = params[0] if hasName else None
            block.points = [int(params[n]) for n in range(hasName + 4 * i, hasName + 4 + 4 * i)]
            blocks.append(block)
        return blocks

    @classmethod
    def printBlocks(self, blocks, numPoints, x, y, z, cellsize):
        for f in blocks:
            if len(f.points) != 4:
                return 'All blocks must have 4 points'
        string  = '////////////////////////////////////////////////////////\n'
        string += '// PLEASE CHECK CELL NUMBERS SINCE PROBABLY ARE WRONG //\n'
        string += '////////////////////////////////////////////////////////\n'
        #string = blocks[0].name
        #string += '\n{\n'
        #string += ' type ' + blocks[0].type + ';\n'
        #string += ' faces\n'
        #string += ' (\n'
        for f in blocks:
            if f.zonename == None: f.zonename = ''
            x_cells, y_cells, z_cells = getcellsnumber(x, y, z, f.points, cellsize)
            # x_cells = abs(int(math.ceil((x[f.points[0]] - x[f.points[1]]) / cellsize)))
            # y_cells = abs(int(math.ceil((y[f.points[1]] - y[f.points[2]]) / cellsize)))
            # z_cells = 1
            #print(f.points)
            string += '     hex (' + str(f.points[0]) + '  ' + str(f.points[1]) + '  ' + str(f.points[2]) + '  ' + str(f.points[3]) + '  '
            string += str(f.points[0]+numPoints) + '  ' + str(f.points[1]+numPoints) + '  ' + str(f.points[2]+numPoints) + '  ' + str(f.points[3]+numPoints) + ')'
            string += '    ' + f.zonename + ' (' + (str(x_cells) + '  ' + str(y_cells) + '  ' + str(z_cells) + ')' )
            string += '    simpleGrading (1 1 1)'
            string += '\n'
        #string += ' );\n'
        #string += '}'

        return string

def getcellsnumber(x, y, z, indices, cellsize):
    deltax1 = abs(x[indices[0]] - x[indices[1]])
    deltax2 = abs(x[indices[2]] - x[indices[3]])
    deltay1 = abs(y[indices[1]] - y[indices[2]])
    deltay2 = abs(y[indices[3]] - y[indices[0]])
    x_cells = int(math.ceil(max(deltax1, deltax2) / cellsize))
    y_cells = int(math.ceil(max(deltay1, deltay2) / cellsize))
    return x_cells, y_cells, 1 # z_cells = 1
