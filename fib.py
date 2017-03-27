import gc

def fibonacci(n):
	if n < 2:
		return n
	else:
		return fibonacci(n-1) + fibonacci(n-2)

def fibonacci_i(n):
	r = [1,1]
	for i in range(2,n):
		r.append(r[i-1]+r[i-2])
	return r

def is_prime(n):
	if n < 2: return False
	for x in range(2,int(n ** 0.5)+1):
		if n % x == 0:
			return False
	return True

#Program loop
while True:
	try:
		gc.collect()
		print ("We will calculate the result of the fibonacci sequence given the input.")
		input_int = int(input("Input: "))
		#temp = []
		temp2 = []
		#for x in range(input_int):
		#	temp.append(fibonacci(x))
		temp = fibonacci_i(input_int)
		for x in temp:
			if is_prime(x):
				temp2.append(x)
		print ("Result:", temp, "\n")
		print ("Primes:", temp2, "\n")
	except ValueError:
		print ("Input error.")
		break