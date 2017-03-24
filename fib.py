def fibonacci(n):
	if n == 0:
		return 0
	elif n == 1:
		return 1
	else:
		return fibonacci(n-1) + fibonacci(n-2)


#Program loop
while True:
	try:
		print "We will calculate the result of the fibonacci sequence given the input."
		input_int = int(raw_input("Input: "))
		temp = []
		for x in range(input_int):
			temp.append(fibonacci(x))
		print "Result:", temp, "\n"
	except:
		print "Input error."
		break