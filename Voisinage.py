import copy

def voisins(s):
    voisins = []
    subvoisins = []
    interINIT = copy.deepcopy(s)
    for i in range(len(s)):
        for j in range(len(s)):
            inter = interINIT[i]
            interINIT[i] = interINIT[j]
            interINIT[j] = inter
            subvoisins.append(interINIT)
            interINIT = copy.deepcopy(s)
        voisins.append(subvoisins)
        subvoisins = []
    return voisins
