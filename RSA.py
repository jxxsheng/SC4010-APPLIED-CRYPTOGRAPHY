from secrets import SystemRandom
from math import sqrt
import random


class RSA:
    def __init__(self):
        self.e = 65537

    def is_prime(self, n, k =40):
        if n < 2:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0:
            return False
        
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2
        
        for _ in range(k):
            a = random.randrange(2, n - 1)
            x = pow(a, d, n)
            
            if x == 1 or x == n - 1:
                continue
            
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        
        return True


    def generate_prime(self, bits):
        """
        Generate random prime numbers
        """
        not_prime = True
        while not_prime:
            n = SystemRandom().getrandbits(bits)
            # Ensure that the MSB is 1
            n |= (1 << bits-1)
            # Ensure that the LSB is 1
            n |= 1
            if self.is_prime(n):
                not_prime = False
        return n

    def extended_gcd(self, a, b):
        if a == 0:
            return b, 0, 1
        
        gcd_val, x1, y1 = self.extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        
        return gcd_val, x, y

    def inverse(self, e, phi):
        gcd_val, x, y = self.extended_gcd(e, phi)
        
        return x % phi


    def generate_RSA_key(self, bits = 2048):
        """
        Generate RSA keypair
        """
        generated = False
        while not generated:
            p = self.generate_prime(bits//2)
            q = self.generate_prime(bits//2)

            while p == q:
                q = self.generate_prime(bits//2)
            
            n = p * q
            phi = (p-1) * (q-1)
            gcd_of_e_phi = self.gcd(self.e, phi)
            if gcd_of_e_phi == 1:
                generated = True
        d = self.inverse(self.e, phi)
        print("RSA Keys generated")
        return d, n


    def gcd(self, a, b):
        """
        To find greatest common factor
        """
        while b != 0:
            a, b = b, a%b
        return a


    def encrypt(self, m, e, n):
        """
        To do encryption for RSA
        pow (m, e, n) is m to the power of e modulus n
        """
        return pow(m, e, n)


    def decrpyt(self, c, d, n):
        """
        To do decryption for RSA
        pow(c, d, n) is c to the power of d modulus n
        """
        return pow(c, d, n)


def main():
    pass

def test():
    rsa = RSA()
    d , n = rsa.generate_RSA_key()
    message = 43
    ciper_text = rsa.encrypt(message, rsa.e, n)
    decrypted_message = rsa.decrpyt(ciper_text, d, n)
    assert(decrypted_message == message)


if __name__ == "__main__":
    test()
    main()

