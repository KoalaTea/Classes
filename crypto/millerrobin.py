#!/usr/bin/python
#Ryan Whittier


def main():
	start = 90000
	end = 100000
	primedict = {}
	error = 0
	for num in range(start, end):		#num is the odd number being tested
	#for num in range(100000, 100050):
		if(num%2!=0):
			error=0
			p = num - 1		#the n-1 value to determine the odd factor in use
			exp=0			#counter for testing exponetials
		
			r=p;
			while(r%2==0):		#find r which iss the n-1=2^exp * r 
				r=r/2
				exp=exp+1
			rbinary = tobinary(r)	#make our r binary

			prime = bruter(num)	#check if number is prime for later testing
			for a in range(2,num-1):#range from 
				res = squareandmult(a, rbinary, num)
				if(prime):	#if prime error should be 0 make sure alg works
					if(res):#if not 1modn test for -1modn
						s = 0
						while(res==1 and s < exp):
							r2=r*(2**s)
							res = test2(a, tobinary(r2), num)
							s=s+1
					error = error + res
				else:		#if not prime reverse 0 and 1 returns from squareandmult
						#as well as test2
					if(res):
						s = 0
						while(res==1 and s < exp):
							r2=r*(2**s)
							res = test2(a, tobinary(r2), num)
							s=s+1
						if(res):
							pass	#if comes none prime do nothing
						else:
							error = error +1 #if prime error
					else:
						error = error + 1
			
			primedict[num] = float(error)/float(num-2) #make dict for nums and errors
			print(num)
			print(primedict[num])
	mylist=[]
	topten={}
	#this whole section gets the top 10 errors using loops to compare the numbers
	for i in range(0,10):
		topten[i]=[0,0]
	for key in primedict.keys():
		for key2 in topten.keys():
			if(topten[key2][1]<primedict[key]):
				tempkey = 9
				while(tempkey>key2):
					topten[tempkey]=topten[tempkey-1]
					tempkey = tempkey - 1
				topten[key2]=[key,primedict[key]]
				break
				
	#print the top ten errors
	print("The top ten errors are:")
	for key in topten.keys():
		print(key+1)
		print("Number: " + str(topten[key][0]))
		print("Error : " + str(topten[key][1]) + "\n")
		

#
# squareandmult:
#	does square and multiply for the exponentiation of the random a
#
# args:
#	a - random int to be raised to test (base) (also not random...)
#	m - exponent (binary)
#	n - number being tested used as mod in this portion
#
def squareandmult(a, m, n):
	current = 1
	for i in m:
		if(i == 0):
			current = (current * current) % n
		else:
			current = (current * current * a) % n
	if(current == 1):
		return 0
	else:
		return 1

#
# test2
#	same as squareandmult except testing for -1modn
#
def test2(a,m,n):
	current = 1
        for i in m:
                if(i == 0):
                        current = (current * current) % n
                else:
                        current = (current * current * a) % n
        if(current == (n-1) ):
                return 0
        else:
                return 1

def bruter(n):
	temp = 2
	prime = 1
	while(prime==1):
		if( ((n/2)+1) < temp ):
			break
		if(n%temp==0):
			prime = 0
		else:
			temp = temp + 1
	return prime

def tobinary(m):
	binary = []			#binary holds the exponent in binary form
	while(m != 0):			#loop to change to binary
		binary.append(m%2)	#append a 1 if odd 0 if even
		m = m / 2		#half the size using python div (does int div not float)(floors)
	binary.reverse()
	return binary

main()
