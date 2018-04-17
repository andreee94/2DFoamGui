
class Face(object):

    def __init__(self, name, type, points):
        self.name = name
        self.type = type
        self.points = points

    @classmethod
    def printFaces(self, faces, numPoints):
        for f in faces:
            if f.type != faces[0].type or f.name != faces[0].name:
                return 'All faces must have the same name and type'
            if len(f.points) != 2 and len(f.points) != 4:
                return 'All faces must have 2 or 4 points'
        string = '    ' + faces[0].name
        if faces[0].name in ['front', 'back']:
            string += '  # added automatically from blocks definition'
        string += '\n    {\n'
        string += '        type ' + faces[0].type + ';\n'
        string += '        faces\n'
        string += '        (\n'
        for f in faces:
            print(f.points)
            if len(f.points) == 2:
                string += '            (' + str(f.points[0]) + '    ' + str(f.points[1]) + '    ' + str(f.points[1]+numPoints) + '    ' + str(f.points[0]+numPoints)  + ')\n'
            elif len(f.points) == 4:
                string += '            (' + str(f.points[0]) + '    ' + str(f.points[1]) + '    ' + str(f.points[2]) + '    ' + str(f.points[3])  + ')\n'

        string += '        );\n'
        string += '    }'

        return string
