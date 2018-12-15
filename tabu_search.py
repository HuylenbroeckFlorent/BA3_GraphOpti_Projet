#Le tabac c'est tabou on en viendra tous a bout
import random
import copy
import sys
sys.path.append('../util')
from util import read_QAP, swap_by_indexes

#For debug only
def printMatrix(M):
    for i in range(len(M)):
        for j in range(len(M[i])):
            print(M[i][j], end=' ')
        print("")    

#For debug only
def minusOneAll(p):
    for i in range(len(p)):
        p[i]=p[i]-1

def swapij(tab,i,j):
    tmp=tab[i]
    tab[i]=tab[j]
    tab[j]=tmp
    return tab

def appendIfNotIncluded(elem,tab):
    if not elem in tab:
        tab.append(elem)
        
#i beeing the indice of the next cell to be overwritten        
def fifoIfNotIncluded(elem,tab,i):
    if not elem in tab:
        tab[i]=elem

#neighborhood is the list of the neighbor around perm
#directions[q] is the [i,j] permutation needed to go from perm to neighborhood[q]
def getNeighborhood(perm):
    neighborhood=[]
    directions=[]
    for i in range(len(perm)-1):
        for j in range(i+1,len(perm)):
            tmpPerm=copy.deepcopy(perm)
            tmpPerm=swapij(tmpPerm,i,j)
            neighborhood.append(tmpPerm)
            directions.append([i,j])
    return neighborhood,directions

#Return the objectif value of the specific perm.
#/!\considering perm start counting at 1 (and not at 0): [2,0,1] is a valid perm, [3,1,2] isn't
def permValue(perm,F,D):
    sum=0
    for i in range(len(perm)):
        for j in range(len(perm)):
            sum=sum+F[perm[i]][perm[j]]*D[i][j]
    return sum

#If numberOfPacks=-1, then turn until not upgraded
#See tabuSearch for more details
def tabuMovementSearch(F,D,initialPerm=-1,iterBeforeCheck=-1,tabuListSize=-1,numberOfPacks=-1):
    if(iterBeforeCheck==-1):
        iterBeforeCheck=len(F)
    if(initialPerm==-1):
        initialPerm=[]
        for i in range(len(F[0])):
            initialPerm.append(i)
        random.shuffle(initialPerm)
    bestPerm,bestValue=initialPerm,permValue(initialPerm,F,D)
    if(tabuListSize!=-1):
        ind=0
        tabuList=a=[-1]*tabuListSize
    else:
        tabuList=[]       #The list of the tabu directions
        
    current=initialPerm
    uppgraded=True
    while(uppgraded and numberOfPacks!=0):
        numberOfPacks-=1
        uppgraded=False
        #print("Let's go for another pack")
        for Q in range(iterBeforeCheck):
            neighborhood,directions=getNeighborhood(current)
            bnValue=float('inf')   #+inf sentinel
            for i in range(len(neighborhood)):
                neighborValue=permValue(neighborhood[i],F,D)
                if(neighborValue<bnValue):
                    if((directions[i] in tabuList) or ([directions[i][1],directions[i][0]] in tabuList)):     #[i,j] is the same direction as [j,i]
                        if(neighborValue<bestValue):    #If best ever since, let's just ignore tabu
                            bn,bnValue,directionTObn=neighborhood[i],neighborValue,directions[i]
                    else:
                        bn,bnValue,directionTObn=neighborhood[i],neighborValue,directions[i]
            if(bnValue<bestValue):
                bestPerm,bestValue=bn,bnValue        
                uppgraded=True
            if(tabuListSize==-1):
                appendIfNotIncluded(directionTObn,tabuList)
            else:
                fifoIfNotIncluded(directionTObn,tabuList,ind)
                ind=(ind+1)%tabuListSize
                
            current=bn
            print("Current: ",bnValue, "       Best: ",bestPerm,bestValue)
    #
    return bestPerm

