#Nishka Dasgupta
#Programming Assignment 3

def pad(s, l):
    sver = bin(s)[2:]
    while len(sver) < l:
        sver = '0' + sver
    return sver

#Weight of a string
def weight(value):
    w = 0
    for sym in value:
        if sym == '1':
            w = w + 1
    return w

def stringify(vec):
    s = ''
    for item in vec:
        try:
            if len(item) > 0:
                for ele in item:
                    s = s + str(ele)
        except TypeError:
            s = s + str(item)
    return s

def process(eqn):
    terms = eqn.split('+')
    pows = []
    #print(terms)
    for t in terms:
        try:
            x, i = t.strip().split('^')
            pows.append(int(i.strip()))
        except ValueError:
            t = t.strip()
            if t=='1':
                pows.append(0)
            elif t=='x':
                pows.append(1)
    lead = max(pows)
    poly = ''
    for i in range(lead+1):
        if i in pows:
            poly = '1' + poly
        else:
            poly = '0' + poly
    return poly

def mod(dend, sor):
    num = len(dend)
    lead = sor[0]
    sorl = len(sor) - 1
    ctr = num - 1
    dlist = list(dend)
    #print(dend, sor)
    while sorl <= ctr:
        #print(ctr, sorl)
        q = ctr - sorl
        for pos in range(sorl+1):
            if sor[pos] == '1':
                rp = num - 1 - (sorl - pos) - q
                add = str((1 + int(dlist[rp])) % 2)
                dlist[rp] = add
        for i in range(len(dlist)):
            if dlist[i] == '1':
                ctr = num - 1 - i
                break
    rem = ''.join(dlist)
    diff = len(rem) - sorl
    if diff > 0:
        rem = rem[diff:]
    elif diff < 0:
        left = '0' * diff
        rem = left + rem
    return rem

def mult(polylist, minimal):
    p = polylist[0]
    m = len(polylist)
    n = len(p)
    for i in range(1, m):
        curr = polylist[i]
        prod = [0] * (len(p) + len(curr))
        #print(prod)
        for j in range(n-1, -1, -1):
            left = int(p[j])
            for k in range(n-1, -1, -1):
                #print(j, p, k, curr)
                right = int(curr[k])
                if ((left*right)==1):
                    posl = n-1-j
                    posr = n-1-k
                    pos = len(prod) -1-(posl + posr)
                    #print(pos)
                    prod[pos] = (prod[pos] + 1) % 2
        #print(prod)
        pstr = ''
        for item in prod:
            if pstr == '':
                if item == 1:
                    pstr = str(item)
            else:
                pstr = pstr + str(item)
        #print(pstr)
        pint = int(pstr, base=2)
        #print(pint)
        if len(minimal) > 0:
            pn = mod(bin(pint)[2:], minimal)
            p = pad(int(pn, base=2), len(minimal)-1)
        else:
            pn = bin(pint)[2:]
            p = pn
    return p

def findAlpha(n, r, poly):
    alpha = process(input('Enter a primitive root alpha of '+ poly + ': '))
    return pad(int(alpha, base=2), r)

def raiseAlpha(ele, n, r, minpoly):
    table = dict()
    table[0] = pad(1, r)
    table[1] = ele
    #print(table)
    for p in range(2, n):
        #print(p)
        #print(table)
        nxt = mult([ele, table[p-1]], minpoly)
        table[p] = nxt
    return table

def bitxor(a, b):
    num = len(a)
    res = ''
    #print(a, b)
    for i in range(num):
        res = res + str(int(a[i]) ^ int(b[i]))
    return res

def genpoly(n, b, d, r, minpoly):
    alpha = findAlpha(n, r, minpoly)
    altable = raiseAlpha(alpha, n, r, minpoly)
    lim = b + d - 1
    req = '0' * r
    M = []
    for i in range(b, lim):
        for j in range(1, n+1):
            pol = pad(j, r)
            res = 0
            ctr = r-1
            coeff = ''
            for c in pol:
                if c == '1':
                    aft = (i * ctr) % n
                    need = altable[aft]
                    if len(coeff) == 0:
                        coeff = need
                    else:
                        coeff = bitxor(coeff, need)
            if coeff == req:
                M.append(pol)
                break
            ctr = ctr - 1
    
    M = list(set(M))
    g = mult(M, '')
    return g, alpha, altable

def rightrotate(poly, shift):
    res = poly[-shift:] + poly[:-shift]
    return list(res)

def generator(poly, k, n):
    G = []
    row = list(poly)
    row.reverse()
    while len(row) < n:
        row.append('0')
    G.append(row)
    for i in range(1, k):
        targ = rightrotate(row, i)
        nrow = (['0'] * i) + targ
        while len(nrow) < n:
            nrow.append('0')
        G.append(nrow)
    return G

def genParity(alpha, n, b, d):
    H = []
    roots = [1, 3]
    for i in roots:
        row = [0]
        for j in range(1, n):
            p = (i * j) % (n)
            row.append(p)
        H.append(row)
    #print(H)
    return H    

#Multiply two matrices together
def multiply(A, B):
    C = []
    #print('m', len(A), 'n', len(A[0]), 'n', len(B), 'l', len(B[0]))
    for row in A:
        crow = []
        for i in range(len(B[0])):
            csum = 0
            for j in range(len(row)):
                cij = int(row[j])*int(B[j][i])
                csum = csum + cij
            crow.append(csum % 2)
        C.append(crow)
    return C

#Generate the lookup tables for encoding 
def masterKey(G, r):
    key = dict()
    rev = dict()
    lim = 2 ** r
    for i in range(lim):
        m = pad(i, r)
        vec = [[int(x) for x in m]]
        word = multiply(vec, G)
        key[m] = stringify(word)
        rev[stringify(word)] = m
    return key, rev

#Use the lookup table to return the encoding of any message
def encode(msg, code):
    try:
        return code[msg]
    except KeyError:
        print('This message cannot be encoded with this code.')
        return msg

#Calculate the syndrome, decode the received message, and return original message
def decode(H, msg, table, rev):
    try:
        return rev[msg]
    except KeyError:
        syndrome = []
        for row in H:
            s = ''
            for i in range(len(msg)):
                if msg[i] == '1':
                    if len(s) > 0:
                        s = bitxor(s, table[row[i]])
                    else:
                        s = table[row[i]]
            syndrome.append(s)
        for ele in syndrome:
            if weight(ele) > 0:
                print(syndrome)
                print('An error has occurred in transmission. Please request a retransmission.')
                return msg
        
r = int(input('Enter r: '))
n = int(2**r) - 1
k = n - 2*r
d = 5
px = process(input('Enter a generating polynomial of the field GF(2^' + str(r) + '): '))
b = 0
g, alpha, table = genpoly(n, b, d, r, px)
G = generator(g, k, n)
code, rev = masterKey(G, k)
H = genParity(alpha, n, b, d)

#print(rev)
#print(table)

print('Enter 0 to encode, 1 to decode, any other key to quit:')
ch = int(input())
while True:
    if ch==0:
        m = input('Enter the string to be encoded: ')
        c = encode(m, code)
        print('Codeword is: ', c)
    elif ch==1:
        y = input('Enter the string to be decoded: ')
        x = decode(H, y, table, rev)
        print('Message is: ', x)
    else:
        print('Exiting...')
        break
    ch = int(input('Enter your choice: '))
