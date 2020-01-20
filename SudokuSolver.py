from tkinter import *
from tkinter import font
from tkinter import messagebox
import numpy
import time
#REMEBER TO PUT CASE IF SUDOKU IS FILLED COMPLETELY

def getQuadrant(row, column):
    global sudoku
    threeRow = []
    columnSet = int
    quadrent = numpy.empty((3, 3), int)

    if row >= 0 and row <= 2:
        threeRow = sudoku[0:3]
    elif row >= 3 and row <= 5:
        threeRow = sudoku[3:6]
    elif row >= 6 and row <= 8:
        threeRow = sudoku[6:9]

    if column >= 0 and column <= 2:
        columnSet = 0
    elif column >= 3 and column <= 5:
        columnSet = 3
    elif column >= 6 and column <= 8:
        columnSet = 6

    counter = 0
    for row in threeRow:
        quadrent[counter:3] = row[columnSet: columnSet + 3]
        counter += 1

    return quadrent

def checkInput(number, row, column):
    global guiList, sudoku, closeRan
    n = 8 * currentInput[0]

    quadrant = getQuadrant(row, column)
    rowCheck = numpy.isin(number, sudoku[row])
    columnList = numpy.empty(9, int)

    counter = 0
    for sudokuRow in sudoku:
        columnList[counter] = sudokuRow[column: column + 1]
        counter += 1

    columnCheck = numpy.isin(number, columnList)
    quadrantCheck = numpy.isin(number, quadrant)

    if showProcess.get() == 1:
        try:
            guiList[n + row + column][0].delete(0, END)
            guiList[n + row + column][0].insert(0, number)
            guiList[n + row + column][0].update()
            time.sleep(0.01)

            if number == 9 and (rowCheck or columnCheck or quadrantCheck):
                guiList[n + row + column][0].delete(0, END)
        except:
            sys.exit(0)

    if (not rowCheck) and (not columnCheck) and (not quadrantCheck):
        return True

    return False

def displayProcess(n, number):
    global currentInput, guiList

    guiList[n + currentInput[0] + currentInput[1]][0].insert(0, number)

def placeInput(number):
    global currentInput, sudoku

    if checkInput(number, currentInput[0], currentInput[1]):
        sudoku[currentInput[0]][currentInput[1]] = number
        return True

    return False

def updateCurrentInput(positive):
    global currentInput, unchangable

    if positive:
        if (currentInput[1] == 8):
            currentInput[1] = 0
            currentInput[0] = currentInput[0] + 1
        else:
            currentInput[1] = currentInput[1] + 1
    else:
        if (currentInput[1] == 0):
            currentInput[1] = 8
            currentInput[0] = currentInput[0] - 1
        else:
            currentInput[1] = currentInput[1] - 1

    currentUnchangable = False
    while(True):
        for pos in unchangable:
            if pos == currentInput:
                currentUnchangable = True

        if currentUnchangable:
            currentUnchangable = False
            if positive:
                if (currentInput[1] == 8):
                    currentInput[1] = 0
                    currentInput[0] = currentInput[0] + 1
                else:
                    currentInput[1] = currentInput[1] + 1
            else:
                if (currentInput[1] == 0):
                    currentInput[1] = 8
                    currentInput[0] = currentInput[0] - 1
                else:
                    currentInput[1] = currentInput[1] - 1
        else:
            break

def startDisplay():
    global showProcess

    for _ in range(81):
        input = StringVar()
        sudokuBox = Entry(root, width=3, textvariable=input, justify=CENTER, font=sudokuFont)
        sudokuBox.delete(0, END)
        guiList.append([sudokuBox, input])

    global readInputButton, showProcessButton
    readInputButton = Button(root, text="Enter", width=12, command=readInput)
    showProcessButton = Checkbutton(root, text="Show Process", variable=showProcess)

    rowCounter = 0
    columnCounter = 0
    for pair in guiList:
        if columnCounter == 0:
            pair[0].grid(row=rowCounter, column=columnCounter, padx=(10, 0), ipadx=10, ipady=10)

        if columnCounter == 8:
            pair[0].grid(row=rowCounter, column=columnCounter, padx=(0, 10), ipadx=10, ipady=10)

        if rowCounter == 2 or rowCounter == 5:
            pair[0].grid(row=rowCounter, column=columnCounter, pady=(0, 5), ipadx=10, ipady=10)

        if columnCounter == 2 or columnCounter == 5:
            pair[0].grid(row=rowCounter, column=columnCounter, padx=(0, 5), ipadx=10, ipady=10)

        else:
            pair[0].grid(row=rowCounter, column=columnCounter, ipadx=10, ipady=10)

        if columnCounter == 8:
            columnCounter = 0
            rowCounter += 1
        else:
            columnCounter += 1

    readInputButton.grid(row=rowCounter, column=3, columnspan=3, pady=10)
    showProcessButton.grid(row=rowCounter, column=0, columnspan=3, pady=10)

