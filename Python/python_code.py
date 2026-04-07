import csv
# -------------------------
# Node class for Linked List
# -------------------------
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

# -----------------
# Linked List class
# -----------------
class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, key, value):
        new_node = Node(key, value)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        return True

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
                return current.value 
            prev = current
            current = current.next
        return None

    def count_elements(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def keys(self):
        result = []
        current = self.head
        while current:
            result.append(current.key)
            current = current.next
        return result

# -------------------------
# Manual Hex → Int
# -------------------------
def manual_hex_to_int(hex_str):
    hex_str = hex_str.lower().strip()
    if hex_str.startswith("0x"):
        hex_str = hex_str[2:]
    hex_digits = "0123456789abcdef"
    decimal_value = 0
    power = 0
    for char in reversed(hex_str):
        if char not in hex_digits:
            return None
        decimal_value += hex_digits.index(char) * (16 ** power)
        power += 1
    return decimal_value

# -------------------------
# Hash Table
# -------------------------
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
        return self.table[index].insert(key, value)

    def search(self, key):
        index = self._hash(key)
        if index is None:
            return []
        return self.table[index].search(key)

    def delete(self, key):
        index = self._hash(key)
        if index is None:
            return []
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
            print(f"[{i}]", end='')
            for k in self.table[i].keys():
                print(f" --> {k}", end='')
            print()
        print("---------------------------")

# -------------------------
# Load & Save CSV
# -------------------------
def load_dataset(filename):
    transactions = []
    with open(filename, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            row["TxHash"] = row["TxHash"].lower().strip()
            transactions.append(row)
    return transactions

def save_dataset(filename, transactions):
    if not transactions:
        return
    header = list(transactions[0].keys())
    with open(filename, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        writer.writerows(transactions)

# -------------------------
# TxHash validation
# -------------------------
def is_valid_txhash(txhash):
    tx = txhash.lower().strip()
    if not tx.startswith("0x"):
        return False
    hex_part = tx[2:]
    if len(hex_part) != 64:
        return False
    return all(c in "0123456789abcdef" for c in hex_part)

# -------------------------
# Fraud Detection
# -------------------------

def check_fraud(tx, all_transactions=None):
    reasons = []

    # 1. Self-transaction: sender == receiver
    if tx['From'] == tx['To']:
        reasons.append("Self-transaction")

    # 2. High-value transaction: Value > 5 Ether
    try:
        value_num = float(tx['Value'].split()[0])
        if value_num > 5:
            reasons.append("High-value transaction")
    except:
        pass

    if all_transactions:
        # 3. High-frequency transactions from same sender
        sender_txs = [t for t in all_transactions if t['From'] == tx['From'] and t['TxHash'] != tx['TxHash']]
        # Count unique recipients
        unique_recipients = set(t['To'] for t in sender_txs)
        if len(unique_recipients) >= 5:
            reasons.append("High-frequency transactions from same sender to different recipients")

        # 4. Duplicate From-To-Value transactions
        duplicate_count = sum(
            1 for t in all_transactions
            if t['From'] == tx['From'] and t['To'] == tx['To'] and t['Value'] == tx['Value']
        )
        if duplicate_count >= 5:
            reasons.append("Duplicate From-To-Value transaction")

    return reasons

# -------------------------
# Main Program
# -------------------------
if __name__ == "__main__":
    active_file = "100_transaction_dataset.csv"
    deleted_file = "deleted_transactions.csv"


    data = load_dataset(active_file)
    deleted_data = load_dataset(deleted_file)

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
        print("8. Fraud check for all transactions (active + deleted)")
        choice = input("Enter your choice (1-8): ").strip()

        if choice == '1':
            while True:
                txhash = input("Enter Transaction Hash (0x + 64 hex chars): ").strip().lower()
                if is_valid_txhash(txhash):
                    break
                print("Invalid TxHash!")
            
            new_tx = {
                "Record": input("Enter : ").strip(),
                "TxHash": txhash,
                "From": input("Enter From address: ").strip(),
                "To": input("Enter To address: ").strip(),
                "Value": input("Enter Value: ").strip(),            }

            ht.insert(new_tx["TxHash"], new_tx)
            data.append(new_tx)
            save_dataset(active_file, data)
            print("Transaction inserted and saved to CSV!")
            fraud_reasons = check_fraud(new_tx, data + deleted_data)
            if fraud_reasons:
                print(" Fraud detected! Reasons:", ", ".join(fraud_reasons))
            else:
                print(" Transaction appears normal.")

        elif choice == '2':
            del_hash = input("Enter Transaction Hash to delete: ").strip().lower()
            deleted_nodes = ht.delete(del_hash)
            if deleted_nodes:
                data = [tx for tx in data if tx["TxHash"] != del_hash]
                save_dataset(active_file, data)
                deleted_data.append(deleted_nodes)
                save_dataset(deleted_file, deleted_data)
            else:
                print("Transaction not found.")

        elif choice == '3':
            search_hash = input("Enter Transaction Hash to search: ").strip().lower()
            result = ht.search(search_hash)  # directly assign to result
            if result:
                print("\nTransaction Details:")
                for k, v in result.items():
                    print(f"{k}: {v}")
                fraud_reasons = check_fraud(result, data + deleted_data)
                if fraud_reasons:
                    print(" Fraud detected! Reasons:", ", ".join(fraud_reasons))
                else:
                    print(" Transaction appears normal.")
            else:
                print("Transaction not found.")


        elif choice == '4':
            print("Exiting program. Goodbye!")
            break

        elif choice == '5':
            hash_key = input("Enter Transaction Hash to find index: ").strip().lower()
            if ht.search(hash_key):
                index = ht.get_index(hash_key)
                count = ht.count_at_index(index)
                print(f"Index: {index}, Transactions at index: {count}")
                print("TxHashes at this index:", ht.keys_at_index(index))
            else:
                print("Transaction not found.")

        elif choice == '6':
            idx = int(input("Enter index: ").strip())
            count = ht.count_at_index(idx)
            print(f"Index {idx} contains {count} transactions")
            print("TxHashes:", ht.keys_at_index(idx))

        elif choice == '7':
            ht.displayHash()

        elif choice == '8':
            print("\n--- Fraud Check (Active + Deleted) ---")
            combined = data + deleted_data
            processed_hashes = set()
            for tx in combined:
                if tx['TxHash'] in processed_hashes:
                    continue
                processed_hashes.add(tx['TxHash'])
                reasons = check_fraud(tx, combined)
                if reasons:
                    print(f"{tx['TxHash']}:  {', '.join(reasons)}")
                    
        else:
            print("Invalid choice. Please enter 1-8.")