def fibonnaci(n):
	if n == 0:
		return 0
	elif n == 1:
		return 1
	else:
		return fibonnaci(n-1) + fibonnaci(n-2)


#Program loop
while True:
	try:
		print "We will calculate the result of the fibonnaci sequence given the input."
		input_int = int(raw_input("Input: "))
		temp = []
		for x in range(input_int):
			temp.append(fibonnaci(x))
		print "Result:", temp, "\n"
	except:
		print "Input error."
		break