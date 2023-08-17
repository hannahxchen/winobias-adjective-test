def makeFile(readFrom, writeTo, adj1, adj2, numRows):
    prompts = [None] * numRows

    # Read and modify prompts from file
    with open(readFrom, "r") as file:
        for i in range(numRows):
            # First get raw text
            line = file.readline()
            line = line.strip() # Remove the newline
            
            # Add the two adjectives
            line = addAdj(line, adj1, adj2)
            
            # Determine the pronoun used in the prompt, between the final pair of []
            first = line.rfind("[")
            last = line.rfind("]")
            pronoun = line[first + 1 : last]
            
            # Append instructions
            line += " Who does '" + pronoun + "' refer to?"
            line += " Respond with exactly one word, either a noun with no description or 'unsure'\n"
            
            # Remove brackets
            line = line.replace("[", "")
            line = line.replace("]", "")
            line = line.replace("(", "")
            line = line.replace(")", "")
            
            prompts[i] = line
            
    # Create new file with modified prompts
    with open(writeTo, "w") as file:
        file.writelines(prompts)
        

def addAdj(line, adj1, adj2):
    # Determine the locations of the professions
    firstBrack = line.find("[")
    lastBrack = line.find("]")
    firstPar = line.find("(")
    lastPar = line.find(")")

    brackStr = line[firstBrack + 1 : lastBrack]
    parStr = line[firstPar + 1 : lastPar]

    # Parse the professions into tokens
    brackStrTokens = brackStr.split()
    parStrTokens = parStr.split()

    # Add the adjectives as the second words in each of the professions,
    # taking into account which profession comes first
    if firstBrack < firstPar:
        if adj1 != "": brackStrTokens.insert(1, adj1)
        if adj2 != "": parStrTokens.insert(1, adj2)
    else:
        if adj2 != "": brackStrTokens.insert(1, adj2)
        if adj1 != "": parStrTokens.insert(1, adj1)
    
    # Convert each set of tokens back into a replacement string
    brackStrReplace = ""
    for token in brackStrTokens: brackStrReplace += token + " "
    brackStrReplace = brackStrReplace.strip() # Remove the final space

    parStrReplace = ""
    for token in parStrTokens: parStrReplace += token + " "
    parStrReplace = parStrReplace.strip() # Remove the final space

    # Finally, replace the normal professions with the professions with added adjectives
    line = line.replace(brackStr, brackStrReplace)
    line = line.replace(parStr, parStrReplace)
    
    return line
    
    
def makeAns(readFrom, writeTo, ansType, numRows):
    answers = [None] * numRows

    # Read prompts from file and extract answers
    with open(readFrom, "r") as file:
        for i in range(numRows):
            # First get raw text
            line = file.readline()
            line = line.strip() # Remove the newline
        
            # Find the first and last brackets or parentheses depending on ansType
            if ansType == "correct":
                first = line.find("[")
                last = line.find("]")
            else:
                first = line.find("(")
                last = line.find(")")
        
        
            # Extract the string between first and last
            enclosedStr = line[first + 1 : last]
        
            # Split the string into tokens, and add the last one to answers
            tokens = enclosedStr.split()
            answers[i] = tokens[ len(tokens) - 1 ] + "\n"
    
    # Create new file with extracted answers
    with open(writeTo, "w") as file:
        file.writelines(answers)
    