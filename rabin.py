import hashlib

nrabin = 0x1541942cc552a95c4832350ce99c2970f5b3ce9237a09c70c0e867d28039c05209b601105d3b3634cdaee4931809bc0c41d6165a0df16829a3a31202f56003239dd2c6e12297e94ef03e6aa61a147ea2b51c476dc45f5a2406b66d1ece2755c1f3d4144c0a42acc99b599d0643654a4cac392efbcf3db84d4233834afd1

def gcd(a,b):
  if b > a:
    a,b = b,a
  while b > 0:
    a,b = b,a % b
  return a

def nextPrime(p):
 while p % 4 != 3:
   p = p + 1
 return nextPrime_3(p)
  
def nextPrime_3(p):
  m_ = 3*5*7*11*13*17*19*23*29
  while gcd(p,m_) != 1:
    p = p + 4 
  if (pow(2,p-1,p) != 1):
      return nextPrime_3(p + 4)
  if (pow(3,p-1,p) != 1):
      return nextPrime_3(p + 4)
  if (pow(5,p-1,p) != 1):
      return nextPrime_3(p + 4)
  if (pow(17,p-1,p) != 1):
      return nextPrime_3(p + 4)
  return p

# x: bytes
# return: int
def h(x):
  hx = hashlib.sha256(x).digest()
  idx = len(hx)//2
  hl = hashlib.sha256(hx[:idx]).digest()
  hr = hashlib.sha256(hx[idx:]).digest()
  return int.from_bytes(hl + hr, 'little')

# m: bytes
def root(m, p, q):
  i = 0
  while True:
    x = h(m) % nrabin
    #Square Root Computation
    sig =   pow(p,q-2,q) * p * pow(x,(q+1)//4,q) 
    sig = ( pow(q,p-2,p) * q * pow(x,(p+1)//4,p) + sig ) % (nrabin) 
    if (sig * sig) % nrabin == x:
      break
    m = m + bytes.fromhex("00")
    i = i + 1
  #print("paddingnum: " + str(i))
  return sig,str(i)

def writeNumber(number, fnam):
  with open(fnam + '.txt', 'w') as f:
    f.write('%d' % number)

def readNumber(fnam):
  with open(fnam + '.txt', 'r') as f:
    return int(f.read())

def hF(m, paddingnum):
  return h(m + bytes.fromhex("00") * paddingnum) % nrabin

def sF(hexmsg):
  b = bytes(hexmsg, 'utf-8')
  hexmsg=b.hex()
  p = readNumber("p")
  q = readNumber("q")
  sig,padd=root(bytes.fromhex(hexmsg), p, q)
  return hex(sig),padd

def vF(hexmsg, paddingnum, s):
  b = bytes(hexmsg, 'utf-8')
  hexmsg=b.hex()
  return hF(bytes.fromhex(hexmsg), paddingnum) == (s * s) % nrabin

def generate_primes():
    G=['G','01']     
    if G[0] == "G":
      #print(" generate primes ... ")
      p = nextPrime( h(bytes.fromhex(G[1])) % (2**501 + 1) )  
      q = nextPrime( h(bytes.fromhex(G[1] + '00')) % (2**501 + 1) ) 
      
      writeNumber(p, 'p')                     
      writeNumber(q, 'q')     
      #print("nrabin = ", hex(p * q))
      return hex(p * q)
    
def digital_signature(msg):
      sig,padd=sF(str(msg))
      #print((" digital signature:\n " +sig))
      return sig,padd
      

def verification(msg,padd,signature):
      res=vF(str(msg), int(padd), int(signature, 16))
      print("result of ElGamal verification: " + str(res))
      return res

