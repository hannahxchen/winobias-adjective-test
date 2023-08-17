import csv


NUM_ACCURACIES = 4
CORRECT = 1
INCORRECT = 2
UNSURE = 3
OTHER = 4


def makeStatsFile(readCorAnsFrom, readIncAnsFrom, readCompFrom, writeTo, numRows):
    numCompFiles = len(readCompFrom)
    compHeadings = [None] * numCompFiles

    # First read in each set of answers
    corAnswers = [None] * numRows
    with open(readCorAnsFrom, "r") as file:
        for i in range(numRows):
            corAnswers[i] = file.readline().strip()
            
    incAnswers = [None] * numRows
    with open(readIncAnsFrom, "r") as file:
        for i in range(numRows):
            incAnswers[i] = file.readline().strip()
    
    # Allocate space for the 2d list of completions
    completions = [None] * numCompFiles
    for i in range(numCompFiles):
        completions[i] = [None] * numRows
        
    # Read in each completions file
    for i in range(numCompFiles):
        with open(readCompFrom[i], "r") as file:
            compHeadings[i] = file.readline().strip()
            for j in range(numRows):
                completions[i][j] = file.readline().strip()
    
    # Allocate space for 2d list of accuracies
    accuracies = [None] * NUM_ACCURACIES
    for i in range(NUM_ACCURACIES):
        accuracies[i] = [None] * numCompFiles
        
    # Calculate accuracies of each set of completions
    for i in range(numCompFiles):
        accuracySet = getAccuraciesOf(completions[i], corAnswers, incAnswers, numRows)
        for j in range(NUM_ACCURACIES):
            accuracies[j][i] = accuracySet[j]
            
    # Output everything into csv
    with open(writeTo, "w", newline = '') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        # Write headings
        csvwriter.writerow(["Prompt", "Correct Answers"] + compHeadings)
        
        # Write completions
        for i in range(numRows):
            csvrow = [str(i + 1)]
            csvrow.append( corAnswers[i] )
            for j in range(numCompFiles):
                csvrow.append( completions[j][i] )
            csvwriter.writerow(csvrow)
            
        # Write accuracies
        csvwriter.writerow(["Correct:", "---"] + accuracies[0])
        csvwriter.writerow(["Incorrect:", "---"] + accuracies[1])
        csvwriter.writerow(["Unsure:", "---"] + accuracies[2])
        csvwriter.writerow(["Other:", "---"] + accuracies[3])
    
    
def getAccuraciesOf(compList, corAnswers, incAnswers, numRows):
    # Determine the number of each accuracy within the list
    numCorrect = 0
    numIncorrect = 0
    numUnsure = 0
    numOther = 0

    for i in range( len(compList) ):
        if compList[i] == corAnswers[i]:
            numCorrect += 1
        elif compList[i] == incAnswers[i]:
            numIncorrect += 1
        elif compList[i] == "unsure":
            numUnsure += 1
        else:
            numOther += 1
    
    # Take the results as fractions of the number of prompts, and round to the nearest tenth of a percent
    accuracySet = [None] * NUM_ACCURACIES
    accuracySet[0] = round( numCorrect / numRows * 100, 1 )
    accuracySet[1] = round( numIncorrect / numRows * 100, 1 )
    accuracySet[2] = round( numUnsure / numRows * 100, 1 )
    accuracySet[3] = round( numOther / numRows * 100, 1 )
    return accuracySet
    
    
def makeHeatMap(readCorAnsFrom, readIncAnsFrom, readOutFrom, writeTo, numRows, numCols):
    headings = [None] * numCols
    heatMap = [None] * numRows
    
    # First read in each set of answers
    corAnswers = [None] * numRows
    with open(readCorAnsFrom, "r") as file:
        for i in range(numRows):
            corAnswers[i] = file.readline().strip()
            
    incAnswers = [None] * numRows
    with open(readIncAnsFrom, "r") as file:
        for i in range(numRows):
            incAnswers[i] = file.readline().strip()

    # Now read the actual csv file
    with open(readOutFrom, "r") as csvfile:
        csvreader = csv.reader(csvfile)
        
        # Get headings from first row
        line = next(csvreader)
        headings = line[2:] # Exclude the first two elements at the top, "Prompt" and "Correct Answers"
        
        # Now iterate through each row below and record results as it goes
        for i in range(numRows):
            line = next(csvreader)
            
            writeRow = [None] * numCols
            for j in range(numCols):
                cell = line[j + 2] # Use j + 2 in line to skip the first two columns for the same reasons as above
                if cell == corAnswers[i]:
                    writeRow[j] = CORRECT
                elif cell == incAnswers[i]:
                    writeRow[j] = INCORRECT
                elif cell == "unsure":
                    writeRow[j] = UNSURE
                else:
                    writeRow[j] = OTHER
            
            heatMap[i] = writeRow

    # Write results to file
    with open(writeTo, "w") as csvfile:
        csvwriter = csv.writer(csvfile)
        
        csvwriter.writerow(headings)
        for row in heatMap:
            csvwriter.writerow(row)