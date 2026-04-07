# 🔗 Blockchain Transaction Management & Fraud Detection System

## 📌 Project Overview
This project implements a **Blockchain Transaction Management and Fraud Detection System** using Python.

It uses:
- 🔗 Hash Tables for efficient data storage  
- 📄 Linked Lists for collision handling (chaining)  

The system stores, searches, deletes, and analyzes blockchain transactions using a unique **Transaction Hash (TxHash)**.

---

## 🎯 What This Project Does

Managing blockchain transactions requires fast lookup and detection of suspicious activity.

👉 This project:
- Stores transactions using a hash-based system  
- Handles collisions using linked lists  
- Performs operations like insert, search, and delete  
- Detects fraudulent transactions using rule-based analysis  

📌 In simple terms:
> This project efficiently manages blockchain transactions and detects suspicious activities using data structures.

---

## 🚀 Features

- ➕ Add new transactions  
- 🔍 Search transactions using TxHash  
- ❌ Delete transactions  
- 🔢 Find hash table index  
- 📊 Count elements per index  
- 📋 Display full hash table  
- ⚠️ Fraud detection system  

---

## ⚙️ Methodology

The system follows a structured approach for transaction management and fraud detection:

---

### 🔹 Step 1: Data Input & Storage
- Load transaction data from CSV files  
- Maintain:
  - Active transactions file  
  - Deleted transactions file  
- Normalize TxHash values  

---

### 🔹 Step 2: Hash Function

- Convert TxHash (hexadecimal) → integer using manual conversion  
- Compute index using:

  index = TxHash % table_size  

👉 Ensures uniform distribution across hash table  

---

### 🔹 Step 3: Hash Table Construction

- Create fixed-size hash table  
- Each index (bucket) stores a **Linked List**  
- Handle collisions using chaining  

---

### 🔹 Step 4: Transaction Operations

#### ➕ Insertion
- Add new transaction to hash table  
- Store in CSV file  
- Validate TxHash format  

#### ❌ Deletion
- Remove transaction from hash table  
- Move deleted transaction to separate CSV file  

#### 🔍 Search
- Locate transaction using hash index  
- Traverse linked list to find exact match  

#### 📊 Additional Operations
- Find index of a transaction  
- Count elements at a specific index  
- Display entire hash table  

---

### 🔹 Step 5: Fraud Detection

The system detects suspicious transactions based on rules:

#### 🔸 Self-Transaction
- Sender = Receiver  

#### 🔸 High-Value Transaction
- Transaction value exceeds threshold  

#### 🔸 High-Frequency Transactions
- Same sender sends to many recipients  

#### 🔸 Duplicate Transactions
- Same From–To–Value repeated multiple times  

👉 Fraud detection is applied on:
- Active transactions  
- Deleted transactions  

---

### 🔹 Step 6: Data Persistence

- Transactions stored using CSV files  
- Ensures data is retained across executions  

---

##  Core Concepts Used

- Hash Tables  
- Linked Lists  
- Collision Handling (Chaining)  
- File Handling (CSV)  
- Data Validation  
- Fraud Detection Logic  

---





##  Output

- Efficient storage and retrieval of transactions  
- Hash table visualization  
- Index-based grouping of transactions  
- Detection of suspicious transactions with reasons  

---

##  Conclusion

This project demonstrates how **data structures like hash tables and linked lists** can be used to efficiently manage blockchain transactions.

It also integrates **fraud detection mechanisms** to identify suspicious behavior, making the system secure and scalable.

---

##  Future Scope

- Integration with real blockchain APIs  
- Use of machine learning for fraud detection  
- GUI-based interface  
- Real-time transaction monitoring  

