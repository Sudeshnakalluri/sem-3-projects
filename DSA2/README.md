#  Transaction Management using Hash Tables (AVL Tree & Linked List)

## 📌 Project Overview
This project implements a **Transaction Management System** using **Hash Tables** with two different collision handling techniques:

-  AVL Tree (Self-balancing Binary Search Tree)
- Linked List (Separate Chaining)

The system efficiently stores, searches, and manages transaction data using optimized data structures.

---

## 🎯 What This Project Does

Managing large numbers of transactions requires fast and efficient data access.

👉 This project:
- Stores transaction data using a **hash table**
- Handles collisions using:
  - AVL Trees (balanced and faster search)
  - Linked Lists (simple chaining method)
- Performs operations like:
  - Insert
  - Search
  - Delete
  - Display

📌 In simple terms:
> This project compares two ways of implementing a hash table to manage and retrieve transaction data efficiently.

---

## 🚀 Features

- ➕ Add new transactions  
- 🔍 Search transactions using TxHash  
- ❌ Delete transactions  
- 🔢 Count elements at a hash index  
- 📊 Display full hash table  
- ⚡ Performance tracking (time measurement in AVL version)  

---

## ⚙️ Methodology

The project is implemented using two different approaches for handling collisions in hash tables.

---

### 🔹 Step 1: Data Input & Validation
- Load transaction data from CSV file  
- Validate transaction hash (`TxHash`) format  
- Avoid duplicate entries  

---

### 🔹 Step 2: Hash Function

Two hashing methods are used:

#### 📌 DJB2 Hash Function (AVL Version)
- Converts string key into numeric hash  
- Distributes keys uniformly  

#### 📌 Hexadecimal Conversion (Linked List Version)
- Converts `TxHash` from hex to integer  
- Computes index using modulo operation  

---

### 🔹 Step 3: Hash Table Construction

- Fixed-size hash table array is created  
- Each index (bucket) stores:
  - AVL Tree (in AVL version)  
  - Linked List (in Linked List version)  

---

### 🔹 Step 4: Collision Handling

####  AVL Tree Implementation
- Each bucket stores a **self-balancing AVL Tree**
- Maintains height balance using rotations:
  - Left rotation  
  - Right rotation  
- Ensures **O(log n)** search, insert, delete  

---

####  Linked List Implementation
- Each bucket stores a **linked list**
- New elements are added at the end
- Simpler but less efficient than AVL in worst case  

---

### 🔹 Step 5: Operations

The system supports:

- **Insert**
  - Adds transaction if not duplicate  

- **Search**
  - Finds transaction using hash index + structure traversal  

- **Delete**
  - Removes transaction from dataset and hash table  

- **Index Lookup**
  - Finds hash index of a transaction  

- **Count**
  - Counts elements at a given index  

- **Display**
  - Shows full hash table contents  

---

### 🔹 Step 6: Performance Analysis

- AVL version measures:
  - Insert time  
  - Search time  
  - Delete time  

👉 Used to compare efficiency with linked list approach  

---

##  Core Concepts Used

- Hash Tables  
- Collision Handling  
- AVL Trees (Self-balancing BST)  
- Linked Lists  
- Time Complexity Analysis  
- File Handling (CSV)  

---

## 🛠️ Technologies Used

- **Language:** Python 
- **Libraries:**  
  - CSV  
  - Time  

---



---

##  Output

- Transactions stored and retrieved efficiently  
- Hash table structure displayed  
- Index-based grouping of transactions  
- Performance timings (AVL version)  

---

##  Conclusion

This project demonstrates how different data structures affect the performance of hash tables.

- AVL Trees provide faster and balanced operations  
- Linked Lists offer simpler implementation  

👉 It highlights the trade-off between **efficiency and simplicity** in data structure design.

---

## Future Scope

- Dynamic resizing of hash table  
- Use of other structures (Red-Black Tree)  
- GUI-based visualization  
- Real-time transaction systems  

