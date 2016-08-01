import numpy as np

##########################################################
# INPUT description:
# Your algorithms receive 4 inputs:
# I <- an initial feasible basis
# c <- a numpy array that you will use as your objective function
# A,b <- a matrix and vector describing the constraint
#
#      A.dot(x) = b
#
# OUTPUT description:
# You algorithms should return two things:
# 1. the value of the optimal solution v.
#     - Assuming an optimal solution x, get this with c.dot(x).
#     - Alternatively, you can use c[I].dot(xI), where xI
#       is the vector obtained from the optimal basis.
# 2. an optimal solution x
#     - This should be in the form of a numpy array.
#     - Assuming an optimal basis I and associated
#       inverse of A restricted to index set I, called AI,
#       you can construct it with:
#
#       x = np.zeros(c.shape[0])
#       x[I] = AI.dot(b)
#
# return them with the statement: return (v, x)
##########################################################

##########################################################
# Implement any simplex algorithm here.
# You are free to write a dual and/or revised simplex
# implementation and call it here. It may be easier to
# write up the simpler standard simplex algorithm first,
# since you can reuse a lot of its code for the revised
# simplex algorithm anyway. It will also be useful as a
# reference.
##########################################################
def simplex(I, c, A, b):
    return recursiveSimplex(I, c, A, b)
    # write your implementation here
def recursiveSimplex(I, c, A, b):
    j = []; AI = []; xI = []; cI_T = []; aj = []; AI_aj = []; x_ret = np.zeros(c.shape)
    for i in range(0, len(A[0])):
        if i not in I:
            j.append(i)
    AI = np.linalg.inv(A[:,I])
    xI = AI.dot(b)
    cI_T = c[I].transpose()
    aj = A[:,j]
    xi_star = AI.dot(aj)
    cj = c[j]
    cj_ = cj - cI_T.dot(xi_star)
    if all(i >= 0 for i in cj_):
        x_ret[I] = xI
        return c.transpose().dot(x_ret), x_ret
    else:
        min_j = j[np.argmin(cj_)]
        aj_new = A[:,min_j]
        dI =  -1 * AI.dot(aj_new)
        xI_by_dI = []
        for k in range(0, len(dI)):
            if dI[k] < -1*pow(10,-12):
                xI_by_dI.append(-xI[k]/dI[k])
            else:
                xI_by_dI.append(pow(10,12))
        i_star = I[np.argmin(xI_by_dI)]
        I[I == i_star] = [min_j]
        return recursiveSimplex(I, c, A, b)

##########################################################
# Implement a simplex algorithm with incremental
# A inverse computation here.
# You are free to write a dual simplex with incremental
# matrix inversion and call it here.
# In addition to output correctness, this algorithm
# will also be tested for speed. In our reference
# implementation, the speedup was a factor of 10-20
# for most instances.
##########################################################
def revised_simplex(I, c, A, b):
    AI = None
    return recursive_revised_simplex(I, c, A, b, AI)
def recursive_revised_simplex(I, c, A, b, AI):
    j = []; xI = []; cI_T = []; aj = []; AI_aj = []; x_ret = np.zeros(c.shape)
    ek = np.zeros(I.shape)
    for i in range(0, len(A[0])):
        if i not in I:
            j.append(i)
    if AI is None:
        AI = np.linalg.inv(A[:,I])
    xI = AI.dot(b)
    cI_T = c[I].transpose()
    aj = A[:,j]
    xi_star = AI.dot(aj)
    cj = c[j]
    cj_ = cj - cI_T.dot(xi_star)
    if all(i >= 0 for i in cj_):
        x_ret[I] = xI
        return c.transpose().dot(x_ret), x_ret
    else:
        k = j[np.argmin(cj_)]
        aj_new = A[:,k]
        dI =  -1 * AI.dot(aj_new)
        xI_by_dI = []
        for a in range(0, len(dI)):
            if dI[a] < -1*pow(10,-12):
                xI_by_dI.append(-xI[a]/dI[a])
            else:
                xI_by_dI.append(pow(10,12))
        i_star = I[np.argmin(xI_by_dI)]
        aik = A[:,i_star]
        aik = np.reshape(aik,(aik.shape[0], 1))
        aj_new = np.reshape(aj_new, (aj_new.shape[0],1))
        I[I == i_star] = [k]
        ek[np.argmin(xI_by_dI)] = 1
        ek = np.reshape(ek,(ek.shape[0], 1))
        ek_AI = ek.transpose().dot(AI)
        aj_aik = (aj_new - aik).dot(ek_AI)
        AI = AI - (AI.dot(aj_aik))/(1+ek_AI.dot(aj_new-aik))
    return recursive_revised_simplex(I, c, A, b, AI)

