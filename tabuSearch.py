#Le tabac c'est tabou on en viendra tous à bout
import random
import copy

def swapij(tab,i,j):
    tmp=tab[i]
    tab[i]=tab[j]
    tab[j]=tmp
    return tab

def appendIfNotIncluded(elem,tab):
    if not elem in tab:
        tab.append(elem)

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
            sum=sum+F[i][j]*D[perm[i]][perm[j]]
    return sum

def tabuSearch(F,D,initialPerm=-1):
    if(initialPerm==-1):
        initialPerm=[]
        for i in range(len(F[0])):
            initialPerm.append(i)
        random.shuffle(initialPerm)
    bestPerm,bestValue=initialPerm,permValue(initialPerm,F,D)
    
    tabuList=[]       #The list of the tabu directions
    #print("OK LA JE SUIS EN : ",initialPerm,bestValue)
    current=initialPerm
    for Q in range(5):
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
        appendIfNotIncluded(directionTObn,tabuList)
        current=bn
        #print("OK LA JE SUIS EN : ",current,bnValue)
    #
    return bestPerm
    
            
        
    
            
    
    
def printMatrix(M):
    #print("Matrix")
    for i in range(len(M)):
        for j in range(len(M[i])):
            print(M[i][j], end=' ')
        print("")    

F=[[0,10,5],[5,0,15],[2,20,0]]
D=[[0,20,40],[20,0,50],[40,50,0]]
perm=[1,2,0]

print("PERM:",[2,1,0])
#print(permValue(perm,F,D))
oo=tabuSearch(F,D,perm)
print("...............",oo,permValue(oo,F,D))
#print(permValue(oo,F,D))

print("--------")
voisins,osef=getNeighborhood([2,1,0])
for v in voisins:
    print(v,osef,permValue(v,F,D))