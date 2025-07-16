# Two-Phase Distributed Commit System (2PC)
**Contributors:**

- SUHITH GHANATHAY - Date: 24TH JUNE, 2024

---

## Project Overview

This project implements a **Two-Phase Commit (2PC) Distributed Transaction System** for a simulated banking environment. It ensures atomicity and consistency of transactions (such as credit and debit) across distributed nodes, using Python and TinyDB. The system is designed to demonstrate distributed transaction management, fault tolerance, and the 2PC protocol in action.

---

## Tags

`distributed-systems` `two-phase-commit` `2pc` `python` `tinydb` `banking` `xmlrpc` `fault-tolerance` `atomic-transactions`

---

## Features

- **Distributed Transaction Coordination:**
  - Implements the 2PC protocol to coordinate transactions across multiple nodes (debit and credit).
  - Ensures atomic commit or abort of transactions, even in the presence of failures.
- **Banking Operations:**
  - Supports credit and debit operations between accounts.
  - Validates account existence and sufficient balance before processing.
- **Fault Tolerance:**
  - Simulates various failure scenarios (coordinator/participant crash, network delays, etc.).
  - Handles recovery and ensures data consistency after failures.
- **Account Management:**
  - Account creation and initialization using TinyDB.
  - Persistent storage of account balances and transaction logs.
- **Logging and Auditing:**
  - Logs all transaction requests and outcomes for auditability.
  - Maintains transaction and bank operation logs in JSON format.
- **Command-Line Client:**
  - Interactive CLI for initiating transactions and testing fault scenarios.
  - User-friendly menus for normal and fault-tolerance operations.
- **Locking Mechanism:**
  - Timer-based locks to prevent concurrent conflicting operations during transaction phases.
- **Extensible Design:**
  - Modular Python classes for coordinator, debit node, credit node, and client.
  - Easy to extend for more nodes or additional features.

---

## Tech Stack

- **Language:** Python 3.x
- **Database:** TinyDB (file-based NoSQL)
- **Communication:** XML-RPC (built-in Python modules)
- **Data Storage:** JSON files (`accounts.json`, `transaction_logs.json`, `bank_transactions.json`)
- **Other:** Standard Python libraries (`datetime`, `time`, `os`)

---

## System Design

Two-phase commit (2PC) is a distributed transaction protocol that ensures data consistency and integrity across multiple nodes in a distributed system. It's a type of atomic commitment protocol (ACP) that coordinates and synchronizes transactions across databases. The protocol consists of two phases:

### Phase 1 (Prepare Phase)
- The initiating node requests all participating nodes to promise to either commit or abort the transaction
- Ensures all resource managers have saved transaction updates to stable storage

### Phase 2 (Commit Phase)
- Coordinator sends commit message to all participants after receiving "YES" votes
- Transaction status is updated to "Prepared"
- Final status becomes "Committed" after receiving acknowledgments
- If any "NO" votes received, coordinator sends "ABORT" message

### Key Assumptions
- Timeout: 5 seconds (optimized for Python execution time)
- Locking implemented with timer-based mechanism
- Failures simulated using sleep statements
- System designed as bank transaction process with credit/debit operations

---

## Components

1. **Client**:
   - Initiates transactions
   - Interacts with transaction coordinator
   - Executes operations and awaits final decisions
   - Provides CLI for normal and fault-tolerance scenarios

2. **Transaction Coordinator (TC):**
   - Manages entire transaction process
   - Ensures participant agreement
   - Handles prepare and commit phases
   - Logs all transaction steps

3. **Debit Node:**
   - Handles debit operations
   - Manages account locking
   - Processes prepare and commit requests
   - Validates account and balance

4. **Credit Node:**
   - Manages credit operations
   - Processes prepare and commit requests
   - Validates account

---

## Implementation Notes

- **Account Initialization:**
  - Run `create_account_db.py` to initialize `accounts.json` with sample accounts:
    - Example:
      ```json
      {"AccountID": 1, "AccountName": "John Doe", "AccountBalance": 1000.0}
      ```
- **Transaction Logging:**
  - All transaction requests and their status are logged in `transaction_logs.json` and `bank_transactions.json`.
- **Locking:**
  - Both debit and credit nodes implement a 5-second timer-based lock to simulate resource locking during the prepare phase.
- **Failure Simulation:**
  - Fault scenarios are triggered via the client menu, using status flags to simulate coordinator/participant failures and recovery.
- **Extensibility:**
  - The system can be extended to more nodes or more complex transaction types by following the modular class structure.

---

## Deployment Notes

1. **Install Dependencies:**
   ```bash
   pip install tinydb
   ```
2. **Initialize Accounts Database:**
   ```bash
   python create_account_db.py
   ```
3. **Start Services (in separate terminals):**
   - Transaction Coordinator:
     ```bash
     python Transaction_coordinator.py
     ```
   - Debit Node:
     ```bash
     python debit_node.py
     ```
   - Credit Node:
     ```bash
     python credit_node.py
     ```
4. **Run Client:**
   ```bash
   python Client.py
   ```
5. **Testing Fault Tolerance:**
   - Use the client menu to trigger and observe various failure and recovery scenarios.

---

## Fault Tolerance Scenarios

### Part 1 & 3: Transaction Coordinator Failures
1. **TC fails before PREPARE message**
   - Outcome: Aborted
   - Nodes receive no PREPARE message
   - Nodes respond "NO" after TC recovery
2. **TC fails after partial COMMIT**
   - Outcome: Committed
   - TC sends COMMIT to one node, fails
   - Transaction completes after TC recovery

### Part 2 & 4: Participant Node Failures
3. **Both nodes reject PREPARE**
   - Outcome: Aborted
   - TC sends ABORT message
4. **Single node rejects PREPARE**
   - Outcome: Aborted
   - TC sends ABORT message
5. **Node fails after YES to PREPARE**
   - Outcome: Committed
   - TC proceeds with commit

---

## Additional Scenarios

- **Invalid Account:**
  - Non-existent accounts: Nodes send "NO" during prepare
- **Insufficient Balance:**
  - Debit node sends "NO" during prepare

---

## Learning Outcomes

- Understanding of Distributed Transactional Systems and ACID properties
- Implementation of 2PC protocol and fault tolerance
- XMLRPC usage in distributed systems
- Debugging and troubleshooting distributed applications
- Command-line interface development

---

## Challenges Faced

1. 2PC Implementation Complexity
2. Fault Tolerance Implementation
3. Locking Mechanism Design
4. Transaction Storage Solutions
5. Debugging and Synchronization

---

## Files

- `create_account_db.py`: Account creation implementation
- `Transaction_coordinator.py`: TC implementation
- `debit_node.py`: Debit node implementation
- `credit_node.py`: Credit node implementation
- `Client.py`: User interface
- `accounts.json`: Account data storage
- `transaction_logs.json`: Transaction logging
- `bank_transactions.json`: Transaction history

---

## References

- [Remote Procedural Call via XML-RPC in 5 minutes](https://youtu.be/_8xXrFWcWao?si=3NxoW9VxSmdVO6hT) by Live Python
- [Distributed Transactions: Two-Phase Commit Protocol](https://youtu.be/7FgU1D4EnpQ?si=akO9ZFxujLOu03sY) by Arpit Bhayani

---

## Notes

- Run create_account_db.py before other services
- Ensure all services are running before client operation
- System uses TinyDB for file-based database operations
