# 🔍 Transaction Tracing & Fraud Detection System

## 📌 Project Overview
This project focuses on analyzing digital transactions to detect suspicious activities and trace the flow of funds between accounts.

It uses **graph-based analysis and statistical methods** to:
- Identify fraudulent accounts
- Trace transaction paths
- Visualize money flow between users

The system models transactions as a network, enabling efficient monitoring and fraud detection.

---

## 🎯 What This Project Does

In modern financial systems, large numbers of transactions occur continuously, making fraud detection challenging.

 This project:
- Converts transaction data into a **network graph**
- Tracks how money flows between accounts
- Detects unusual patterns in transactions
- Assigns a **fraud score** to each account

📌 In simple terms:
> This project helps identify suspicious transactions and track how money moves between accounts using graph analysis.

---

## 🚀 Features

- 🔗 Transaction network graph visualization
- 🔍 Search transaction by ID
- 🔁 Trace path between accounts
- ⚠️ Fraud detection using scoring system
- 📊 Real-time analysis and updates
- 🌐 Interactive web interface (Flask)

---

## ⚙️ Methodology

The system follows a structured pipeline for fraud detection and transaction tracing:

---

### 🔹 Step 1: Data Preparation
- Load transaction data from CSV files
- Normalize required fields:
  - `txn_id`, `uid`, `from`, `to`, `amount`
- Combine multiple datasets for analysis

---

### 🔹 Step 2: Graph Construction
- Build a **directed graph (DiGraph)** using NetworkX:
  - Nodes → represent accounts  
  - Edges → represent transactions  
- Store transaction details as edge attributes

👉 This enables visualization of fund flow between accounts.

---

### 🔹 Step 3: Transaction Lookup & Path Tracing
- Search transactions using transaction ID
- Trace fund flow from source to destination using **Breadth-First Search (BFS)**
- Identify how money moves across multiple accounts

---

### 🔹 Step 4: Fraud Detection

Each account is assigned a **fraud score (0–100)** based on:

#### 📊 Z-score (Znorm)
- Detects unusual transaction amounts compared to normal behavior

#### 🔗 Centrality (C)
- Measures importance of account in the network
- Highly connected accounts may indicate risk

#### 💰 Bulk Transaction Flag (B)
- Detects frequent high-value transactions

#### ⚡ Spike Detection (S)
- Detects sudden abnormal increases in transaction amount

 Final fraud score is calculated using a weighted combination of these factors.

---

### 🔹 Step 5: Visualization & Interface

- Graph visualization using Matplotlib:
  - Nodes → accounts  
  - Edges → transactions  
  - Highlight suspicious paths  

- Web interface using Flask:
  - View transaction network
  - Search and trace transactions
  - Display fraud scores

---

## 🧠 Core Concepts Used

- Graph Theory (Directed Graphs)
- Breadth-First Search (BFS)
- Statistical Analysis (Z-score)
- Network Centrality Measures
- Data Processing

---

## 🛠️ Technologies Used

- **Backend:** Flask (Python)
- **Data Handling:** Pandas
- **Graph Modeling:** NetworkX
- **Visualization:** Matplotlib
- **Frontend:** HTML, CSS, JavaScript

---

## 📊 Output

- Visual graph of transactions  
- Fraud scores for accounts  
- Highlighted suspicious accounts  
- Traced transaction paths  

---

## 📌 Conclusion

This project demonstrates how **graph-based analysis and statistical techniques** can be used to detect fraud in transaction systems.

It provides:
- Clear visualization of money flow  
- Efficient identification of suspicious activity  
- Real-time monitoring capabilities  

---

## 🔮 Future Scope

- Integration with real-time financial systems  
- Use of machine learning models for prediction  
- Advanced anomaly detection techniques  
- Scalable cloud-based deployment  

