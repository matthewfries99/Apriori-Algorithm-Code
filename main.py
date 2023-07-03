# Matthew Fries, Assignment #6
# This program implements and runs the Apriori Algorithm in order to find the largest and most frequent
# subset of transactions in a data set. This algorithm is commonly used in marketing research in order
# to find which products in a store are bought most frequently together my customers. Researchers are
# then able to utilize this data to discover what items should be placed near each other for the most profit.
# The numbers in the data.txt file each represent a different item at a store. Ex: 1=Eggs, 2=Milk, etc.
import itertools


def apriori(trans, newCand, freq, kCtr, minSup):
    newFreq = []
    tempCand = []
    kCtr += 1
    # Create new frequency list based on candidate list and transaction list
    for row in newCand:
        numCount = 0
        for transaction in trans:
            if all(item in transaction for item in row):
                numCount += 1
                if numCount == minSup:
                    newFreq.append([row])
    # Flatten 3D list to 2D list
    Output = [elem for twod in newFreq for elem in twod]
    freq = Output.copy()
    print("\nNew Frequency List: ")
    print(freq)
    # Create new candidate list by joining all combinations of frequent list
    for row in freq:
        for row2 in freq:
            if row[0:kCtr] == row2[0:kCtr]:
                rest = list(set(row + row2))
                rest.sort()
                if rest not in tempCand:
                    if len(rest) == len(row)+1:
                        tempCand.append(rest)
    newCand = tempCand.copy()
    tempCand.clear()
    print("\nNew candidate list: ")
    print(newCand)
    # Prune new candidate list by using frequent list
    posComb = []
    loopCtr = 0
    # Find all possible combinations of new candidate list
    for row in newCand:
        for r in range(len(row) + 1):
            for combination in itertools.combinations(row, r):
                combination = list(combination)
                if len(combination) == len(row)-1:
                    posComb.append(combination)

    print("Possible combinations in New candidate list: ")
    print(posComb)

    # Complete pruning step
    index = 0
    combCtr = 0
    for row in newCand:
        loopCtr = 0
        while loopCtr < 3:
            if all(item in row for item in posComb[index]):
                combCtr += 1
                if combCtr == 3:
                    tempCand.append(row)
                    combCtr = 0
                if combCtr % 3 == 0:
                    combCtr = 0
            loopCtr += 1
            index += 1

    # Set final new candidate list based on pruning step
    newCand.clear()
    newCand = tempCand.copy()

    print("New candidate list after pruning: ")
    print(newCand)
    return trans, newCand, freq, kCtr


def main():
    # Read in transactions from data file
    trans = []
    datafile = open("data.txt", "r")
    line = datafile.readline().rstrip()
    while line != "":
        line = line.split(",")
        trans.append(line)
        line = datafile.readline().rstrip()

    minSup = int(input("Minimum support value: \n"))
    print("Transaction List: ")
    print(trans)

    # Create C1 list based on transaction list
    cand = []
    for row in trans:
        for num in row:
            if not any([e[0] == num for e in cand]):
                cand.append([num])
    cand.sort()
    # print(cand)


    # Create F1 list based on minimum support value
    freq = []
    numCtr = 0
    loopCtr = 0
    while loopCtr < len(cand):
        c = cand[loopCtr][0]
        for row in trans:
            for num in row:
                if c == num:
                    numCtr += 1
                    if numCtr == minSup:
                        freq.append([num])
        loopCtr += 1
        numCtr = 0

    # Create C2 list by joining all combinations of F1 list
    newCand = []
    loopCtr2 = 0
    loopCtr3 = 1
    while loopCtr2 < len(freq):
        f = freq[loopCtr2][0]
        for num in freq:
            while loopCtr3 < len(freq):
                if int(freq[loopCtr3][0]) > int(f):
                    newCand.append([f, freq[loopCtr3][0]])
                loopCtr3 += 1
        loopCtr2 += 1
        loopCtr3 = 0
    print("\nCandidate List: ")
    print(newCand)

    kCtr = 0
    while len(freq) != 1 and len(freq) != 0:
        trans, newCand, freq, kCtr = apriori(trans, newCand, freq, kCtr, minSup)
        apriori(trans, newCand, freq, kCtr, minSup)

    if len(freq) == 1:
        print("Largest most frequent subset found: ")
        print(freq)

    if len(freq) == 0:
        print("No subset found that meets minimum support value.")


main()
