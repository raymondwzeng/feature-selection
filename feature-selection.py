# Author: Raymond Zeng
# A simple program designed to finish project 2 of CS170
import pandas
import math

DEFAULT_RATE = 0.50

# Returns the integer corresponding to the class that the series should be.
def nearestNeighborClassify(heuristics: set, series: pandas.Series, dataframe: pandas.DataFrame) -> int:
    closestNeighbor: pandas.Series = None
    minDistance: float = math.inf
    for row in dataframe.iterrows():
        sumDistance: float = 0
        if(row[0] != series[0]): #Only compare distance with other rows, otherwise closest neighbor would be itself
            for heuristic in heuristics:
                # print(f"Row {row[0]} with {row[1][heuristic]} and row {series[0]} with {series[1][heuristic]}")
                squaredDistance = pow(row[1][heuristic] - series[1][heuristic], 2)
                sumDistance = sumDistance + squaredDistance
            # print(f"The total distance across all heuristics is {sumDistance}.")
            if closestNeighbor == None or sumDistance < minDistance:
                # print(f"The new closest neighbor is {row[0]}")
                minDistance = sumDistance
                closestNeighbor = row
    # print(f"The closest neighbor is {closestNeighbor} with class {closestNeighbor[0]}")
    return closestNeighbor[1][0] #The 0th column is always the class.

# Performs leave-one-out KxF across all rows, returning the percentage of success.
# Takes a set of numbers indicating the column included in heuristics.
def kcrossfold(heuristics: set, dataframe: pandas.DataFrame) -> float:
    numRuns = 0
    numSuccess = 0
    if len(heuristics) == 0: # Return the default rate if we have an empty set.
        return DEFAULT_RATE
    for row in dataframe.iterrows():
        guessClass: int = nearestNeighborClassify(heuristics, row, dataframe)
        if(nearestNeighborClassify(heuristics, row, dataframe) == row[1][0]):
            numSuccess += 1
        numRuns += 1
    return numSuccess/numRuns

# Performs forward selection on all of the columns and returns the best set for the job.
def forwardSelection(dataframe: pandas.DataFrame) -> set():
    bestSet = None
    bestQuality = -math.inf
    heuristics = set() #Begin with an empty set
    qualityList = []
    for _ in range(len(dataframe.columns)): # Iterate over the entire range, basically doing an O(n^2) traversal over all columns looking for columns to add.
        bestColumn = None
        maxQuality = DEFAULT_RATE
        for innerColumn in dataframe.columns: # Check all of the columns each time
            if innerColumn > 0 and not innerColumn in heuristics: # Avoid column 0 (the class)
                setCopy = heuristics.copy()
                setCopy.add(innerColumn)
                columnQuality = kcrossfold(setCopy, dataframe)
                print(f"Heuristic {innerColumn} with existing set {heuristics} is {columnQuality}")
                if bestColumn == None or columnQuality > maxQuality:
                    bestColumn = innerColumn
                    maxQuality = columnQuality
                if bestSet == None or columnQuality > bestQuality: # Update the best set so far
                    bestSet = setCopy
                    bestQuality = maxQuality
        if bestColumn != None:
            print(f"Best next heuristic to add is {bestColumn}")
            heuristics.add(bestColumn)
            qualityList.append(maxQuality)
    print(f"Quality list: {qualityList}")
    return bestSet 

# Performs backward selection, starting with the full set and eliminating one at a time. Also returns the best set to use.
def backwardSelection(dataframe: pandas.DataFrame) -> set():
    bestSet = None
    bestQuality = -math.inf
    heuristics = set() #Begin with an empty set
    for column in dataframe.columns: # Copy the heuristics into the set.
        if column > 0: # 0 column is class label
            heuristics.add(column)
    qualityList = []
    for _ in range(len(dataframe.columns)): # Iterate over the entire range, basically doing an O(n^2) traversal over all columns looking for columns to add.
        bestColumn = None
        maxQuality = DEFAULT_RATE
        for innerColumn in dataframe.columns: # Check all of the columns each time
            if innerColumn > 0 and innerColumn in heuristics: # Avoid column 0 (the class)
                setCopy = heuristics.copy()
                setCopy.remove(innerColumn) # Remove items one by one
                columnQuality = kcrossfold(setCopy, dataframe)
                print(f"Set {setCopy} has a quality of {columnQuality}")
                if bestColumn == None or columnQuality > maxQuality:
                    bestColumn = innerColumn
                    maxQuality = columnQuality
                if bestSet == None or columnQuality > bestQuality: # Update the best set so far
                    print(f"New set: {setCopy} has column quality {columnQuality} > {bestQuality}")
                    bestSet = setCopy
                    bestQuality = columnQuality
        if bestColumn != None:
            print(f"Best next heuristic to remove is {bestColumn}")
            heuristics.remove(bestColumn)
            qualityList.append(maxQuality)
    print(f"Quality list: {qualityList}")
    return bestSet

def main():
    dataframe = pandas.read_fwf("./CS170_Small_Data__96.txt", header=None)
    print(f"The best set for this data set is {backwardSelection(dataframe)}")
    #TODO: User inputs their own file name.

if __name__ == "__main__":
    main()