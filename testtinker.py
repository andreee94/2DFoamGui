from Tkinter import * # python 2
import Tkinter, Tkconstants, tkFileDialog
import ttk
import myutil as myutil
import os
from face import Face
from block import Block

 
#from tkinter import * # python 3
 
window = Tk()
 
window.title("Welcome to 2D FOAM GUI")

levelRowLoad = 0
levelRowBlocks = 4
levelRowFaces = 8
levelRowSave = 12
levelRowError = 14

global x, y, z
global fig, fig_num, ax
cellsize = 0.1
faces = {}
global blocks
blocks = []

global windowTemp, text, scrollbar
global blockNameEntry, blockPointsEntry
global faceNameEntry, facePointsEntry, faceTypeEntry
windowTemp = None

def createBlockInterface():
    global  blockPointsEntry, blockNameEntry
    ttk.Separator(window, orient=HORIZONTAL).grid(row=levelRowBlocks, columnspan=6, sticky="ew")
    Label(window, text="BLOCKS definition").grid(column=2, row=levelRowBlocks, columnspan=2, rowspan=2)
    Label(window, text="Zone name (optional)=").grid(column=2, row=levelRowBlocks+1, columnspan=2, rowspan=2)
    Label(window, text="Points of the block (4) = ").grid(column=2, row=levelRowBlocks+2, columnspan=2, rowspan=2)
    blockNameEntry = Entry(window, width=15)
    blockNameEntry.grid(column=4, row=levelRowBlocks+1, columnspan=1, rowspan=2)
    blockPointsEntry = Entry(window, width=15)
    blockPointsEntry.grid(column=4, row=levelRowBlocks+2, columnspan=1, rowspan=2)
    Button(window, text="Apply", command=btnBlockClicked).grid(column=6, row=levelRowBlocks+1, columnspan=3, rowspan=3)

def createFaceInterface():
    global faceNameEntry, facePointsEntry, faceTypeEntry # strange thing of python
    ttk.Separator(window, orient=HORIZONTAL).grid(row=levelRowFaces, columnspan=6, sticky="ew")
    Label(window, text="FACES definition").grid(column=2, row=levelRowFaces, columnspan=2, rowspan=2)
    Label(window, text="Face name =").grid(column=2, row=levelRowFaces+1, columnspan=2, rowspan=2)
    Label(window, text="Face type =").grid(column=2, row=levelRowFaces+2, columnspan=2, rowspan=2)
    Label(window, text="Points of the Face (2)= ").grid(column=2, row=levelRowFaces+3, columnspan=2, rowspan=2)
    faceNameEntry = Entry(window, width=15)
    faceNameEntry.grid(column=4, row=levelRowFaces+1, columnspan=1, rowspan=2)
    faceTypeEntry = Entry(window, width=15)
    faceTypeEntry.grid(column=4, row=levelRowFaces+2, columnspan=1, rowspan=2)
    facePointsEntry = Entry(window, width=15)
    facePointsEntry.grid(column=4, row=levelRowFaces+3, columnspan=1, rowspan=2)
    Button(window, text="Apply", command=btnFaceClicked).grid(column=6, row=levelRowFaces+2, columnspan=3, rowspan=3)

def btnBlockClicked():
    if blockPointsEntry.get() == None:
        printError('ERROR. Empty points field in block form')
    else:
        zoneName = blockNameEntry.get()
        blockPoints = [int(n) for n in blockPointsEntry.get().split()]
        if len(blockPoints)  % 4 != 0:
            printError('ERROR. Number of points must be multiple of 4')
        else:
            for i in range(0, len(blockPoints)/4):
                addBlock(Block(zoneName, [blockPoints[2*i], blockPoints[2*i+1], blockPoints[2*i+2], blockPoints[2*i+3]]))
            updateFacesAndBlocksPlot()
            printError('')
            printTemp()

def btnFaceClicked():
    if faceNameEntry.get() == None or facePointsEntry.get() == None or faceTypeEntry.get() == None:
        printError('ERROR. Empty fields in face form')
    else:
        faceName = faceNameEntry.get()
        faceType = faceTypeEntry.get()
        facePoints = [int(n) for n in facePointsEntry.get().split()]
        if len(facePoints)  % 2 == 1:
            printError('ERROR. Odd Number of points')
        else:
            for i in range(0, len(facePoints)/2):
               addFace(faceName, Face(faceName, faceType, [facePoints[2*i], facePoints[2*i+1]]))
            updateFacesAndBlocksPlot()
            printError('')
            printTemp()

