from math import *
import copy
from Voisinage import voisins
import random

alphas = {0,10,20,30,40,50,60,70,80,90,100}
Taille = 0
D = []
F = []
VoisinageG = []
Solution = []
INIT = []
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
        for i in range(Taille):
            INIT.append(i)
        VoisinageG = voisins(INIT)

def cout(s):
    c = 0
    for i in range(len(s)):
        for j in range(len(s)):
            c+= D[i][j]*F[s[i]][s[j]]
    return c

def initialiser(elements):
    s = []
    s.append(random.randint(1,Taille))
    return s

def incomplet(s):
    return len(s)<Taille

def perm(s,alpha,min,max):
    return cout(s)<=(min + alpha*(max-min))

def rcl(s,elements,min,max,alpha):
    RCL = []
    sub = copy.copy(s)
    for e in elements :
        sub.append(e)
        if perm(sub,alpha,min,max):
            RCL.append(sub
        sub = copy.copy(s)
    return RCL

def Min_Max(s,elements):
    sub = copy.copy(s)
    max = 0
    min = math.inf
    for e in elements:
        sub.append(e)
        test = cout(sub)
        min = min(test,min)
        max = max(test,max)
        sub = copy.copy(s)
    return min,max

def calculer_proba(alpha,s,elements):
    RESTE = []
    for i in s:
        if not(i in elements):
            RESTE.append(i)
    prob = []
    mini,maxi = Min_Max(s,RESTE)
    RCL = rcl(s,RESTE,mini,maxi,alpha)
    for e in RESTE:
        if e in RCL:
            prob.append(1/len(RCL))
        else:
            prob.append(0)
    return prob

def select_proba(prob,s,elements):
    return

def glouton_proba(alpha):
    e = initialiser(INIT)
    s = e[:]
    while incomplet(s):
        prob = calculer_proba(alpha,s,INIT)
        e = select_proba(prob,s,INIT)
        for i in e:
            if not (i in s):
                s.append(i)
    return s

if __name__ == '__main__':
    init()
