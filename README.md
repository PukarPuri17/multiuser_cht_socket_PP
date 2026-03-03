# 💬 Multiuser Chat System with Authentication

**Author:** Pukar Puri  
**Course:** Distributed Systems  
**Language:** Python  

---

##  Project Overview

This project implements a **multiuser client-server chat system** using Python socket programming.  
Multiple clients can connect to a central server and communicate in real time.

The system includes user authentication using an SQLite database.

---

## 🏗️ Architecture

- Client-Server architecture
- TCP socket communication
- Multi-threaded server (handles multiple clients simultaneously)
- SQLite database for user authentication

Client 1 ─┐
Client 2 ─┼──> Server ─── SQLite Database
Client 3 ─┘


---

##  Features

-  Multi-client support
-  User registration
-  User login authentication
-  SQLite database storage
-  Broadcast messaging
-  Real-time communication
-  Command-line interface
-  Basic server logging

---

##  Project Structure
multiuser_cht_socket/
│
├── server.py
├── client.py
├── auth_db.py
├── chat.db
├── Documentation.docx
├── TestingReport.docx
└── SourceCode.docx


---

## ▶️ How to Run

### 1️⃣ Start the Server

```bash
python server.py


2️⃣ Start Clients (open multiple terminals)
python client.py

## Authentication Example
REGISTER
username
password

LOGIN
username
password

## Example Chat Session

client 1:
Hello

Client 2 receives:
USER1: Hello

##🧪 Testing Summary

Multiple clients connected successfully

Registration worked correctly

Login authentication worked correctly

Messages were broadcast in real time

No crashes occurred during testing
