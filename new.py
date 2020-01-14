import random
import math
import time
import concurrent.futures

# # Read file
file = open('two.dimacs', 'r' )
writeFile = open('two.txt', 'w')
start = time.perf_counter()
## Parsing file
# ========================================
line = file.readline().strip().split(' ')
# skip comments
while line[0] == 'c':
    line = file.readline().strip().split(' ')

# getting number of variables
numVar = int(line[2])
# getting number of clauses
numClauses = int(line[3])

# create a symbols list for each variable
symbols = [x for x in range(1, numVar + 1)]

# =================================================
# Creating a list of dictionaries for all clauses
clauses = []
for i in range(0, numClauses):
    clauseline = file.readline().strip().split(' ')[:-1]
    clause = {int(x): True for x in clauseline}
    clauses.append(clause)

# assign random boolean values in model
model =  {x: random.choice([True, False]) for x in symbols}

# Track True and False clauses in clauses[]
clauseResult = {x: False for x in range(1, numClauses + 1)}
print('Finished Parshing File! Executing phase 2...')
# add model values to clauses
def modelizeClauses():
    for clause in clauses:
        for key in clause:
            if key > 0:
                clause[key] = model[key]
            else:
                clause[key] = not model[abs(key)]                   
    return clauses

# modelizeClauses() and check if model satisfies clauses
def isModelSatisfying():
    count = 1
    clauses = modelizeClauses()
    for clause in clauses:  
        for x in clause:
            if clause[x] == True:
                for y in clauseResult:
                    if y == clauses.index(clause) + 1:
                        clauseResult[y] = True  
                        count += 1               
                break  
    print('Satisfied: ', count,'/',numClauses,' clauses')
    if count <= numClauses:    
        return False
    return True

# Setting clauseResult{} values to false
def setClauseResultToFalse():
    for i in clauseResult:
        if clauseResult[i] == True:
            clauseResult[i] = False

# Check clauseResult for false clauses
def check():
    falseItem = []
    for i in clauseResult:
        if clauseResult[i] == False:
            falseItem.append(clauses[i - 1])
    return falseItem

#Put false clauses into 'flagList' list
def createFlagList(falseClausesResult):
    flagList = []
    for clause in falseClausesResult:
        for key in clause:
            flagList.append(abs(key))
    return flagList   

# With probability 0.5 flip random var or best var
def randomizer():
    prob = random.random() 
    falseClausesResult = check() 
    setClauseResultToFalse()
    if prob <= 0.3:
        randChoise = random.choice(falseClausesResult)
        randkey = abs(random.choice(list(randChoise.keys())))
        model[randkey] = not model[randkey]
        return model
    else:
        minKey = 0
        minValue = None
        flagList = createFlagList(falseClausesResult)
        for item in flagList:
            model[item] = not model[item]
            modelizeClauses()
            falseFlipResults = check()
            if minValue is None:
                minKey = item                       #Best variable
                minValue = len(falseFlipResults)    #Best variable position
            elif minValue > len(falseFlipResults):
                minKey = item
                minValue = len(falseFlipResults)
            model[item] = not model[item]
        if minKey != 0:
            model[minKey] = not model[minKey]
        return model
        
maxFlips = 10
def walksat(maxFlips):
    counter = 0
    for i in range(0, maxFlips): 
        check = isModelSatisfying() 
        if check:
            writeFile.write('Satisfying model: ' + str(model) + ': Performed ' + str(i) + ' flips! ')
            return model
            break
        randomizer()
        counter = counter + 1
        print('Fliped Times: ', counter)
        if counter == maxFlips:
            writeFile.write('Failure to satisfy all clauses. Performed ' + str(maxFlips) + ' flips! ')
            return 'failure'

walksat(10)
    


finish = time.perf_counter()
print('It took ', str(finish-start), ' seconds')
