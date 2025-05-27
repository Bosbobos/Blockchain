from MerkleTree import MerkleTree
from SchnorrSignature import SchnorrSiganture

if __name__ == '__main__':
    transactions = ["tx1", "tx2", "tx3", "tx4"]
    mt = MerkleTree(transactions)
    print(mt)
    print('\n\nAfter adding another node')
    mt.add_transaction('tx5')
    print(mt)

    p, q, g = 23, 11, 2
    sch = SchnorrSiganture(p, q, g)
    msg = '1101'
    sig = sch.generate_sig(msg)
    print(SchnorrSiganture.verify_sig(msg, sig, sch.get_pub_key(), g, p, q))
    print(SchnorrSiganture.verify_sig('1001', sig, sch.get_pub_key(), g, p, q))
