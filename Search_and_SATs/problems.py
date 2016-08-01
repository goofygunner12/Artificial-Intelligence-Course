import operator as op
import math

numvar=2
formula=[[],[]]#[[(0, 0)],[(1,0),(1,1)]]# (0, 1), (0, 2)],
##         [(0,3)],
##         [(0, 0), (0, 1), (1, 2)],
##         [(0, 5), (0, 6), (0, 7)],
##         [(0, 5), (0, 6), (1, 7)]]

################################################################################
# Check if a given partial assignment is consistent with the cnf
# Input: formula is a CNF encoded as described in the problem set.
#        ass is a dictionary of assignments.
# Output: Whether there is a clause that is false in the formula.
################################################################################
def check(formula, ass):
    if not formula:
        retBool = True
    else:
        variableAssignmentList = []
        bitwiseOperationList = []
        for everyClause in formula:
            clauseList = []
            if not everyClause:
                literalAssignment = 0
                clauseList.append(literalAssignment) 
            else:
                for everyLiteral in everyClause:
                    literalIndex = (everyLiteral[-1])
                    literalAssignment = ass.get((literalIndex), '?')
                    if(everyLiteral[0] != 0 and literalAssignment != '?'):
                        if(literalAssignment == 0):
                            literalAssignment = 1
                        elif(literalAssignment == 1):
                            literalAssignment = 0
                    elif(literalAssignment == '?'):
                        literalAssignment = 1
                    clauseList.append(literalAssignment)
            variableAssignmentList.append(clauseList[:])
        for everyAssignment in variableAssignmentList:
            clauseOperationValue = reduce(op.ior, everyAssignment)
            bitwiseOperationList.append(clauseOperationValue)
        retBool = bool(reduce(op.iand, bitwiseOperationList))
    return retBool
################################################################################
# Simple Sat Problem Solver
# Input: n is the number of variables (numbered 0, ..., n-1).
#        formula is CNF
# Output: An assignment that satisfies the formula
#         A count of how many variable assignments were tried
################################################################################
def simpleSolver(n, formula):
    initAssignment = {}
    return backtrackingSearch(n, formula, initAssignment)

def backtrackingSearch(n, formula, assignment):
    updateAssignment = {}
    updateAssignment.update(assignment)
    if check(formula, updateAssignment):
        if len(updateAssignment.keys()) == n:
            return updateAssignment, 0
        else:
            lieralIndex = len(updateAssignment.keys())
            updateAssignment[lieralIndex] = 0
            (newAssignment, totalZeroAssignmentsMade) = backtrackingSearch(n, formula, updateAssignment)
            if newAssignment is not False:
                return newAssignment, totalZeroAssignmentsMade+1
            else:
                updateAssignment[lieralIndex] = 1
                (newAssignment, totalOneAssignmentsMade) = backtrackingSearch(n, formula, updateAssignment)
                return newAssignment, totalZeroAssignmentsMade+totalOneAssignmentsMade+2
    else:
        return False, 0

################################################################################
# Simple Sat Problem Solver with unit propagation
# Input: n is the number of variables (numbered 0, ..., n-1).
#        formula is CNF
# Output: An assignment that satisfies the formula
#         A count of how many variable assignments were tried
################################################################################
def unitSolver(n, formula):
    totalAssignmentsMade = 0
    totalPossibleAssignment = 0
    bcpAssignment = {}
    btAssignment = {}
    tempAssignment = {}
    count = 0
    for i in range(0,n):
        totalPossibleAssignment = totalPossibleAssignment + math.pow(2,i+1)
    if n > 0:
        while(totalAssignmentsMade <= totalPossibleAssignment): 
            bcpAssignment = checkSingletonClause(formula, bcpAssignment)
            retValue = check( formula, bcpAssignment)
           # print "hello", bcpAssignment, retValue
            if(retValue is True):
                btAssignment.update(bcpAssignment)
                if len(btAssignment) == n:
                    return btAssignment,totalAssignmentsMade
                elif len(btAssignment) == 0:
                    btAssignment[0] = 0
                    tempAssignment[0] = 0
                    totalAssignmentsMade = totalAssignmentsMade + 1
                elif len(btAssignment) == btAssignment.keys()[-1]+1 and btAssignment.keys()[-1]!=0:
                    index = len(btAssignment)
                    btAssignment[index] = 0
                    tempAssignment[index] = 0
                    totalAssignmentsMade = totalAssignmentsMade + 1
                else:
                    if not tempAssignment:
                        btAssignment[0] = 0
                        tempAssignment[0] = 0
                        totalAssignmentsMade = totalAssignmentsMade + 1
                    else:
                        litIndex = tempAssignment.keys()[-1]+1
                        litAssignment = btAssignment.get(litIndex, 2)
                        if litAssignment == 2:
                            tempAssignment[litIndex]=0
                            btAssignment[litIndex]=0
                            totalAssignmentsMade = totalAssignmentsMade + 1
                        else:
                            tempAssignment[litIndex]=litAssignment                  
                
                
            elif(retValue is False):
                if len(btAssignment) == n:
                    return False,0
                elif tempAssignment:
                   # print "false ret", btAssignment
                   # print tempAssignment
                    litIndex = tempAssignment.keys()[-1]+1
                    litAssignment = btAssignment.get(litIndex, 2)
