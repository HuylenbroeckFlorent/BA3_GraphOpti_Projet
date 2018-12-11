
def calculer_proba(alpha,s,elements):
    RESTE = []
    for i in s:
        if not(i in elements):
            RESTE.append(i)
    prob = []
    #min = min{coût(s U {e}/ e € RESTE)}
    #max = max{coût(s U {e}/ e € RESTE)}
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
    retour s
