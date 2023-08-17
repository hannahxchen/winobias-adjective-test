import openai
import time

openai.api_key = ""


def getCompletionsOf(readFrom, writeTo, modelName, heading, numRows):
    # Read in given number of prompts
    prompts = [None] * numRows
    with open(readFrom, "r") as file:
        for i in range(numRows):
            prompts[i] = file.readline().strip()
    
    # Get responses from API
    completions = [None] * numRows
    for i in range(numRows):
        # Get response from model
        response = None
        gotResponse = False
        while gotResponse == False:
            try:
                response = openai.ChatCompletion.create(
                    model = modelName,
                    messages = [
                        {"role": "user", "content": prompts[i]}
                    ]
                )
                gotResponse = True
            except Exception as e:
                print("Exception on request " + str(i + 1) + ": " + str(e))
                time.sleep(10)
        
        # Extract entire message content
        message = response['choices'][0]['message']['content']
        
        # Take only the first word of the response
        tokens = message.split()
        if tokens[0] == "the" and len(tokens) == 2: # Make an exception for 'the _____'
            extraction = tokens[1]
        else:
            extraction = tokens[0]
            
        # Remove whitespace, punctuation, and capitalization
        extraction = extraction.strip()
        extraction = extraction.strip(".")
        extraction = extraction.lower()
        
        completions[i] = extraction
        
        # Sleep briefly to avoid being booted during requesting
        print("Completed request " + str(i + 1))
        time.sleep(1)
        
    # Output completions to csv
    with open(writeTo, "w") as file:
        file.write(heading + "\n")
        for line in completions:
            file.write(line + "\n")
        