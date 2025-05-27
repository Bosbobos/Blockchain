import hashlib

class Node:
    def __init__(self, left=None, right=None, value=None, node_hash=None):
        self.left = left
        self.right = right
        self.value = value
        self.hash = node_hash

        if self.left == self.right == self.value:
            raise ValueError('A node must have a value or children.')

        if (self.left is not None
                and self.right is not None
                and self.value is not None):
            raise ValueError('Only leafs can be created with a value.')

        if self.value is not None:
            self.find_hash()
            return
        elif self.left is not None and self.right is None:
            self.right = self.left
        elif self.right is not None and self.left is None:
            self.left = self.right

        self.value = self.left.hash + self.right.hash
        self.find_hash()

    def find_hash(self):
        if isinstance(self.value, str):
            value = self.value.encode()
        self.hash = hashlib.sha256(value).hexdigest()