
class Face(object):


    def __init__(self, name=None, type=None, points=None):
        self.name = name
        self.type = type
        self.points = points

    @classmethod
    def parse(self, s):
        # string in the form:
        #"name type 0 1 2 3"
        params = s.split()
        # params length must be 2 + a multiple of 2 or 4 so even
        if len(params) % 2 != 0:
            raise Exception('Odd number of parameters when even number is required')
        if len(params) < 4:
            raise Exception('At least 4 parameters are required')
        faces = []
        for i in range(0, (len(params)-2)/2):
            face = Face()
            face.name = params[0]
            face.type = params[1]
            face.points = [int(params[n]) for n in range(2 + 2 * i, 4 + 2 * i)]
            faces.append(face)
        return faces


    @classmethod
    def printFaces(self, faces, numPoints):
        for f in faces:
            if f.type != faces[0].type or f.name != faces[0].name:
                return 'All faces must have the same name and type'
            if len(f.points) != 2 and len(f.points) != 4:
                return 'All faces must have 2 or 4 points'
        string = '    ' + faces[0].name
        if faces[0].name in ['front', 'back']:
            string += '  // added automatically from blocks definition'
        string += '\n    {\n'
        string += '        type ' + faces[0].type + ';\n'
        string += '        faces\n'
        string += '        (\n'
        for f in faces:
            #print(f.points)
            if len(f.points) == 2:
                string += '            (' + str(f.points[0]) + '    ' + str(f.points[1]) + '    ' + str(f.points[1]+numPoints) + '    ' + str(f.points[0]+numPoints)  + ')\n'
            elif len(f.points) == 4:
                string += '            (' + str(f.points[0]) + '    ' + str(f.points[1]) + '    ' + str(f.points[2]) + '    ' + str(f.points[3])  + ')\n'

        string += '        );\n'
        string += '    }'

        return string
