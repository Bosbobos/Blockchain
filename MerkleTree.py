from Node import Node
import hashlib

class MerkleTree:
    def __init__(self, transactions=None):
        self.leaves = []
        self.levels = []  # Иерархия уровней дерева
        self.root = None
        if transactions:
            self.build_tree(transactions)

    def __str__(self):
        if not self.levels:
            return "Merkle Tree is empty"

        tree_str = []

        for level_idx, level in enumerate(reversed(self.levels)):
            tree_str.append(f"Level {level_idx} (Hashes): " + ", ".join(node.hash[:8] + "..." for node in level))
            values = [f"'{node.value}'" for node in level]
            tree_str.append(f"Level {level_idx} (Values): " + ", ".join(values))
            tree_str.append("")  # Пустая строка для разделения

        return "\n".join(tree_str)

    def build_tree(self, transactions):
        self.leaves = [Node(value=tx) for tx in transactions]
        if not self.leaves:
            self.levels = []
            self.root = None
            return

        # Убедимся, что количество листьев чётное
        if len(self.leaves) % 2 != 0:
            self.leaves.append(self.leaves[-1])

        self.levels = [self.leaves]
        self._build_levels()

    def _build_levels(self):
        current_level = self.leaves
        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i+1] if i+1 < len(current_level) else left
                parent = Node(left=left, right=right)
                next_level.append(parent)
            self.levels.append(next_level)
            current_level = next_level

        self.root = current_level[0] if current_level else None

    def add_transaction(self, tx):
        new_leaf = Node(value=tx)
        self.leaves.append(new_leaf)

        # Если количество листьев стало нечётным, дублируем последний
        if len(self.leaves) % 2 != 0:
            self.leaves.append(self.leaves[-1])

        # Обновляем уровни инкрементально
        self._update_levels()

    def _update_levels(self):
        # Начинаем с уровня листьев
        current_level = self.leaves
        self.levels[0] = current_level

        # Пересчитываем только затронутые уровни
        for level_idx in range(1, len(self.levels)):
            parent_level = []
            current_level = self.levels[level_idx-1]

            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i+1] if i+1 < len(current_level) else left
                parent = Node(left=left, right=right)
                parent_level.append(parent)

            if level_idx < len(self.levels):
                self.levels[level_idx] = parent_level
            else:
                self.levels.append(parent_level)

        # Если дерево выросло, добавляем новые уровни
        while len(self.levels[-1]) > 1:
            current_level = self.levels[-1]
            parent_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i+1] if i+1 < len(current_level) else left
                parent = Node(left=left, right=right)
                parent_level.append(parent)
            self.levels.append(parent_level)

        self.root = self.levels[-1][0] if self.levels else None


    def get_root_hash(self):
        return self.root.hash if self.root else None

    def get_proof(self, tx):
        # Находим индекс листа с транзакцией
        index = -1
        for i, leaf in enumerate(self.leaves):
            if leaf.value == tx:
                index = i
                break
        if index == -1:
            return []

        proof = []
        current_index = index
        for level in self.levels[:-1]:  # Исключаем корневой уровень
            level_nodes = level
            sibling_index = current_index + 1 if current_index % 2 == 0 else current_index - 1
            if sibling_index >= len(level_nodes):
                sibling_index = current_index  # Если вышли за границы, берём тот же узел
            sibling = level_nodes[sibling_index]
            proof.append(sibling.hash)
            current_index = current_index // 2  # Переходим на уровень выше

        return proof

    @staticmethod
    def verify_proof(tx, proof, root_hash):
        current_hash = hashlib.sha256(tx.encode()).hexdigest()
        for sibling_hash in proof:
            # Определяем порядок конкатенации
            combined = (current_hash + sibling_hash).encode()
            current_hash = hashlib.sha256(combined).hexdigest()
        return current_hash == root_hash