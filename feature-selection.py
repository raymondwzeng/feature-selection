# Author: Raymond Zeng
# A simple program designed to finish project 2 of CS170
import pandas
import math
import row

DEFAULT_RATE = 0.50

# Returns the integer corresponding to the class that the series should be.
def nearestNeighborClassify(heuristics: set, series: row.row, dataframe: list[row.row]) -> int:
    closestNeighbor: row.row = None
    minDistance: float = math.inf
    for innerRow in dataframe:
        sumDistance: float = 0
        if(innerRow != series): #Only compare distance with other rows, otherwise closest neighbor would be itself
            for heuristic in heuristics:
                # print(f"Row {row[0]} with {row[1][heuristic]} and row {series[0]} with {series[1][heuristic]}")
                squaredDistance = pow(innerRow.selectionData[heuristic] - series.selectionData[heuristic], 2)
                sumDistance = sumDistance + squaredDistance
            # print(f"The total distance across all heuristics is {sumDistance}.")
            if closestNeighbor == None or sumDistance < minDistance:
                # print(f"The new closest neighbor is {row[0]}")
                minDistance = sumDistance
                closestNeighbor = innerRow
    # print(f"The closest neighbor is {closestNeighbor} with class {closestNeighbor[0]}")
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
    for _ in range(NUM_COLUMNS): # Iterate over the entire range, basically doing an O(n^2) traversal over all columns looking for columns to add.
        bestColumn = None
        maxQuality = -math.inf
        for innerColumn in range(NUM_COLUMNS): # Check all of the columns each time
            if not innerColumn in heuristics: # Do not add or even consider duplicate columns. NOTE: Now, class and data are separated, so we don't need to do the previous thing.
                setCopy = heuristics.copy()
                setCopy.add(innerColumn)
                columnQuality = kcrossfold(setCopy, dataframe)
                print(f"Heuristic {innerColumn} with existing set {heuristics} is {columnQuality}")
                if bestColumn == None or columnQuality > maxQuality:
                    bestColumn = innerColumn
                    maxQuality = columnQuality
                if bestSet == None or columnQuality > bestQuality: # Update the best set so far
                    bestSet = setCopy
                    bestQuality = columnQuality
        if bestColumn != None:
            print(f"Best next heuristic to add is {bestColumn}")
            heuristics.add(bestColumn)
            qualityList.append(maxQuality)
    print(f"Quality list: {qualityList}")
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
    for _ in range(NUM_COLUMNS): # Iterate over the entire range, basically doing an O(n^2) traversal over all columns looking for columns to add.
        worstColumn = None
        maxQuality = -math.inf
        for innerColumn in range(NUM_COLUMNS): # Check all of the columns each time
            if innerColumn in heuristics: # Do not add or even consider duplicate columns. NOTE: Now, class and data are separated, so we don't need to do the previous thing.
                setCopy = heuristics.copy()
                setCopy.remove(innerColumn)
                columnQuality = kcrossfold(setCopy, dataframe)
                print(f"Heuristic {innerColumn} with existing set {heuristics} is {columnQuality}")
                if worstColumn == None or columnQuality > maxQuality:
                    worstColumn = innerColumn # This would be the column to remove, if we get the best accuracy without it.
                    maxQuality = columnQuality
                if bestSet == None or columnQuality > bestQuality: # Update the best set so far
                    bestSet = setCopy
                    bestQuality = columnQuality
        if worstColumn != None:
            print(f"Best next heuristic to remove is {worstColumn}")
            heuristics.remove(worstColumn)
            qualityList.append(maxQuality)
    print(f"Quality list: {qualityList}")
    return bestSet 

def main():
    dataframe = pandas.read_fwf("./CS170_Large_Data__6.txt", header=None)
    rows: list[row.row] = []
    for innerRow in dataframe.iterrows():
        dataList : list[float] = innerRow[1].to_list()
        dataList.pop(0)
        rows.append(row.row(innerRow[1][0], dataList))
    print(f"The best set for this data set is {forwardSelection(rows)}")
    #TODO: User inputs their own file name.

if __name__ == "__main__":
    main()