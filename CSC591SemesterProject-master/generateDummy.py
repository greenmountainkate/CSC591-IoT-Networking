import random
import sys

timeStr="00:00:"
maxLength=2750
strideAvg=80
speedAg=14 
dist=0
t=0
sNum=10

try:
	fileName=str(sys.argv[1])
except:
	print "Usage: generateDummy.py <dummy-file-name>"
	exit()

distList=[]
strideList=[]
timeList=[]
for i in range(0,sNum):
	strideList.append(random.randrange(strideAvg-5,strideAvg+5,1))
	timeList.append(float(random.randrange(45,75,2))/100)
	dist+=strideList[i]
	distList.append(dist)
	timeList[i]=timeStr+"0"+str(timeList[i])
strideList.sort()
timeList.sort(reverse=True)
distList.sort(reverse=True)

f=open("dummy"+fileName+".json","w")
f.write('{\n')
for i in range (0,10):
	if i!=9:
		stri='	"'+timeList[i]+'":'+str(distList[i])+',\n'
	else:
		stri=stri='	"'+timeList[i]+'":'+str(distList[i])+'\n'
	f.write(stri)
f.write("}")
f.close()


