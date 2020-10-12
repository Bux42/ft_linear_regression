import os
import csv

from train import normalizeElem, denormalizeElem, getData

def	estimatePrice(thetas, mileage, mileages, prices):
	price = thetas[1] * normalizeElem(mileages, mileage) + thetas[0]
	return (denormalizeElem(prices, price))

def	getMileage():
	while 1:
		print('Enter a mileage: ')
		mileage = input()
		try:
			mileage = int(mileage)
			if mileage >= 0:
				break
			else:
				print('Invalid input')
		except ValueError:
			print('Invalid input')
	return (mileage)

def	getThetas(thetas):
	t0, t1 = 0, 0
	if (os.path.isfile(thetas)):
		with open(thetas, 'r') as csvfile:
			file = csv.reader(csvfile, delimiter=',')
			for row in file:
				t0 = float(row[0])
				t1 = float(row[1])
				break
	return (t0, t1)

def	main():
	thetas = getThetas('thetas.csv')
	mileage = getMileage()
	mileages, prices = getData('data.csv')
	price = estimatePrice(thetas, mileage, mileages, prices)
	print('Price estimation: {}'.format(price))

if __name__ == "__main__":
	main()