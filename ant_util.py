#swaps elements i and element j in 1-dim array s
def swap_by_indexes(s,i,j):
	tmp=s[i]
	s[i]=s[j]
	s[j]=tmp