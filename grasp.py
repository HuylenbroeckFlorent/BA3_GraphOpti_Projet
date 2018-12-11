from math import *
import copy
from Voisinage import voisins
Taille = 0
D = []
F = []
VoisinageG = []
Solution = []
CoutOpti = inf

def init():
    file = input("Fichier à tester (sans le .dat): ")
    with open("../instances/"+file+".dat",'r') as f:
        Taille = int(f.readline().split()[0])
        i = 0
        f.readline()
        for ligne in f.readlines():
            if i<Taille:
                if ligne[0]!='\n':
                    D.append([int(i) for i in ligne.split()])
                i+=1
            else:
                if ligne[0]!='\n':
                    F.append([int(i) for i in ligne.split()])
                i+=1
        INIT = []
        for i in range(Taille):
            INIT.append(i+1)
        VoisinageG = voisins(INIT)
        print(len(VoisinageG))
        for ligne in VoisinageG:
            print(ligne)

#def cout(s):


def calculer_proba(alpha,s,elements):
    RESTE = []
    for i in s:
        if not(i in elements):
            RESTE.append(i)
    prob = []
    #min = min{coût(s U {e}| e € RESTE)}
    #max = max{coût(s U {e}| e € RESTE)}
    #RCL = {e € RESTE, min<=coût(s U {e})<=min+alpha*(max-min)}
    for e in RESTE:
        if e in RCL:
            prob[e] = 1/(len(RCL))
        else:
            prob[e] = 0
    return prob

def glouton_proba(alpha):
    e = initialiser(elements)
    s = e[:]
    while incomplet(s):
        prob = calculer_proba(alpha,s,elements)
        e = select_proba(prob,s,elements)
        for i in e:
            if not (i in s):
                s.append(i)
    return s

if __name__ == '__main__':
    init()
