import csv
import math
import matplotlib.pyplot as plt
import os

def	getData(file):
	mileages = []
	prices = []
	with open(file, 'r') as csvfile:
		csvReader = csv.reader(csvfile, delimiter=',')
		for row in csvReader:
			mileages.append(row[0])
			prices.append(row[1])
	
	mileages.pop(0)
	prices.pop(0)
	for i in range(len(mileages)):
		mileages[i] = eval(mileages[i])
		prices[i] = eval(prices[i])
	return (mileages, prices)

def	normalizeData(mileages, prices):
	x = []
	y = []
	minM = min(mileages)
	maxM = max(mileages)
	for mileage in mileages:
		x.append((mileage - minM) / (maxM - minM))
	minP = min(prices)
	maxP = max(prices)
	for price in prices:
		y.append((price - minP) / (maxP - minP))
	return (x, y)
	
def	normalizeElem(list, elem):
	return ((elem - min(list)) / (max(list) - min(list)))

def	denormalizeElem(list, elem):
	return ((elem * (max(list) - min(list))) + min(list))
	
def	gradientDescent(mileages, prices, learningRate, iterations):
	lossHistory = []
	t0History = [0.0]
	t1History = [0.0]
	t0 = 0.0
	t1 = 0.0
	
	for iteration in range(iterations):
		dt0 = 0
		dt1 = 0
		for mileage, price in zip(mileages, prices):
			dt0 += (t1 * mileage + t0) - price
			dt1 += ((t1 * mileage + t0) - price) * mileage
		t0 -= dt0 / len(mileages) * learningRate
		t1 -= dt1 / len(prices) * learningRate
		loss = lossFunction(t0, t1, mileages, prices)
		t0, t1, learningRate = boldDriver(loss, lossHistory, t0, t1, dt0, dt1, learningRate, len(mileages))
		lossHistory.append(loss)
		t0History.append(t0)
		t1History.append(t1)
	print("Training done, iteration: {} - loss: {:.8}".format(iteration + 1, loss))
	return (t0, t1, lossHistory, t0History, t1History)
	
def	lossFunction(t0, t1, mileages, prices):
	loss = 0.0
	for mileage, price in zip(mileages, prices):
		loss += (price - (t1 * mileage + t0)) ** 2
	return (loss / len(mileages))

def	boldDriver(loss, lossHistory, t0, t1, dt0, dt1, learningRate, length):
	newLearningRate = learningRate
	if len(lossHistory) > 1:
		if loss >= lossHistory[-1]:
			t0 += dt0 / length * learningRate
			t1 += dt1 / length * learningRate
			newLearningRate *= 0.5
		else:
			newLearningRate *= 1.05
	return (t0, t1, newLearningRate)

def	storeData(t0, t1, file):
	with open(file, 'w') as csvfile:
		csvWriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		csvWriter.writerow([t0, t1])
	
def	displayPlot(t0, t1, mileages, prices, lossHistory, t0History, t1History):
	fig, axs = plt.subplots(2, 2, figsize=(10,8))

	for i in range(len(lossHistory)):
		lineX = [float(min(mileages)), float(max(mileages))]
		lineY = []
		for elem in lineX:
			elem = t1History[i] * normalizeElem(mileages, elem) + t0History[i]
			lineY.append(denormalizeElem(prices, elem))
		
		fig.suptitle('Iteration ' + str(i + 1) + ' / ' + str(len(lossHistory)))

		axs[0, 0].set_title('Result')
		axs[0, 0].plot(mileages, prices, 'bo', lineX, lineY, 'r-')
		
		axs[0, 1].set_title('Loss')
		axs[0, 1].plot(lossHistory[:i], 'r.')

		axs[1, 0].set_title('Theta0')
		axs[1, 0].plot(t0History[:i], 'g.')

		axs[1, 1].set_title('Theta1')
		axs[1, 1].plot(t1History[:i], 'g.')
		
		plt.pause(0.01)

		if i + 1 == len(lossHistory):
			break
		axs[0, 0].cla()
		axs[1, 0].cla()
		axs[0, 1].cla()
		axs[1, 1].cla()
	plt.show()


	
def	main():
	learningRate = 0.5
	iterations = 60
	
	mileages, prices = getData('data.csv')
	x, y = normalizeData(mileages, prices)
	t0, t1, lossHistory, t0History, t1History = gradientDescent(x, y, learningRate, iterations)
	storeData(t0, t1, 'thetas.csv')
	displayPlot(t0, t1, mileages, prices, lossHistory, t0History, t1History)
	
if	__name__ == '__main__':
	main()