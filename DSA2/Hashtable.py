import csv

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

# Linked List class
class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, key, value):
        # Check if key already exists
        current = self.head
        while current:
            if current.key == key:
                print(f"Duplicate TxHash {key} not allowed ")
                return False   # Duplicate found → don't insert
            current = current.next

        new_node = Node(key, value)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current =current.next
            current.next = new_node

    def search(self, key):
        current = self.head
        while current:
            if current.key == key:
                return current.value
            current = current.next
        return None

    def delete(self, key):
        current = self.head
        prev = None
        while current:
            if current.key == key:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return True
            prev = current
            current = current.next
        return False

    def count_elements(self):
        current = self.head
        count = 0
        while current:
            count += 1
            current = current.next
        return count

    def keys(self):
        current = self.head
        result = []
        while current:
            result.append(current.key)
            current = current.next
        return result


# Manual Hex → Int conversion
def manual_hex_to_int(hex_str):
    hex_str = hex_str.lower().strip()
    if hex_str.startswith("0x"):
        hex_str = hex_str[2:]

    hex_digits = "0123456789abcdef"
    decimal_value = 0
    power = 0

    for char in reversed(hex_str):
        if char not in hex_digits:
            return None  # invalid hex character
        digit_value = hex_digits.index(char)
        decimal_value += digit_value * (16 ** power)
        power += 1

    return decimal_value

# Hash Table class using hex TxHash
class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [LinkedList() for _ in range(size)]

    def _hex_to_int(self, key):
        return manual_hex_to_int(key)

    def _hash(self, key):
        tx_int = self._hex_to_int(key)
        if tx_int is None:
            return None
        return tx_int % self.size

    def insert(self, key, value):
        index = self._hash(key)
        if index is None:
            return False
        return self.table[index].insert(key, value)   # return actual result

    def search(self, key):
        index = self._hash(key)
        if index is None:
            return None
        return self.table[index].search(key)

    def delete(self, key):
        index = self._hash(key)
        if index is None:
            return False
        return self.table[index].delete(key)

    def get_index(self, key):
        return self._hash(key)

    def count_at_index(self, index):
        if 0 <= index < self.size:
            return self.table[index].count_elements()
        return 0

    def keys_at_index(self, index):
        if 0 <= index < self.size:
            return self.table[index].keys()
        return []

    def displayHash(self):
        print("\n--- Hash Table Contents ---")
        for i in range(self.size):
            print(f"[{i}]", end='')   # f-string for index
            for k in self.table[i].keys():
                print(f" --> {k}", end='')  # f-string for key
            print()
        print("---------------------------")

def load_dataset(filename):
    transactions = []
    seen = set()   # prevent duplicates when loading
    try:
        with open(filename, "r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row["TxHash"] = row["TxHash"].lower().strip()
                if row["TxHash"] not in seen:   # skip duplicates
                    transactions.append(row)
                    seen.add(row["TxHash"])
    except FileNotFoundError:
        pass  # return empty if no file
    return transactions

def save_dataset(filename, transactions):
    if not transactions:
        return
    header = list(transactions[0].keys())
    with open(filename, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        writer.writerows(transactions)

# TxHash validation function
def is_valid_txhash(txhash):
    tx = txhash.lower().strip()
    if not tx.startswith("0x"):
        return False
    hex_part = tx[2:]
    if len(hex_part) != 64:  # standard Ethereum TxHash length
        return False
    return all(c in "0123456789abcdef" for c in hex_part)


if __name__ == "__main__":
    filename = "test1.csv"
    data = load_dataset(filename)

    ht = HashTable(size=10)
    for tx in data:
        ht.insert(tx["TxHash"], tx)

    while True:
        print("\nOptions:")
        print("1. Add a new transaction ")
        print("2. Delete a transaction ")
        print("3. Search a transaction")
        print("4. Exit")
        print("5. Find hash table index of a transaction")
        print("6. Count elements at an index")
        print("7. Display entire hash table")
        choice = input("Enter your choice (1-7): ").strip()

        if choice == '1':
            while True:
                txhash = input("Enter Transaction Hash (0x followed by 64 hex chars): ").strip().lower()
                if is_valid_txhash(txhash):
                    break
                print("Invalid TxHash! Must be 0x followed by 64 hexadecimal characters (0-9, a-f).")

            new_tx = {
                "TxHash": txhash,
                "From": input("Enter From address: ").strip(),
                "To": input("Enter To address: ").strip(),
                "Value": input("Enter Value: ").strip(),
            }

            if ht.insert(new_tx["TxHash"], new_tx):   # only insert if not duplicate
                data.append(new_tx)
                save_dataset(filename, data)  # save only if new
                print("Transaction inserted and saved to CSV!")
            else:
                print("Duplicate transaction not inserted ")

        elif choice == '2':
            del_hash = input("Enter Transaction Hash to delete: ").strip().lower()
            if ht.delete(del_hash):
                data = [tx for tx in data if tx["TxHash"] != del_hash]
                save_dataset(filename, data)
                print(" Transaction deleted from CSV!")
            else:
                print(" Transaction not found or invalid.") 

        elif choice == '3':
            search_hash = input("Enter Transaction Hash to search: ").strip().lower()
            result = ht.search(search_hash)
            if result:
                print("\n Transaction Found:")
                for k,v in result.items():
                    print(f"{k}: {v}")
            else:
                print(" Transaction not found.")

        elif choice == '4':
            print("Exiting program. Goodbye!")
            break

        elif choice == '5':
             hash_key = input("Enter Transaction Hash to find index: ").strip().lower()

            # Only allow if the transaction exists in the hash table
             if ht.search(hash_key) is not None:
                index = ht.get_index(hash_key)
                count = ht.count_at_index(index)
                print(f"The transaction hash '{hash_key}' maps to index: {index}")
                print(f" Number of transactions at this index : {count}")
                print("IDs at this index:", ht.keys_at_index(index))
             else:
                print(" Transaction ID not found. Only existing transactions are allowed.")

        elif choice == '6':
            idx = int(input("Enter index: ").strip())
            count = ht.count_at_index(idx)
            print(f"Index {idx} contains {count} transactions")
            print("IDs:", ht.keys_at_index(idx))

        elif choice == '7':
            ht.displayHash()

        else:
            print("Invalid choice. Please enter 1-7.")