##########################################################
# Implement the dual simplex algorithm.
##########################################################
def dual_simplex(I, c, A, b):
    bp = np.zeros(b.shape[0])
    for n in range (0, b.shape[0]):
        bp[n] = pow(10,-13)
    b = b + bp

    #print "hellloooo",b
    ## Initialise Variables
    j = []; x_ret = np.zeros(c.shape[0]); xI = np.zeros(A.shape[0])

    ## get I complement
    for i in range(0, len(A[0])):
        if i not in I:
            j.append(i)

    ## AI, AI Transpose, and A Transpose
    AI = np.linalg.inv(A[:,I])
    AT = np.transpose(A[:,I])
    AI_T = np.linalg.inv(AT)

    ## Calculate yI = -AI_T * cI
    cI = c[I]
    yI = -AI_T.dot(cI)

    ## Calculate xI = AI * b
    xI = AI.dot(b)
    if (xI > 0).all():
        x_ret[I] = xI
        return c.transpose().dot(x_ret), x_ret

    Ik_list =[]
    for buf in range(0, xI.shape[0]):
        if xI[buf] <= 0:
            Ik_list.append(buf)

    ## get Ik
    Ik_list = np.where(xI <= 0)[0]

    ## Get any index of xI where the value xI <= 0
    Ik = Ik_list[0]

    ## First, get cj-bar
    cI_T = np.transpose(c[I])
    aj = A
    cj = c
    cj_ = cj - np.dot(cI_T, np.dot(AI, aj))

    ## get the min_j value that needs to be added to I
    ## first compute cjBar/vI
    ## Calculate vI = AT * AI_T[:,Ik]
    vI = AT.dot(AI_T[:,Ik])
    if (vI>=0).all():
        return (float("inf"), np.zeros(c.shape[0]))
    cjBar_by_vI = np.zeros(vI.shape)
    for k in range(0, vI.shape[0]):
        if (vI[k] < -1*pow(10,-12)):
            cjBar_by_vI[k] = -cj_[k]/vI[k]
        else:
            cjBar_by_vI[k] = pow(10,15)
    ## get the min_j
    min_j = [np.argmin(cjBar_by_vI)]
    ## Update I = I - {Ik} U {min_j}
    I = I[I != I[Ik]]
    I = np.sort(np.append(I, min_j))
    return c.transpose().dot(x_ret), x_ret

##########################################################
# Implement a method that add the new constraint g.T.dot(x) <= h
# to the existing system of equations
#
#    A.dot(x)=b.
#
# Then use dual simplex to solve this problem. You can assume
# that I is an index set which will yield a dual-feasible basis.
#
# OUTPUT description:
# You algorithms should return two things:
# 1. the value of the optimal solution v (for the new problem).
#     - Assuming an optimal solution x, get this with c.dot(x).
#     - Alternatively, you can use c[I].dot(xI), where xI
#       is the vector obtained from the optimal basis.
# 2. an optimal solution x (for the new problem).
#     - This should be in the form of a numpy array.
#     - Assuming an optimal basis I and associated
#       inverse of A called AI, you can construct
#       it with:
#       x = np.zeros(c.shape[0])
#       x[I] = AI.dot(b)
#
# return them with the statement: return (v, x)
##########################################################
def add_constraint(I,c,A,b,g,h):
    #A = np.c_[ A, np.zeros(len(A)) ]
    A = np.vstack([A, g])
    #print b.shape
    #print b
    #print h.shape
    #print h

    temp = np.zeros((A.shape[0]-1,1))
    #print temp.shape
    temp = np.vstack([temp,1])
    #print temp.shape
    A = np.hstack([A,temp])
    #g = np.append(g,1)
    #A = np.r_[A, [g]]
    c = np.append(c,0)
    b = np.append(b,h)
   # print "latest---------",b.shape
    I = np.append(I,A.shape[1]-1)
    return dual_simplex(I, c, A, b)