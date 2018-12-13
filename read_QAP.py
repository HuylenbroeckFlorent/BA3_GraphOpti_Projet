# Opens a .dat file folowing the following model :
# 1st line is the size (size)
# line skip
# first matrix D(size*size)
# line skip
# second matrix F(size*size)
def read_QAP(path):
	with open(path,'r') as file:
		content=file.readlines()
		file.close()

	wholefile=[]

	for line in content:
		wholefile.extend([nums for nums in line.split()])

	size=int(wholefile.pop(0))

	distances=[]
	flows=[]

	for _ in range(size):
		row=[]
		for __ in range(size):
			row.append(int(wholefile.pop(0)))
		distances.append(row)

	for _ in range(size):
		row=[]
		for __ in range(size):
			row.append(int(wholefile.pop(0)))
		flows.append(row)

	return size,distances,flows