#tabuListSize will be divided by two every [iterBeforeCheck] iterations
#See tabuSearch for more details
def tabuPermSearch(F,D,initialPerm=-1,iterBeforeCheck=-1,tabuListSize=-1,numberOfPacks=-1):
    if(iterBeforeCheck==-1):
        iterBeforeCheck=len(F)
    if(initialPerm==-1):
        initialPerm=[]
        for i in range(len(F[0])):
            initialPerm.append(i)
        random.shuffle(initialPerm)
    bestPerm,bestValue=initialPerm,permValue(initialPerm,F,D)
    if(tabuListSize!=-1):
        ind=0
        tabuList=[-1]*tabuListSize
    else:
        tabuList=[]       #The list of the tabu directions
        
    current=initialPerm
    uppgraded=True
    while(uppgraded and numberOfPacks!=0):
        numberOfPacks-=1
        uppgraded=False
        #print("Let's go for another pack")
        for Q in range(iterBeforeCheck):
            neighborhood,directions=getNeighborhood(current)
            bnValue=float('inf')   #+inf sentinel
            for i in range(len(neighborhood)):
                neighborValue=permValue(neighborhood[i],F,D)
                if(neighborValue<bnValue):
                    if(neighborhood[i] in tabuList):
                        if(neighborValue<bestValue):    #If best ever since, let's just ignore tabu
                            bn,bnValue,directionTObn=neighborhood[i],neighborValue,directions[i]
                    else:
                        bn,bnValue,directionTObn=neighborhood[i],neighborValue,directions[i]
            if(bnValue<bestValue):
                bestPerm,bestValue=bn,bnValue        
                uppgraded=True
            if(tabuListSize==-1):
                appendIfNotIncluded(bn,tabuList)
            else:
                fifoIfNotIncluded(bn,tabuList,ind)
                ind=(ind+1)%tabuListSize
            current=bn
            print("Current: ",bnValue, "       Best: ",bestPerm,bestValue)
        if(tabuListSize!=-1):
            tabuListSize=max(4,tabuListSize//2) #the size of the tabuList never goes below 4
            tabuList=tabuList[(len(tabuList)-tabuListSize):]
            ind=0
    #
    return bestPerm

#Launch a tabu search starting at the permutation "initialPerm". If initialPerm=-1, then start at a random permutation
#Start with [movesPackSwitch] times [iterBeforeCheck] iterations with the movements as tabu
#Then go on with [tabuPermPacks] times [iterBeforeCheck] iterations with the permutation as tabu, until we can't finda better solutoin (checked every [iterBeforeCheck] iterations)
#If tabuPermPacks = -1, then there is no maximums number of iterations in the tabu permutation search and we go on until we don't find a better permutation after [iterBeforeCheck] iterations
#If tabuListSize = -1, then there is no limitation of the tabu list size.
#The defaults value are for a not so long computation time, so it can be used for every ant in the ants algorithm
def tabuSearch(F,D,initialPerm=-1,iterBeforeCheck=-1,tabuListSize=-2,movesPackSwitch=1,tabuPermPacks=2):
    if(tabuListSize==-2):
        tabuListSize=len(F)+5
    bestPerm=tabuMovementSearch(F,D,initialPerm,iterBeforeCheck,tabuListSize,movesPackSwitch)
    #print("Switching from tabu movements to tabu permutations")
    bestPerm=tabuPermSearch(F,D,bestPerm,iterBeforeCheck,tabuListSize,tabuPermPacks)
    return bestPerm

    

 
size,D,F=read_QAP("nug30.dat")     


#perm=tabuSearch(F,D,[POINT DE DEPART DE LA FOURMI])
perm=tabuSearch(F,D)                  #RELATIVLY QUICK, seems good for ants
#perm=tabuSearch(F,D,-1,100,75,2,-1)     #LONGER (but better)
#perm=tabuSearch(F,D,-1,10,15,1)      #VERY QUICK


print(perm)
print(permValue(perm,F,D))