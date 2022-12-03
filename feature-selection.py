# Author: Raymond Zeng
# A simple program designed to finish project 2 of CS170
import pandas
import math

DEFAULT_RATE = 50.0

# Returns the integer corresponding to the class that the series should be .
def nearestNeighborClassify(heuristics: set, series: pandas.Series, dataframe: pandas.DataFrame) -> int:
    closestNeighbor: pandas.Series = None
    minDistance = math.inf
    for row in dataframe.iterrows():
        sumDistance = 0
        if(row != series): #Only compare distance with other rows, otherwise closest neighbor would be itself
            for heuristic in heuristics:
                squaredDistance = pow(row[1][heuristic] - series[1][heuristic], 2)
                print(f"The squared distance between rows {series[0]} and {row[0]} is {squaredDistance}")
                sumDistance = sumDistance + squaredDistance
            print(f"The total distance across all heuristics is {sumDistance}.")
            if closestNeighbor == None or sumDistance < minDistance:
                minDistance = sumDistance
                closestNeighbor = row
    print(f"The closest neighbor is {closestNeighbor} with class {closestNeighbor[1][0]}")
    return closestNeighbor[1][0] #The first column is always the class.

# Performs leave-one-out KxF across all rows, returning the percentage of success.
# Takes a set of numbers indicating the column included in heuristics.
def kcrossfold(heuristics: set, dataframe: pandas.DataFrame) -> float:
    successRate = DEFAULT_RATE
    return successRate

def main():
    dataframe = pandas.read_fwf("./CS170_Tiny_Data__26.txt", header=None)
    heuristics = set() #Begin with an empty set
    qualityList = []
    for column in dataframe.columns:
        bestColumn = None
        maxQuality = DEFAULT_RATE
        for innerColumn in dataframe.columns:
            if(column != innerColumn and not (innerColumn in heuristics)):
                columnQuality = kcrossfold(heuristics + innerColumn, dataframe)
                if bestColumn == None or columnQuality > maxQuality:
                    bestColumn = innerColumn
                    maxQuality = columnQuality
        if bestColumn != None:
            print(f"Best next heuristic to add is {bestColumn}")
            set.add(bestColumn)
            qualityList.append(maxQuality)
    #TODO: User inputs their own file name.

if __name__ == "__main__":
    main()