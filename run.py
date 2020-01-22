import random
import math
import time

# # Read file
file = open('On.dimacs', 'r' )
writeFile = open('On.txt', 'w')
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


#============================================================================================================

# Tabu Search
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
    count = 0
    for clause in clauses:  
        for x in clause:
            if clause[x] is True:
                clauseResult[clauses.index(clause) + 1] = True
                count += 1               
                break  
    return count

def isModelSatisfying(number):
    if number < numClauses:    
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
def createFlagList(falseItem):
    flagList = []
    for clause in falseItem:
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
    maxKey = 0
    maxValue = 0
    flagList = createFlagList(check())
    falseFlipResults = [] #list of Flip Results
    positions = [] # list of keys
    for item in flagList:
        if item not in taboo:
            model[item] = not model[item]
            modelizeClauses()
            temp = countTrueClauses()
            falseFlipResults.append(temp)
            positions.append(item)
            model[item] = not model[item]
            modelizeClauses()
            if temp == numClauses:
                break
    maxValue = max(falseFlipResults)
    maxKey = falseFlipResults.index(maxValue)
    item = positions[maxKey]
    model[item] = not model[item]
    addToTabooList(item)
    return model


# With probability 0.5 randomFlipper1 or randomFlipper2 
def randomWalk():
    prob = random.random() 
    if prob < 0.5:
        randomFlipperOne()
    else:
        randomFlipperTwo()
        

def walkSAT(maxFlips):
    maxCounter = 0 # find the best solution if walkSAT fails to satisfy
    optimizedModel = model # Store the best solution if walkSAT fails to satisfy
    counter = 0
    while counter < maxFlips and int(time.perf_counter() - start) <= 10:
        modelizeClauses()
        temp = countTrueClauses()
        check = isModelSatisfying(temp) 
        if check:
            print('All Clauses Satisfied!')
            writeFile.write('Solved!!! Satisfying model: ' + str(model))
            return model
        randomWalk()
        setClauseResultToFalse() #initialize clauseResult list
        if temp > maxCounter:
            maxCounter = temp
            optimizedModel = model
        counter = counter + 1
        print('Fliped Times: ', counter)
        print('clauses Satisfied: ', temp)
    writeFile.write('Failure to satisfy all clauses. Clauses Satisfied: ' + str(maxCounter) + '! Best Solution found:' + str(optimizedModel))
    return model

try:
    walkSAT(1000000)
    finish = time.perf_counter()
    print('It took ', str(finish-start), ' seconds')
except:
    print('Something interrupted the execution')