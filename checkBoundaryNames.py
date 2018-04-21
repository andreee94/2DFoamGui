import sys
import os.path
from collections import Counter
from tabulate import tabulate
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile

def getBoundaryNames(filename, isBlockMeshDict=False):
    if not os.path.isfile(filename):
        return None

    f = ParsedParameterFile(filename)

    boundaryString = 'boundary' if isBlockMeshDict else 'boundaryField'

    if boundaryString not in f:
        return 0
    b = f[boundaryString]

    res = []
    for s in b:
        if isinstance(s, str):
            res.append(s)
    return res

def compareArrays(a, b):
    return Counter(a) == Counter(b)

# END FUNCTIONS
########################################

files = ['0/k',
         '0/nut',
         '0/omega',
         '0/p',
         '0/U',
         '0/Ux,'
         '0/Uy',
         '0/Uz',
         '0/nuTilda',
         '0/epsilon',
         '0/v2']

blockMeshDictFile = 'system/blockMeshDict'

bmd_boundaries = getBoundaryNames(blockMeshDictFile, isBlockMeshDict=True)

boundaries = {}
for f in files:
    print('_________________________________________________________')
    print('Checking file: ' + f + '...')
    bdNames = getBoundaryNames(f)
    if bdNames == None:
        print('File: ' + f + 'doens\'t exist')
    elif bdNames == 0:
        print('File: ' + f + 'doens\'t contain boundary field')
    else:
        boundaries[f] = bdNames
        isEqualToBlockMeshDict = compareArrays(bdNames, bmd_boundaries)
        if isEqualToBlockMeshDict:
            print('OK ----> Same fields as BlockMesh dict.')
        else:
            print('ERROR ---->')
            counter_bmd = Counter(bmd_boundaries).items()
            counter_file = Counter(bdNames).items()
            table = []
            for ii in range(0, max(len(counter_bmd), len(counter_file))):
                item1 = counter_bmd[ii][0] if ii<len(counter_bmd) else ''
                item2 = counter_file[ii][0] if ii<len(counter_file) else ''
                table.append([item1, item2])
            print(tabulate(table, headers=['BlockMeshDict', f]))


