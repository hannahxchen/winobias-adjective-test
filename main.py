# This file just served as a place for me to write down all my commands without having to go through them one by one with the command line
# Whenever I was done with the previous commands and ready for the next ones, I would delete what was there and rewrite
# So what's left is what was last


import prompt
import completion
import data


adjList = ["pro_base", "anti_base",
        "pro_arrog-respo", "anti_arrog-respo",
        "pro_brill-busy", "anti_brill-busy",
        "pro_dry-bubbl", "anti_dry-bubbl",
        "pro_funny-stric", "anti_funny-stric",
        "pro_hard-soft", "anti_hard-soft",
        "pro_intel-sweet", "anti_intel-sweet",
        "pro_knowl-helpf", "anti_knowl-helpf",
        "pro_large-littl", "anti_large-littl",
        "pro_nothi-blond", "anti_nothi-blond",
        "pro_nothi-mean", "anti_nothi-mean",
        "pro_old-nothi", "anti_old-nothi",
        "pro_organ-disor", "anti_organ-disor",
        "pro_polit-nothi", "anti_polit-nothi",
        "pro_pract-pleas", "anti_pract-pleas",
        "pro_tough-under", "anti_tough-under"
    ]
prompts = [None] * 32
completions = [None] * 32
headings = [None] * 32


def run(trialNum):
    print("Running...")
    
    readAdj(trialNum)
    runCompletions()
    runStats(trialNum)
    runHeatMap(trialNum)
    
    print("Done!")
    
    
def readAdj(trialNum):
    for i in range( len(adjList) ):
        prompts[i] = "prompts\\promp_type1_" + adjList[i] + ".txt.test"
        completions[i] = "completions\\trial" + str(trialNum) + "\\compl_tri" + str(trialNum) + "_type1_" + adjList[i] + ".txt.test"
        
        tokens = adjList[i].split("_")
        headings[i] = "I"
        for j in range( len(tokens) ):
            headings[i] += " " + tokens[j].title() # title() is used over capitalize() so that the letter after the hyphen is also uppercase
    

def runPrompts():
    # prompt.makeFile("[Read From]", "[Write To]", "[Adj 1]", "[Adj 2]", 395)
    print()


def runCompletions():
    modelName = "gpt-3.5-turbo"
    numRows = 395
        
    for i in range( len(prompts) ):
        completion.getCompletionsOf(prompts[i], completions[i], modelName, headings[i], numRows)
        printSeparator("Completed File " + str(i + 1))


def runStats(trialNum):
    for i in range( len(completions) ):
        completions[i] = completions[i]
    
    data.makeStatsFile("answers\\coranswers.txt.test", "answers\\incanswers.txt.test", completions, "output\\output_data_tri" + str(trialNum) + ".csv", 395)
    
 
def runHeatMap(trialNum):
    data.makeHeatMap("answers\\coranswers.txt.test", "answers\\incanswers.txt.test", "output\\output_data_tri" + str(trialNum) + ".csv",
        "output\\output_heat_tri" + str(trialNum) + ".csv", 395, 32)
    
    
    
def printSeparator(message):
    print("\n\n")
    print("------------------------------")
    print("******************************")
    print(message)
    print("------------------------------")
    print("******************************")
    print("\n\n")