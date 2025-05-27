from random import randint
import hashlib

class SchnorrSiganture:
    def __init__(self, p, q, g):
        self.p = p
        self.q = q
        self.g = g
        self.x = randint(2, q-1)
        self.pub_key = pow(self.g, self.x, self.p)

    def get_pub_key(self):
        return self.pub_key

    def generate_sig(self, bin_message):
        r = randint(2, self.q-1)
        R = pow(self.g, r, self.p)
        e = SchnorrSiganture.find_e(R, self.pub_key, bin_message, self.q)
        s = (r + e*self.x) % self.q

        return R, s


    @staticmethod
    def find_e(R, pub_key, bin_msg, q):
        full_message = bin(R)[2:] + bin(pub_key)[2:] + bin_msg
        return int.from_bytes(hashlib.sha256(full_message.encode()).digest()) % q

    @staticmethod
    def verify_sig(bin_msg, sig, pub_key, g, p, q):
        R, s = sig
        e = SchnorrSiganture.find_e(R, pub_key, bin_msg, q)
        return (R * pow(pub_key, e, p)) % p == pow(g, s, p)
