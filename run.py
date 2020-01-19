import random
import math
import time

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
taboo = [0 for i in range(0, int(numVar/10))] # List to use in taboo search
print(len(taboo))

# Track True and False clauses in clauses[]
clauseResult = {x: False for x in range(1, numClauses + 1)}

# Taboo Search
def addToTabooList(key):
    taboo.pop(0)
    taboo.append(key)
    return taboo

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
def countTrueClauses():
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
    return count

def isModelSatisfying(number):
    count = number
    if count <= numClauses:    
        return False
    return True

# Setting clauseResult{} values to false
def setClauseResultToFalse():
    for i in clauseResult:
        if clauseResult[i] == True:
            clauseResult[i] = False
    return clauseResult

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


def randomFlipperOne():
    randChoise = random.choice(check())
    randkey = abs(random.choice(list(randChoise.keys())))
    if(randkey not in taboo):
        model[randkey] = not model[randkey]
        addToTabooList(randkey)
    else:
        randomFlipperOne()
    return model

def randomFlipperTwo():
    minKey = 0
    minValue = None
    flagList = createFlagList(check())
    for item in flagList:
        if item not in taboo:
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
        addToTabooList(minKey)
    return model

# With probability 0.5 randomFlipper1 or randomFlipper2 
def randomizer():
    prob = random.random() 
    setClauseResultToFalse()
    if prob < 0.5:
        randomFlipperOne()
    else:
        randomFlipperTwo()
        

def walksat(maxFlips):
    maxCounter = 0 # find the best solution if walkSAT fails to satisfy
    optimizedModel = model # Store the best solution if walkSAT fails to satisfy
    counter = 0
    while counter < maxFlips and int(time.perf_counter() - start) <= 10:
        temp = countTrueClauses()
        check = isModelSatisfying(temp) 
        if check:
            writeFile.write('Solved!!! Satisfying model: ' + str(model))
            return model
        randomizer()
        if temp > maxCounter:
            maxCounter = temp
            optimizedModel = model
        counter = counter + 1
        print('Fliped Times: ', counter)
    writeFile.write('Failure to satisfy all clauses. Clauses Satisfied: ' + str(maxCounter) + '! Best Solution found:' + str(optimizedModel))
    return model
        

try:
    walksat(1000000)
    finish = time.perf_counter()
    print('It took ', str(finish-start), ' seconds')
except:
    print('Something interrupted the execution')