def writeBlockMeshDict(temp=False):
    if temp:
        filename = '.temp'
    else: filename = 'blockMeshDict'
    with open(filename, 'w+') as file:
        writeInit(file)
        writePoints(file)
        writeEdges(file)
        writeFaces(file)
        writeBlocks(file)
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

def writePoints(file):
    file.write('vertices' + '\n')
    file.write('(' + '\n')
    file.write('   #Front points' + '\n')
    for i in range(0, len(x)):
        file.write('   (')
        file.write(str(x[i]) + '   ')
        file.write(str(y[i]) + '   ')
        file.write(str(z[0]))
        file.write(')' + ' ' + '#' + str(i) + '\n')

    file.write('   #Back points' + '\n')
    for i in range(0, len(x)):
        file.write('   (')
        file.write(str(x[i]) + '   ')
        file.write(str(y[i]) + '   ')
        file.write(str(z[1]))
        file.write(')' + ' ' + '#' + str(len(x) + i) + '\n')

    file.write(');\n\n')

def writeBlocks(file):
    file.write('blocks\n(\n')
    file.write(Block.printBlocks(blocks, len(x), x, y, z, cellsize))
    file.write(');\n\n')

def writeEdges(file):
    file.write('edges\n(\n')
    file.write(');\n\n')

def writeFaces(file):
    file.write('boundary\n(\n')
    for f in faces:
        file.write(Face.printFaces(faces[f], len(x)))
        file.write('\n\n')
    file.write(');\n\n')

def writePatchPairs(file):
    file.write('mergePatchPairs\n(\n')
    file.write(');\n\n')

def btnSaveClicked():
    writeBlockMeshDict()

def btnLoadClicked():
    global x,y,z
    global fig, fig_num, ax
    fileInput = tkFileDialog.askopenfilename(initialdir = os.getcwd(),title = "Select file",filetypes = (("All files","*.*"),("All files","*")))
    if fileInput != None:
        # graphics
        Label(window, text=fileInput).grid(column=4, row=levelRowLoad+2, columnspan=4, rowspan=2) # filename
        createBlockInterface()
        createFaceInterface()
        Button(window, text="Save", command=btnSaveClicked).grid(column=4, row=levelRowSave, columnspan=2, rowspan=2)  #save button
        updateGridsize()
        # load and plot
        x, y, z = myutil.xyzFromFile(fileInput)
        fig, fig_num, ax = myutil.plotPoints(x, y, z)

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

def updateFacesAndBlocksPlot():
    global x,y,z
    global fig, fig_num, ax
    myutil.plotFacesAndBlocks(fig, fig_num, ax, x, y, z, faces, blocks)

def printError(msg):
    Label(window, text=msg).grid(column=2, row=levelRowError+2, columnspan=8, rowspan=1)

def printTemp():
    global windowTemp, text, scrollbar
    #if windowTemp == None:
    windowTemp = Tk()
    scrollbar = Scrollbar(windowTemp)
    scrollbar.pack(side=RIGHT, fill=Y)
    text = Text(windowTemp, wrap=WORD, yscrollcommand=scrollbar.set)#, state="disabled")
    writeBlockMeshDict(temp=True)
    with open('.temp', 'r') as myfile:
        t = myfile.read()
    try: text.delete(0, END)
    except: pass
    text.insert(INSERT, t)
    text.pack(fill=BOTH, expand=1)
    scrollbar.config(command=text.yview)
    windowTemp.mainloop()

def updateGridsize():
    col_count, row_count = window.grid_size()
    for col in xrange(col_count):
        window.grid_columnconfigure(col, minsize=20)
    for row in xrange(row_count):
        window.grid_rowconfigure(row, minsize=20)

loadBtn = Button(window, text="Load", command=btnLoadClicked)
loadBtn.grid(column=4, row=levelRowLoad, columnspan=2, rowspan=2)
#btn.pack()

Label(window, text="Choose File...").grid(column=2, row=levelRowLoad, columnspan=2, rowspan=2)

#window.filename = tkFileDialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))

#lbl.pack()

updateGridsize()
window.geometry('600x400')
window.mainloop()