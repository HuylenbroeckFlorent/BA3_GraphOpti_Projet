import copy

def swapij(tab,i,j):
    tmp=tab[i]
    tab[i]=tab[j]
    tab[j]=tmp
    return tab

def getNeighborhood(perm):
    neighborhood=[]
    for i in range(len(perm)-1):
        for j in range(i+1,len(perm)):
            tmpPerm=copy.deepcopy(perm)
            tmpPerm=swapij(tmpPerm,i,j)
            neighborhood.append(tmpPerm)
    return neighborhood
            

print(getNeighborhood([1,2,3,4]))
    