import math
import random

def Euclid(a, b):
    """Two integers a & b with a >= b >= 0
    Euclid's algorithm for finding the greatest common divisor of two numbers.
    """
    if b == 0:
        return a
    return Euclid(b, a % b)

def extended_Euclid(a, b):
    """Two integer a & b with a >= b >= 0
    Return integers x, y, d such that d = Euclid(a, b) and a*x + b*y = d
    """
    if b == 0:
        return 1, 0, a
    x1, y1, d = extended_Euclid(b, a % b)
    return y1, x1 - a / b * y1, d

def modinv(a, N):
    """Two n-bit integers a & N
    Return the multiplicative inverse of a modulo N if it exists, else NaN
    """
    x, y, d = extended_Euclid(a, N)
    if d == 1:
        return x % N
    else:
        return float("nan")

def primality2(n):
    """give a positive integer n, testing primality.
    With the power of Fermat's little theorem, we can use a probabilistic tests
    that it makes the probability of failure at most 2^(-100).
    """
    if n <= 102:
        for a in xrange(2, n):
            if pow(a, n - 1, n) != 1:
                return False
        return True
    else:
        for i in xrange(100):
            a = random.randint(2, n - 1)
            if pow(a, n - 1, n) != 1:
                return False
        return True


def generate_prime(n):
    """Return a n-bit prime."""
    while 1:
        p = random.randint(pow(2, n-2), pow(2, n-1)-1)
        p = 2 * p + 1
        if primality2(p):
            return p

class RSA(object):
    def __init__(self, n=256):
        """Generate n-bit prime p, q
        Initialize N=pq, e, d
        """
        self.p = generate_prime(n)
        self.q = generate_prime(n)
        self.N = self.p * self.q
        self.u = (self.p - 1) * (self.q - 1)
        self.e = 3
        while Euclid(self.e, self.u) != 1:
            self.e += 2
        self.d = modinv(self.e, self.u)
    def encrypt(self, msg):
        """encrypt the message, return a list of encoded message."""
        encode_list = [pow(ord(c), self.e, self.N) for c in msg]
        return encode_list
    def decrypt(self, enc):
        """decrypt the list of encoded message."""
        decode_list = [pow(i, self.d, self.N) for i in enc]
        return "".join(unichr(i) for i in decode_list)