##                    if litAssignment == 2:
##                        tempAssignment[litIndex]=0
##                        btAssignment[litIndex]=0
##                        totalAssignmentsMade = totalAssignmentsMade + 1
                    if tempAssignment[litIndex-1] == 1:
                        tempAssignment[litIndex-1]=0
                        btAssignment[litIndex-1]=0
                        totalAssignmentsMade = totalAssignmentsMade + 1
                    elif tempAssignment[litIndex-1] == 0:
                        tempAssignment[litIndex-1]=1
                        btAssignment[litIndex-1]=1
                        totalAssignmentsMade = totalAssignmentsMade + 1
                    #count = count+1
                    #if count > 15:
                    #    return
##                    index = len(btAssignment)-1
##                    btAssignment[index] = 1
##                    totalAssignmentsMade = totalAssignmentsMade + 1
                else:
                    return False,0
            bcpAssignment = btAssignment.copy()
           # print "ttt",bcpAssignment
           # print tempAssignment
           # print "-------------------"
    return btAssignment, totalAssignmentsMade

def checkSingletonClause(formula, bcpAssignment):
    restart = True
    bcpCount = 0
    #print "before", bcpAssignment
    while restart:
        restart = False
        flag = 0
        for everyClause in formula:            
            clauseList=[]
            clauseListResult=[]
            for everyLiteral in everyClause:
                if not everyLiteral:
                        literalAssignment = 0
                else:
                    literalIndex = (everyLiteral[-1])
                    literalAssignment = bcpAssignment.get((literalIndex), 2)
                    if(everyLiteral[0] != 0 and literalAssignment != 2):
                        if(literalAssignment == 0):
                            literalAssignment = 1
                        elif(literalAssignment == 1):
                            literalAssignment = 0                                     
                clauseListResult.append(literalAssignment)
                clauseList.append(everyLiteral)
                if len(everyClause) == 1 and 2 in clauseListResult:
                    for eachLiteral in clauseList:
                        litIndex = eachLiteral[-1]
                        litNegate = eachLiteral[0]
                        if litNegate == 1:
                            bcpAssignment[litIndex] = 0
                            bcpCount = bcpCount + 1
                        elif litNegate == 0:
                            bcpAssignment[litIndex] = 1
                            bcpCount = bcpCount + 1
                        flag = 1
                        restart = True
                        break
                    if flag==1:
                        break
            if 0 in clauseListResult and clauseListResult.count(2)== 1 and not 1 in clauseListResult :
                    for eachLiteral in clauseList:
                        if eachLiteral:
                            litIndex = eachLiteral[-1]
                            litNegate = eachLiteral[0]
                            litAssignment = bcpAssignment.get((litIndex), 2)
                            if litAssignment == 2:
                                if litNegate == 1:
                                    bcpAssignment[litIndex] = 0
                                    bcpCount = bcpCount + 1
                                elif litNegate == 0:
                                    bcpAssignment[litIndex] = 1
                                    bcpCount = bcpCount + 1
                                flag = 1
                                restart = True
                                break
            if flag == 1:
                break
                
    #print "after", bcpAssignment                      
    return bcpAssignment
################################################################################
# Clause Learning SAT Problem Solver                      
# Input: n is the number of variables (numbered 0, ..., n-1).
#        formula is CNF
# Output: An assignment that satisfies the formula
#         A count of how many variable assignments where tried
#         A list of all conflict-induced clauses that were found
################################################################################
def clauseLearningSolver(n, formula):
    return False, 0, []

################################################################################
# Conflict-directed backjumping with clause learning SAT Problem Solver                      
# Input: n is the number of variables (numbered 0, ..., n-1).
#        formula is CNF
# Output: An assignment that satisfies the formula
#         A count of how many variable assignments where tried
################################################################################
def backjumpSolver(n, formula):
    return False, 0, []

################################################################################

#print check(formula, assignment)
#print simpleSolver(numvar, formula)
print unitSolver(numvar, formula)
