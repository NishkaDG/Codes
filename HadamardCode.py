#TODO: sylvester
#test paley

import math
import secrets

def squareandmultiply(x, c, n):
    z = 1
    l = len(c)
    for i in range(l-1, -1, -1):
        z = (z*z) % n
        pos = l - 1 - i
        #print('i', i)
        #print('bi', c[l-1-i])
        if c[pos]=='1':
            z = (z*x) % n
        #print('z', z)
    return z

def decompose(num):
    k = 0
    m = 1
    while (num%2) == 0:
        k = k+1
        num//=2
    m = int(num)
    return k, m

def millerrabin(n, d):
    prev = n-1
    a = secrets.randbelow(n-1)
    while a < 2:
        a = secrets.randbelow(n-1)
    #x = pow(a, d, n)
    x = squareandmultiply(a, bin(d), n)
    if (x==1) or (x==prev):
        return True
    while not (d==prev):
        #x = pow(x, 2, n)
        x = (x * x) % n
        d = d * 2
        if x==1:
            return False
        if x==prev:
            return True
    return False

def isPrime(n):
    #print(n)
    if n < 2:
        return False
    prev = n - 1
    k, m = decompose(prev)
    for i in range(10):
        if millerrabin(n, m) == False:
            return False
    return True

def Log2(x): 
    return (math.log10(x) / math.log10(2))

def isPowerOf2(n):
    logn = Log2(n)
    return (math.ceil(logn) == math.floor(logn))

def toBinary(H):
    for i in range(len(H)):
        for j in range(len(H)):
            ele = H[i][j]
            if ele == 1:
                H[i][j] = 0
            else:
                H[i][j] = 1

def quadraticResidues(p):
    lst = []
    for i in range(1, p):
        s = (i * i) % p
        if s not in lst:
            lst.append(s)
    return lst

def rshift(row):
    nextrow = [row[-1]] + row[:-1]
    return nextrow

def sylvester(n):
    if n == 1:
        return [[1]]
    else:
        prev = int(n / 2)
        pH = sylvester(prev)
        H = []
        for i in range(n):
            if i < prev:
                H.append(pH[i] + pH[i])
            else:
                row = pH[i-prev]
                neg = []
                for item in row:
                    neg.append(-item)
                H.append(row + neg)
        return H

def paley(n):
    p = n-1
    if isPrime(p):
        qr = quadraticResidues(p)
        H = [[1] * n]
        first = [1]
        for j in range(p):
            if j == 0:
                first.append(0)
            elif j in qr:
                first.append(1)
            else:
                first.append(-1)
        H.append(first)
        for i in range(2, n):
            row = [1] + rshift(H[i-1][1:])
            H.append(row)
        return H
    else:
        print('may be possible')
        return [[]]

def display(H):
    toBinary(H)
    for row in H:
        line = ''
        for item in row:
            line = line + str(item) + ' '
        print(line)

n = int(input('Enter parameter n: '))
H = [[]]
if ((n%4) > 0) and (n > 2):
    print('not possible')
else:
    if isPowerOf2(n):
        print('Attempting a Sylvester construction...')
        H = sylvester(n)
    else:
        print('Attempting a Paley construction...')
        H = paley(n)
if len(H[0]) > 0:
    print('Hadamard matrix found!')
    display(H)
