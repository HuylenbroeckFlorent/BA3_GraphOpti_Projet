from math import *
import copy
from Voisinage import voisins
import random

alphas = [0,10,20,30,40,50,60,70,80,90,100]
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
        global Taille,D,F,VoisinageG,INIT
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
        i = random.randint(0,Taille)
        j = random.randint(0,Taille)
        while(i==j):
            i = random.randint(0,Taille)
            j = random.randint(0,Taille)
        INIT = VoisinageG[i][j]

def Coute(s):
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

def perm(s,Alpha,mini,maxi):
    test = Coute(s)
    return test <= mini+Alpha*(maxi-mini)

def rcl(s,elements,mini,maxi,Alpha):
    RCL = []
    sub = copy.copy(s)
    for e in elements :
        if not (e in sub):
            sub.append(e)
        if perm(sub,Alpha,mini,maxi):
            RCL.append(e)
        sub = copy.copy(s)
    return RCL

def Min_Max(s,elements):
    sub = copy.copy(s)
    maxi = 0
    mini = inf
    for e in elements:
        sub.append(e)
        test = Coute(sub)
        mini = min(test, mini)
        maxi = max(test, maxi)
        sub = copy.copy(s)
    return mini,maxi

def calculer_proba(Alpha,s,elements):
    RESTE = []
    for i in elements:
        if not(i in s):
            RESTE.append(i)
    prob = Taille*[0]
    mini,maxi = Min_Max(s,RESTE)
    RCL = rcl(s,RESTE,mini,maxi,Alpha)
    for e in RESTE:
        if e in RCL:
            prob[e] = 1/(len(RCL))
    return prob

def select_proba(prob,s,elements):
    sol = []
    for i in range(len(prob)):
        proba = random.randint(0,100)
        if proba<=(prob[i]*100):
            sol.append(elements[i])
    return sol

def glouton_proba(Alpha):
    e = initialiser(INIT)
    s = copy.copy(e)
    while incomplet(s):
        prob = calculer_proba(Alpha,s,INIT)
        e = select_proba(prob,s,INIT)
        for i in e:
            if not (i in s):
                s.append(i)
    return s

def optimize(s,m):
    global Solution,CoutOpti
    if Coute(s)<CoutOpti:
        CoutOpti = Coute(s)
        Solution = s

if __name__ == '__main__':
    init()
    while true:
        s = glouton_proba(0.5)
        s_ = recherche_locale(s)
        optimize(s_,CoutOpti)
    print("%d  %d" Taille,CoutOpti)
