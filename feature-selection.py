# Author: Raymond Zeng
# A simple program designed to finish project 2 of CS170
import pandas
import math
import row
import time

DEFAULT_RATE = 0.50

def printSet(inputSet: set) -> None:
    count = 0
    print("{", end="")
    for item in inputSet:
        if count != len(inputSet) - 1:
            print(item + 1, end=", ")
        else:
            print(item + 1, end="")
        count += 1
    print("}", end="")

# Returns the integer corresponding to the class that the series should be.
def nearestNeighborClassify(heuristics: set, series: row.row, dataframe: list[row.row]) -> int:
    closestNeighbor: row.row = None
    minDistance: float = math.inf
    for innerRow in dataframe:
        sumDistance: float = 0
        if(innerRow != series): #Only compare distance with other rows, otherwise closest neighbor would be itself
            for heuristic in heuristics:
                squaredDistance = pow(innerRow.selectionData[heuristic] - series.selectionData[heuristic], 2)
                sumDistance += squaredDistance
            sumDistance = math.sqrt(sumDistance)
            if closestNeighbor == None or sumDistance < minDistance:
                minDistance = sumDistance
                closestNeighbor = innerRow
    return closestNeighbor.selectionClass #The 0th column is always the class.

# Performs leave-one-out KxF across all rows, returning the percentage of success.
# Takes a set of numbers indicating the column included in heuristics.
def kcrossfold(heuristics: set, dataframe: list[row.row]) -> float:
    numRuns = 0
    numSuccess = 0
    if len(heuristics) == 0: # Return the default rate if we have an empty set.
        return DEFAULT_RATE
    for innerRow in dataframe:
        if(nearestNeighborClassify(heuristics, innerRow, dataframe) == innerRow.selectionClass):
            numSuccess += 1
        numRuns += 1
    return numSuccess/numRuns

# Performs forward selection on all of the columns and returns the best set for the job.
def forwardSelection(dataframe: list[row.row]) -> set():
    bestSet = None
    bestQuality = -math.inf
    heuristics = set() #Begin with an empty set
    qualityList = []
    if len(dataframe) == 0: # Failsafe: Return if we have 0 columns.
        return heuristics
    NUM_COLUMNS: int = len(dataframe[0].selectionData)
    print(f"Initial run of nearest neighbor with an empty set results in accuracy of {kcrossfold(heuristics, dataframe)}\nBeginning Search...")
    for _ in range(NUM_COLUMNS): # Iterate over the entire range, basically doing an O(n^2) traversal over all columns looking for columns to add.
        bestSetSoFar: set = None
        maxQuality: float = -math.inf
        for innerColumn in range(NUM_COLUMNS): # Check all of the columns each time
            if not innerColumn in heuristics: # Do not add or even consider duplicate columns. NOTE: Now, class and data are separated, so we don't need to do the previous thing.
                setCopy = heuristics.copy()
                setCopy.add(innerColumn)
                columnQuality = kcrossfold(setCopy, dataframe)
                print("New heuristic set ", end="") 
                printSet(setCopy) 
                print(f" has accuracy of {columnQuality}")
                if bestSetSoFar == None or columnQuality > maxQuality:
                    bestSetSoFar = setCopy
                    maxQuality = columnQuality
                if bestSet == None or columnQuality > bestQuality: # Update the best set so far
                    bestSet = setCopy
                    bestQuality = columnQuality
        if bestSetSoFar != None:
            print(f"Best next set to go down is ", end="")
            printSet(bestSetSoFar) 
            print(f" with a resulting accuracy of {maxQuality}")
            heuristics = bestSetSoFar
            qualityList.append(maxQuality)
    print(f"Quality list: {qualityList}")
    print(f"Best set: ", end="")
    printSet(bestSet)
    print(f" has an accuracy of {bestQuality}")
    return bestSet 

# Performs backward elimination on all of the columns and returns the best set for the job.
def backwardElimination(dataframe: list[row.row]) -> set():
    bestSet = None
    bestQuality = -math.inf
    qualityList = []
    if len(dataframe) == 0: # Failsafe: Return if we have 0 columns.
        return heuristics
    NUM_COLUMNS: int = len(dataframe[0].selectionData)
    heuristics: set[int] = set() # Begin with an empty set
    for index in range(NUM_COLUMNS): # Populate empty set
        heuristics.add(index)
    print(f"Initial run of nearest neighbor with an full set results in accuracy of {kcrossfold(heuristics, dataframe)}.\nBeginning Search...")
    for _ in range(NUM_COLUMNS): # Iterate over the entire range, basically doing an O(n^2) traversal over all columns looking for columns to add.
        bestSetSoFar: set = None
        maxQuality: float = -math.inf
        for innerColumn in range(NUM_COLUMNS): # Check all of the columns each time
            if innerColumn in heuristics: # Do not add or even consider duplicate columns. NOTE: Now, class and data are separated, so we don't need to do the previous thing.
                setCopy = heuristics.copy()
                setCopy.remove(innerColumn)
                columnQuality = kcrossfold(setCopy, dataframe)
                print("New heuristic set ", end="") 
                printSet(setCopy) 
                print(f" has accuracy of {columnQuality}")
                if bestSetSoFar == None or columnQuality > maxQuality: # The worst column is characterized by the column which, by its removal, would result in the largest accuracy.
                    bestSetSoFar = setCopy
                    maxQuality = columnQuality
                if bestSet == None or columnQuality > bestQuality: # Update the best set globally
                    bestSet = setCopy
                    bestQuality = columnQuality
        if bestSetSoFar != None:
            print(f"Best next set to go down is ", end="")
            printSet(bestSetSoFar) 
            print(f" with a resulting accuracy of {maxQuality}")
            heuristics = bestSetSoFar
            qualityList.append(maxQuality)
    print(f"Quality list: {qualityList}")
    print(f"Best set: ", end="")
    printSet(bestSet)
    print(f" has an accuracy of {bestQuality}")
    return bestSet 

def main():
    print("Welcome to Raymond's Feature Selection Program.")
    fileName = input("Input the name of the file that you wish to read: ")
    dataframe = pandas.read_fwf(fileName, header=None)
    rows: list[row.row] = []
    for innerRow in dataframe.iterrows():
        dataList : list[float] = innerRow[1].to_list()
        dataList.pop(0)
        rows.append(row.row(innerRow[1][0], dataList))
    algorithm = input("Input 1 for forward selection, or 2 for backward elimination: ")
    timeNow: float = 0
    if len(rows) == 0:
        print("No rows - exiting.")
        return
    print(f"There are {len(rows[0].selectionData)} features, and {len(rows)} rows.")
    if algorithm == '1':
        timeNow = time.time()
        forwardSelection(rows)   
    elif algorithm == '2':
        timeNow = time.time()
        backwardElimination(rows)
    else:
        print("Invalid response.")
    if timeNow != 0:
        print(f"Time spent on algorithm in seconds: {round(time.time() - timeNow, 2)}")

if __name__ == "__main__":
    main()