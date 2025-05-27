from MerkleTree import MerkleTree

if __name__ == '__main__':
    transactions = ["tx1", "tx2", "tx3", "tx4"]
    mt = MerkleTree(transactions)
    print(mt)
    print('\n\nAfter adding another node')
    mt.add_transaction('tx5')
    print(mt)