# Comparative Analysis of TCP Variants using NS-3

##  Project Overview
This project analyzes and compares the performance of different **TCP congestion control algorithms** using the NS-3 network simulator.

The TCP variants studied include:
- 📊 TcpNewReno  
- ⚡ TcpCubic  
- 🧠 TcpVegas  
- 🚀 TcpBbr  

The system evaluates their performance based on key network metrics such as throughput, delay, and packet loss.

---

##  What This Project Does

In computer networks, multiple devices transmit data simultaneously, which can lead to congestion.

 This project:
- Simulates a network environment using NS-3  
- Applies different TCP variants  
- Measures their performance under the same conditions  
- Compares efficiency based on network metrics  

📌 In simple terms:
> This project compares how different TCP algorithms handle network traffic and identifies which performs best.

---

##  Features

- 🌐 Simulation of network topology using NS-3  
- 🔄 Comparison of multiple TCP variants  
- 📊 Measurement of:
  - Throughput  
  - Delay  
  - Packet Loss  
- ⚙️ Configurable TCP variant selection  
- 📈 Performance analysis of network behavior  

---

## ⚙️ Methodology

The project follows a structured simulation-based approach:

---

### 🔹 Step 1: TCP Variant Selection
- Select TCP variant using command-line input  
- Options include:
  - TcpNewReno  
  - TcpCubic  
  - TcpVegas  
  - TcpBbr  

---

### 🔹 Step 2: Network Topology Creation
- Create **4 nodes**:
  - Sender  
  - Receiver  
  - Intermediate routers  
- Connect nodes using **point-to-point links**  
- Configure:
  - Bandwidth (Data Rate)  
  - Delay  

---

### 🔹 Step 3: Protocol Stack Installation
- Install Internet stack on all nodes  
- Assign IP addresses to each link  
- Enable routing between nodes  

---

### 🔹 Step 4: Application Setup
- Configure:
  - **BulkSend Application** (sender)  
  - **PacketSink Application** (receiver)  
- Establish TCP connection between sender and receiver  

---

### 🔹 Step 5: Simulation Execution
- Start data transmission  
- Run simulation for a fixed duration  
- Monitor network activity  

---

### 🔹 Step 6: Performance Monitoring
- Use **FlowMonitor** to collect metrics:
  - Throughput (data transfer rate)  
  - Delay (latency)  
  - Packet loss  

---

### 🔹 Step 7: Result Analysis
- Extract performance statistics  
- Compare results across TCP variants  
- Identify best-performing algorithm based on:
  - Speed  
  - Reliability  
  - Efficiency  

---

##  Core Concepts Used

- Computer Networks  
- TCP Congestion Control  
- Network Simulation  
- Flow Monitoring  
- Performance Metrics Analysis  

---

##  Technologies Used

- **Language:** C++  
- **Simulator:** NS-3  
- **Tools:**  
  - FlowMonitor (for metrics)  
  - Matplotlib (for visualization - optional)  
- **Environment:** Linux / Ubuntu  

---



---

## 📊 Output

- Throughput values for each TCP variant  
- Delay measurements  
- Packet loss statistics  
- Comparative performance results  

---

## 📌 Conclusion

This project demonstrates how different TCP variants behave under similar network conditions.

- **NewReno**: Stable with good throughput  
- **Cubic**: High throughput for high-speed networks  
- **Vegas**: Low delay, suitable for real-time applications  
- **BBR**: Balanced performance for modern networks  

👉 It helps in selecting the most suitable TCP variant based on network requirements.

---

## 🔮 Future Scope

- Testing under different network conditions  
- Larger and complex network topologies  
- Real-time visualization dashboards  
- Integration with real network systems  
