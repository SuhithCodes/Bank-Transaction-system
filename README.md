# Two-Phase Distributed Commit System (2PC)

# CSE5306 Distributed Systems - Project 2

This project implements a distributed transaction coordinator system using XML-RPC for communication between a transaction coordinator and debit/credit nodes. The system ensures that transactions are processed consistently across multiple nodes with fault tolerance using the Two-Phase Commit (2PC) protocol.

## Academic Integrity Statement

I have neither given nor received unauthorized assistance with this work. I will not post the project description and the solution online.

**Contributors:**

- SWETA SANDHYA NAYAK (1002127265) - Date: 24TH JUNE, 2024
- SUHITH GHANATHAY (1002170591) - Date: 24TH JUNE, 2024

## Table of Contents

1. [System Design](#system-design)
2. [2PC System Implementation](#2pc-system-implementation)
3. [Components](#components)
4. [Setup Instructions](#setup-instructions)
5. [Fault Tolerance Scenarios](#fault-tolerance-scenarios)
6. [Additional Scenarios](#additional-scenarios)
7. [Learning Outcomes](#learning-outcomes)
8. [Team Contributions](#team-contributions)
9. [Challenges Faced](#challenges-faced)
10. [Files](#files)
11. [References](#references)

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

## Components

1. **Client**:

   - Initiates transactions
   - Interacts with transaction coordinator
   - Executes operations and awaits final decisions

2. **Transaction Coordinator (TC)**:

   - Manages entire transaction process
   - Ensures participant agreement
   - Handles prepare and commit phases

3. **Debit Node**:

   - Handles debit operations
   - Manages account locking
   - Processes prepare and commit requests

4. **Credit Node**:
   - Manages credit operations
   - Processes prepare and commit requests

## Setup Instructions

### Prerequisites

```bash
pip install tinydb
```

### Starting the System

1. Create Account Database:

   ```bash
   python create_account_db.py
   ```

2. Start Transaction Coordinator:

   ```bash
   python transaction_coordinator.py
   ```

3. Start Debit Node:

   ```bash
   python debit_node.py
   ```

4. Start Credit Node:

   ```bash
   python credit_node.py
   ```

5. Run Client:
   ```bash
   python client.py
   ```

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

## Additional Scenarios

1. **Invalid Account Scenarios**
   - Non-existent accounts: Nodes send "NO" during prepare
   - Insufficient balance: Debit node sends "NO" during prepare

## Learning Outcomes

- Understanding of Distributed Transactional Systems and ACID properties
- Implementation of 2PC protocol and fault tolerance
- XMLRPC usage in distributed systems
- Debugging and troubleshooting distributed applications
- Command-line interface development

## Team Contributions

**Suhith Ghanathay:**

- System design
- Base 2PC implementation
- Locking mechanism
- TC fault tolerance
- Bank transaction logic
- Test scenarios
- Report review

**Sweta Sandhya Nayak:**

- Account database setup
- Node fault tolerance
- TinyDB integration
- Test scenarios
- Documentation and reporting

## Challenges Faced

1. 2PC Implementation Complexity
2. Fault Tolerance Implementation
3. Locking Mechanism Design
4. Transaction Storage Solutions
5. Debugging and Synchronization

## Files

- `create_account_db.py`: Account creation implementation
- `transaction_coordinator.py`: TC implementation
- `debit_node.py`: Debit node implementation
- `credit_node.py`: Credit node implementation
- `client.py`: User interface
- `accounts.json`: Account data storage
- `transaction_logs.json`: Transaction logging
- `bank_transaction.json`: Transaction history

## References

- [Remote Procedural Call via XML-RPC in 5 minutes](https://youtu.be/_8xXrFWcWao?si=3NxoW9VxSmdVO6hT) by Live Python
- [Distributed Transactions: Two-Phase Commit Protocol](https://youtu.be/7FgU1D4EnpQ?si=akO9ZFxujLOu03sY) by Arpit Bhayani

## Notes

- Run create_account_db.py before other services
- Ensure all services are running before client operation
- System uses TinyDB for file-based database operations
