# 🔐 Secure File Vault using System Calls in C

## 📌 Project Overview
This project implements a **Secure File Vault** using low-level system calls in C to provide file security and management.

The system allows users to:
- Encrypt and decrypt files
- Hide and unhide files
- Securely delete files
- Manage file permissions
- Authenticate users using a local database

It demonstrates how operating system concepts can be applied to build a practical security tool.

---

## 🎯 What This Project Does

Sensitive files on local systems are often vulnerable to unauthorized access.

👉 This project:
- Protects files using encryption
- Hides files from normal view
- Permanently deletes files when needed
- Controls access using user authentication

📌 In simple terms:
> This project acts like a secure vault that protects, hides, and manages files using operating system functionalities.

---

## 🚀 Features

- 🔐 File encryption and decryption (XOR-based)
- 👤 User login and registration system
- 📁 Hide and unhide files
- 🗑️ Secure file deletion
- 🔒 File permission management
- ⚙️ Uses low-level Linux system calls

---

## ⚙️ Methodology

The system follows a structured workflow to ensure secure file management:

---

### 🔹 Step 1: User Authentication
- Check if user database (`users.db`) exists
- If empty, register a new user
- Validate login credentials for access
- Store user data securely in a file

---

### 🔹 Step 2: File Encryption & Decryption
- Use **XOR-based encryption technique**
- Read file content using system calls
- Apply XOR operation to each byte
- Write encrypted/decrypted content back to file

---

### 🔹 Step 3: File Hiding & Unhiding
- Hide files by renaming them with a `.` prefix
- Unhide files by removing the prefix
- Use system-level `rename()` function

---

### 🔹 Step 4: Secure File Deletion
- Permanently delete files using `unlink()`
- Ensures files are removed from the filesystem
- Prevents recovery of deleted data

---

### 🔹 Step 5: Permission Management
- Modify file access permissions using `chmod()`
- Control read, write, and execute access

---

### 🔹 Step 6: Menu-Driven Interface
- Provide options:
  - Encrypt file
  - Decrypt file
  - Hide file
  - Unhide file
  - Secure delete
  - Logout
- Allow continuous user interaction

---

## 🧠 Core Concepts Used

- Operating System System Calls
- File Handling in C
- User Authentication
- Data Security Techniques
- File Permissions Management

---

## 🛠️ Technologies Used

- **Language:** C  
- **Platform:** Linux / Ubuntu  
- **System Calls:**
  - `open()`
  - `read()`
  - `write()`
  - `close()`
  - `chmod()`
  - `rename()`
  - `unlink()`


---

## 📊 Output

- Successful user login/registration  
- Files encrypted and decrypted  
- Files hidden/unhidden  
- Files securely deleted  
- Permission changes applied  

---

## 📌 Conclusion

This project demonstrates how **operating system concepts and system calls** can be used to build a secure file management system.

It provides:
- File-level security  
- Controlled access through authentication  
- Efficient file operations at system level  

---

## 🔮 Future Scope

- Stronger encryption algorithms (AES)
- GUI-based interface
- Multi-user access control
- Cloud-based secure storage integration

