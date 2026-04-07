import csv
import time

# ---------- AVL Tree Implementation ----------
class AVLNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    def _height(self, node):
        return node.height if node else 0

    def _balance_factor(self, node):
        return self._height(node.left) - self._height(node.right) if node else 0

    def _right_rotate(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self._height(y.left), self._height(y.right))
        x.height = 1 + max(self._height(x.left), self._height(x.right))
        return x

    def _left_rotate(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(self._height(x.left), self._height(x.right))
        y.height = 1 + max(self._height(y.left), self._height(y.right))
        return y

    def _insert(self, node, key, value):
        if not node:
            return AVLNode(key, value), True
        if key == node.key:
            return node, False
        elif key < node.key:
            node.left, inserted = self._insert(node.left, key, value)
        else:
            node.right, inserted = self._insert(node.right, key, value)

        node.height = 1 + max(self._height(node.left), self._height(node.right))
        balance = self._balance_factor(node)

        if balance > 1 and key < node.left.key:
            return self._right_rotate(node), inserted
        if balance < -1 and key > node.right.key:
            return self._left_rotate(node), inserted
        if balance > 1 and key > node.left.key:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node), inserted
        if balance < -1 and key < node.right.key:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node), inserted

        return node, inserted

    def insert(self, key, value):
        start = time.perf_counter()
        self.root, inserted = self._insert(self.root, key, value)
        end = time.perf_counter()
        #print(f"[Insert Time: {end-start:.6f} seconds]")
        return inserted

    def search(self, key):
        start = time.perf_counter()
        cur = self.root
        while cur:
            if key == cur.key:
                end = time.perf_counter()
                print(f"[Search Time: {end-start:.6f} seconds]")
                return cur.value
            elif key < cur.key:
                cur = cur.left
            else:
                cur = cur.right
        end = time.perf_counter()
        print(f"[Search Time: {end-start:.6f} seconds]")
        return None

    def _min_value_node(self, node):
        cur = node
        while cur.left:
            cur = cur.left
        return cur

    def _delete(self, node, key):
        if not node:
            return node, False
        deleted = False
        if key < node.key:
            node.left, deleted = self._delete(node.left, key)
        elif key > node.key:
            node.right, deleted = self._delete(node.right, key)
        else:
            deleted = True
            if not node.left:
                return node.right, deleted
            elif not node.right:
                return node.left, deleted
            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.value = temp.value
            node.right, _ = self._delete(node.right, temp.key)

        node.height = 1 + max(self._height(node.left), self._height(node.right))
        balance = self._balance_factor(node)

        if balance > 1 and self._balance_factor(node.left) >= 0:
            return self._right_rotate(node), deleted
        if balance > 1 and self._balance_factor(node.left) < 0:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node), deleted
        if balance < -1 and self._balance_factor(node.right) <= 0:
            return self._left_rotate(node), deleted
        if balance < -1 and self._balance_factor(node.right) > 0:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node), deleted
        return node, deleted

    def delete(self, key):
        start = time.perf_counter()
        self.root, deleted = self._delete(self.root, key)
        end = time.perf_counter()
        print(f"[Delete Time: {end-start:.6f} seconds]")
        return deleted

    def _count(self, node):
        if not node:
            return 0
        return 1 + self._count(node.left) + self._count(node.right)

    def count_elements(self):
        start = time.perf_counter()
        count = self._count(self.root)
        end = time.perf_counter()
        print(f"[Count Time: {end-start:.6f} seconds]")
        return count
    
    def _keys(self, node, out):
        if not node:
            return
        self._keys(node.left, out)
        out.append(node.key)
        self._keys(node.right, out)

    def keys(self):
        start = time.perf_counter()
        out = []
        self._keys(self.root, out)
        end = time.perf_counter()
        print(f"[Keys Retrieval Time: {end-start:.6f} seconds]")
        return out

