# Opens a .dat file folowing the following model :
# 1st line is the size (size)
# line skip
# first matrix D(size*size)
# line skip
# second matrix F(size*size)
def read_QAP(path):
	D=[]
	F=[]
	with open(path) as file:
		content=file.readlines()
	size=int(content[0])
	for i in range(size):
		D.append([int(elem_D) for elem_D in content[i+2].split()])
		F.append([int(elem_F) for elem_F in content[i+size+3].split()])
	return size,D,F