
def fib(n):
	if n == 0: return 1
	if n == 1: return 2
	return fib(n-1)+fib(n-2)

def is_fib(n):
	b = 0
	while True:
		r = fib(b)
		if r == n:
			return True
		elif r > n:
			return False
		b += 1

inputi = int(input())
print (is_fib(inputi))