def readInput():
    global currentInput, unchangable, guiList, sudoku

    readInputButton.configure(state=DISABLED)
    showProcessButton.configure(state=DISABLED)
    readInputButton.update()

    firstBlankNotFound = True
    rowCounter = 0
    columnCounter = 0
    for pair in guiList:
        if pair[1].get() != "":
            if pair[1].get() == "1" or pair[1].get() == "2" or pair[1].get() == "3"\
            or pair[1].get() == "4" or pair[1].get() == "5" or pair[1].get() == "6" or pair[1].get() == "7"\
            or pair[1].get() == "8" or pair[1].get() == "9":
                sudoku[rowCounter, columnCounter] = int(pair[1].get())
                unchangable.append([rowCounter, columnCounter])
            else:
                messagebox.showinfo("Incorrect Input", "A Sudoku can only accept numbers between 1 - 9, can not solve!")
                return False

        elif firstBlankNotFound:
            firstInput = [rowCounter, columnCounter]
            firstBlankNotFound = False

        if columnCounter == 8:
            columnCounter = 0
            rowCounter += 1
        else:
            columnCounter += 1

    if firstBlankNotFound:
        messagebox.showinfo("Sudoku Filled", "Every cell in the sudoku is filled, can not solve!")
        return False

    elif unsolvableCheck():
        messagebox.showinfo("Sudoku Unsolvable", "The information does not follow the rules of Sudoku, can not solve!")
        return False

    else:
        currentInput = firstInput
        solve()
        printSudoku()

def unsolvableCheck():
    global unchangable

    alreadyCheck = []
    for coord in unchangable:
        row = coord[0]
        column = coord[1]
        quadrant = getQuadrant(row, column)
        number = sudoku[coord[0], coord[1]]
        columnList = numpy.empty(9, int)

        counter = 0
        for sudokuRow in sudoku:
            columnList[counter] = sudokuRow[column: column + 1]
            counter += 1

        rowUnique, rowCount = numpy.unique(sudoku[row], return_counts=True)
        columnUnique, columnCount = numpy.unique(columnList, return_counts=True)
        quadrantUnique, quadrantCount = numpy.unique(quadrant, return_counts=True)

        rowDict = dict(zip(rowUnique, rowCount))
        columnDict = dict(zip(columnUnique, columnCount))
        quadrantDict = dict(zip(quadrantUnique, quadrantCount))

        if rowDict[number] >= 2 or columnDict[number] >= 2 or quadrantDict[number] >= 2:
            return True

    return False

def solve():
    inputToPlace = 1

    while (True):
        backtrack = False
        inputPlaced = placeInput(inputToPlace)

        if inputPlaced:
            inputToPlace = 1
            updateCurrentInput(True)

        else:
            if inputToPlace == 9:
                if not inputPlaced:
                    backtrack = True
                inputToPlace = 1
            else:
                inputToPlace += 1

        if backtrack:
            backtrack = False
            sudoku[currentInput[0]][currentInput[1]] = 0

            if currentInput == firstInput:
                break

            updateCurrentInput(False)
            inputToPlace = sudoku[currentInput[0]][currentInput[1]]

        if currentInput[0] == 9 and currentInput[1] == 0:
            break

def printSudoku():
    global guiList

    rowCounter = 0
    columnCounter = 0
    for pair in guiList:
        pair[0].delete(0, END)
        pair[0].insert(0, sudoku[rowCounter, columnCounter])

        if columnCounter == 8:
            columnCounter = 0
            rowCounter += 1
        else:
            columnCounter += 1

root = Tk()
root.title(r"Sudoku Solver")
root.iconbitmap()
sudokuFont = font.Font(family="Helvetica", size=15)

sudoku = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0]])

currentInput = [0, 0]
firstInput = []
unchangable = []
guiList = []
showProcess = IntVar()

startDisplay()

root.mainloop()
