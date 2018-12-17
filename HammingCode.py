#Nishka Dasgupta
#Programming Assignment 1

#Initialising
r = int(input('Enter parameter r: '))
n = (2 ** r) - 1
k = n - r
d = 3
key = dict()
rev = dict()
colpos = dict()

H = []
G = []
Ir = []

#Weight of a string
def weight(value):
    w = 0
    for sym in value:
        if sym == '1':
            w = w + 1
    return w

#Extend a string to required number of bits by prepending 0
def pad(bitstring, l):
    rem = l - len(bitstring)
    for ctr in range(rem):
        bitstring = '0' + bitstring
    return bitstring

#Create generator matrix G and parity check matrix H for a Hamming code with given parameter r
def initialise():
    for i in range(r):
        H.append([])
        Ir.append([])

    for i in range(1, n+1):
        c = pad(bin(i)[2:], r)
        if weight(c) > 1:
            for j in range(r):
                H[j].append(int(c[j]))
            G.append([int(x) for x in c])
            colpos[i] = len(H[j]) - 1
        else:
            for index in range(r):
                if pad(bin(2**index)[2:], r) == c:
                    colpos[i] = n - 1 - index
            for j in range(r):
                Ir[j] = [c[j]] + Ir[j]

    for j in range(r):
        H[j] = H[j] + Ir[j]

    for j in range(k):
        iden = [0] * k
        iden[j] = 1
        G[j] = iden + G[j]

#Convert a row or column vector into a string
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

#Multiply two matrices together
def multiply(A, B):
    C = []
    #print('m', len(A), 'n', len(A[0]), 'n', len(B), 'l', len(B[0]))
    for row in A:
        crow = []
        for i in range(len(B[0])):
            csum = 0
            for j in range(len(row)):
                try:
                    cij = int(row[j])*int(B[j][i])
                except:
                    print(B)
                csum = csum + cij
            crow.append(csum % 2)
        C.append(crow)
    return C

#Generate the lookup tables for encoding 
def masterKey():
    lim = 2 ** k
    for i in range(lim):
        m = pad(bin(i)[2:], k)
        vec = [[int(x) for x in m]]
        word = multiply(vec, G)
        key[m] = stringify(word)
        rev[stringify(word)] = m

#Use the lookup table to return the encoding of any message
def encode(msg):
    try:
        return key[msg]
    except KeyError:
        print('This message cannot be encoded with this code.')

#Calculate the syndrome, decode the received message, and return original message
def decode(msg):
    vec = [[int(x)] for x in msg]
    syndrome = multiply(H, vec)
    syn = ''
    for ele in syndrome:
        syn = syn + str(ele[0])
    if weight(syn) == 0:
        return rev[msg]
    else:
        shift = int(syn, base=2)
        pos = colpos[shift]
        crctd = '0'
        if msg[pos] == '0':
            crctd = '1'
        dec = msg[:pos] + crctd + msg[pos+1:]
        print('Decoded codeword is', dec)
        return rev[dec]
initialise()
masterKey()
#print(key)
#print(rev)
cont = True

#Infinite loop for user input
while cont:
    user = int(input('Enter 1 to encode, 2 to decode, anything else to exit... '))
    if user == 1:
        msg = input('Enter message to encode: ')
        print(encode(msg))
    elif user == 2:
        msg = input('Enter message to decode: ')
        print(decode(msg))
    else:
        cont = False
