import sys
import json
import heapq

THRESHOLD = 100
MAX = 120


fh0 = open('output_0')
fh1 = open('output_1')


array1 = []
with open('output_0') as data:
	for line in data:
		val = line.split(' ')
		#print val
		val[4] = val[4].strip()
		#print val[4]
		array1.append(val[1:])
		#print val[1:]

array1 = array1[1:]

array2 = []
with open('output_1') as data:
	for line in data:
		val = line.split(' ')
		#print val
		val[4] = val[4].strip()
		#print val[4]
		array2.append(val[1:])		
		#print val[1:]



minLen = min(len(array1),len(array2))

jsonDict = {}
opArray = []
prevVal = []
fh = open('steps.csv','w')
for y in range(minLen):
	#print array1[y][2:7],array2[y][2:7]
	#print array1[y][2:],array2[y][2:]
	fh.write(','.join(array1[y][2:]))
	fh.write(',')
	fh.write(','.join(array2[y][2:]))
	fh.write('\n')

	start = float(array1[y][0])
	end = float(array2[y][1])


volume = [0,0,0,0]

for y in range(minLen):
	if float(array1[y][2]) < 120:
		volume[0] += 120 - float(array1[y][2])
	if float(array1[y][3]) < 120:
		volume[1] += 120 - float(array1[y][3])
	if float(array2[y][2]) < 120:
		volume[2] += 120 - float(array2[y][2])
	if float(array2[y][3]) < 120:
		volume[3] += 120 - float(array2[y][3])

# maxIdx = volume.index(max(volume))

idx = heapq.nlargest(3, xrange(len(volume)), key=volume.__getitem__)
vals = heapq.nlargest(3, volume)
#print idx
#print vals

# 0 -> 1*3
# 1 -> 4*3
# 2 -> 7*3
# 3 -> 10*3
dist = [12,18,30,36]
if idx[1] < idx[0]:
	final = dist[idx[0]] - (vals[1]/(vals[1] + vals[2]))*abs(dist[idx[1]]-dist[idx[2]])
	
else:
	final = dist[idx[0]] + (vals[1]/(vals[1] + vals[2]))*abs(dist[idx[1]]-dist[idx[2]])

print 'Position 	: ',final

maxArray = []	
if idx[0] == 0 or idx[0] == 1:
	for y in range(minLen):
		maxArray.append(float(array1[y][idx[0]+2]))
else:
	for y in range(minLen):
		maxArray.append(float(array2[y][idx[0]]))

minIdx = maxArray.index(min(maxArray))

if idx[0] == 0 or idx[0] == 1:
	start = float(array1[minIdx][0])
else:
 	start = float(array2[minIdx][0])

if idx[0] == 0 or idx[0] == 1:
	#print start,float(array1[1][0])
	diffTime = start-float(array1[0][0])
else:
	#print start,float(array2[1][0])
	diffTime = start-float(array2[0][0])
print 'Time 		: ',diffTime

if diffTime < 10:
	key = '00:00:0{}'.format(diffTime)
else:
	key = '00:00:{}'.format(diffTime)
jsonDict[key] = final
jsonTime = diffTime
jsonPos = final

for x in range(5):
	jsonTime += diffTime
	jsonPos += final
	
	if diffTime < 10:
		key = '00:00:0{}'.format(jsonTime)
	else:
		key = '00:00:{}'.format(jsonTime)

	jsonDict[key] = jsonPos
#print jsonDict

	# if len(prevVal) == 0:
	# 	for z in range(len(array1[y])): 
	# 		prevVal.append(array1[y][z])
	# 	for z in range(len(array2[y])): 
	# 		prevVal.append(array2[y][z]) 
	# else:
	# 	for z in range(len(array1[y])): 
	# 		if prevVal[z] < array1[y][z]:
	# 			if (float(array1[y][z]) - float(prevVal))/float(prevVal) > 0.2:
	# 				output.append([str(start*0.5 + end*0.5),z])


	# 		prevVal.append(array1[y][z])
	# 	for z in range(len(array2[y])): 
	# 		prevVal.append(array2[y][z]) 



# 	for x in range(12):
# 		if x < 6:
# 			data = float(array1[y][x+2])
# 		else:
# 			data = float(array2[y][x-4])

# 		if data < THRESHOLD or data > MAX:
# 			op = 0
# 		else:
# 			op = 1
# 		opArray.append(op)
	
# 	if sum(opArray) < 9:
# 		for x in range(len(opArray)):
# 			if opArray[x] == 0:
				
# 				minX = x
# 				cur = x+1
				
# 				while True:
# 					if cur < len(opArray):
# 						if opArray[cur] == 0:
# 							cur += 1
# 						else:
# 							break
# 					else:
# 						break


# 				position = ((cur - x)/2.0) + x*3

# 				jsonDict[str(start*0.5 + end*0.5)] = position
# 				break

with open('position.json','w') as outfile:
	json.dump(jsonDict,outfile)










