from svmutil import *
import sys


labelVector = []
trainInstances = []

for trainSample in range(1,17):
	
	for action in ['open','close']:
		
		print 'Training {}_{}'.format(action,trainSample)
		# Examle training for door open/close action
		sample = []

		# open = 1; close = -1
		if action == 'open':
			label = 1
		elif action == 'close':
			label = -1
		else:
			print 'ERROR: Unidentified action'
			sys.exit(1)
		

		# read all the values of column 5 in a sample
		with open('samples/{}_{}.csv'.format(action,trainSample),'r') as fh:
			for line in fh:
				sample.append(float(line.split(',')[4]))

		# Create 20 bins with features as mean of all sample values -> Feature vector
		binVal = 20
		feature = []
		sample_length = len(sample)
		binLength = sample_length/binVal
		for x in range(0,binVal-1):
			feature.append(sum(sample[x*binLength:(x+1)*binLength])/float(binLength))
		feature.append(sum(sample[(binVal-1)*binLength:sample_length])/float(sample_length - (binVal-1)*binLength))

		# vector normalization
		maxVal = max(map(abs,feature))
		for x in range(0,len(feature)):
			feature[x] = feature[x]/maxVal

		# Debug print
		# for x in feature:
		# 	print x

		labelVector.append(label)
		trainInstances.append(feature)

# train 10 samples, test 6 samples
model = svm_train(labelVector[0:20],trainInstances[0:20])
p_labels, p_acc, p_vals = svm_predict(labelVector[20:32], trainInstances[20:32], model)

svm_save_model('doorSvmModel',model)