# ---------- DJB2 Hash Table using AVL ----------
class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [AVLTree() for _ in range(size)]

    def djb2_hash(self, key):
        h = 5381
        for c in key:
            h = ((h << 5) + h) + ord(c)
            h = h & 0xFFFFFFFFFFFFFFFF  # 64-bit
        return h

    def _hash_index(self, key):
        return self.djb2_hash(key) % self.size

    def insert(self, key, value):
        return self.table[self._hash_index(key)].insert(key, value)

    def search(self, key):
        return self.table[self._hash_index(key)].search(key)

    def delete(self, key):
        return self.table[self._hash_index(key)].delete(key)

    def get_index(self, key):
        start = time.perf_counter()
        idx = self._hash_index(key)
        end = time.perf_counter()
        print(f"[Index Calculation Time: {end-start:.6f} seconds]")
        return idx

    def count_at_index(self, idx):
        if 0 <= idx < self.size:
            return self.table[idx].count_elements()
        return 0

    def keys_at_index(self, idx):
        if 0 <= idx < self.size:
            return self.table[idx].keys()
        return []

    def displayHash(self):
        start = time.perf_counter()
        print("\n--- Hash Table Contents ---")
        for i in range(self.size):
            keys = self.table[i].keys()
            print(f"[{i}]", end='')
            for k in keys:
                print(f" --> {k}", end='')
            print()
        end = time.perf_counter()
        print(f"[Display Time: {end-start:.6f} seconds]")
        print("---------------------------")

# ---------- CSV helpers ----------
def load_dataset(filename):
    transactions = []
    seen = set()
    try:
        with open(filename, "r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row["TxHash"] = row["TxHash"].lower().strip()
                if row["TxHash"] not in seen:
                    transactions.append(row)
                    seen.add(row["TxHash"])
    except FileNotFoundError:
        pass
    return transactions

def save_dataset(filename, transactions):
    if not transactions:
        return
    header = list(transactions[0].keys())
    with open(filename, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        writer.writerows(transactions)

# ---------- TxHash validation ----------
def is_valid_txhash(txhash):
    tx = txhash.lower().strip()
    return tx.startswith("0x") and len(tx) == 66 and all(c in "0123456789abcdef" for c in tx[2:])
def djb2_hash(key,size):
        h = 5381
        for c in key:
            h = ((h << 5) + h) + ord(c)
            h = h & 0xFFFFFFFFFFFFFFFF  # 64-bit
        return h%size

# ---------- Main program ----------
if __name__ == "__main__":
    filename = "test8.csv"
    data = load_dataset(filename)

    ht = HashTable(size=10)
    for tx in data:
        ht.insert(tx["TxHash"], tx)

    while True:
        print("\nOptions:")
        print("1. Add a new transaction")
        print("2. Delete a transaction")
        print("3. Search a transaction")
        print("4. Exit")
        print("5. Find hash table index of a transaction")
        print("6. Count elements at an index")
        print("7. Display entire hash table")
        choice = input("Enter your choice (1-7): ").strip()

        if choice == '1':
            while True:
                txhash = input("Enter Transaction Hash (0x + 64 hex chars): ").strip().lower()
                if is_valid_txhash(txhash):
                    break
                print("Invalid TxHash! Must be 0x followed by 64 hex characters.")
            new_tx = {
                "TxHash": txhash,
                "From": input("Enter From address: ").strip(),
                "To": input("Enter To address: ").strip(),
                "Value": input("Enter Value: ").strip(),
            }
            if ht.insert(new_tx["TxHash"], new_tx):
                data.append(new_tx)
                save_dataset(filename, data)
                print("Transaction inserted and saved to CSV!")
            else:
                print("Duplicate transaction not inserted.")

        elif choice == '2':
            del_hash = input("Enter Transaction Hash to delete: ").strip().lower()
            if ht.delete(del_hash):
                data = [tx for tx in data if tx["TxHash"] != del_hash]
                save_dataset(filename, data)
                print("Transaction deleted from CSV!")
                print("hash table index",djb2_hash(del_hash,10))
            else:
                print("Transaction not found.")

        elif choice == '3':
            search_hash = input("Enter Transaction Hash to search: ").strip().lower()
            result = ht.search(search_hash)
            if result:
                print("\nTransaction Found:")
                for k,v in result.items():
                    print(f"{k}: {v}")
            else:
                print("Transaction not found.")

        elif choice == '4':
            print("Exiting program. Goodbye!")
            break

        elif choice == '5':
            hash_key = input("Enter Transaction Hash to find index: ").strip().lower()
            if ht.search(hash_key):
                idx = ht.get_index(hash_key)
                count = ht.count_at_index(idx)
                print(f"Hash '{hash_key}' maps to index {idx} with {count} transactions.")
                print("Transactions at this index:", ht.keys_at_index(idx))
            else:
                print("Transaction not found.")

        elif choice == '6':
            idx = int(input("Enter index: ").strip())
            count = ht.count_at_index(idx)
            print(f"Index {idx} contains {count} transactions")
            print("Transactions:", ht.keys_at_index(idx))

        elif choice == '7':
            ht.displayHash()

        else:
            print("Invalid choice. Please enter 1-7.")
