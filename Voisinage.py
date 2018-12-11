import copy

def voisins(s):
    voisins = []
    interINIT = copy.deepcopy(s)
    for i in range(len(s)):
        for j in range(i+1,len(s)):
            inter = interINIT[i]
            interINIT[i] = interINIT[j]
            interINIT[j] = inter
            voisins.append(interINIT)
            interINIT = copy.deepcopy(s)
    return voisins
