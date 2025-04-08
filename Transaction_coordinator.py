import xmlrpc.server
import xmlrpc.client
from tinydb import TinyDB, Query
import time
import os

class TransactionCoordinator:
    def __init__(self):
        self.credit_url = 'http://localhost:50002'
        self.debit_url = 'http://localhost:50001'
        self.participants = [self.debit_url, self.credit_url]
        self.db = TinyDB('transaction_logs.json')
        self.bank_db = TinyDB('bank_transactions.json')
        self.transactions = {}
            
    def initiate_transaction(self, request):
        txn_id = request['transaction_id']
        status_flag = request['request_status']
        # Clear the transaction logs before starting a new transaction
        self.clear_logs()
        self.transactions[txn_id] = {'prepare_debit': None, 'prepare_credit': None, 'commit_debit': None, 'commit_credit': None}
        self.log_request(request)
        print(f"\nCoordinator received transaction request: {request}\n")
        # Clear the transaction logs before starting a new transaction
        self.lock_servers()
        return self.process_transaction(txn_id, request, status_flag)

    def process_transaction(self, txn_id, request, status_flag):
        # Testcase 0: Base case
        # Testcase 3, Testcase 4, Testcase 5 are node failures, implemented at node servers
        if status_flag in {'0', '3', '4', '5'}:
            debit_prepare_response = self.send_prepare(self.debit_url, request)
            credit_prepare_response = self.send_prepare(self.credit_url, request)
    
            # Log the responses
            self.transactions[txn_id]['prepare_debit'] = debit_prepare_response
            self.transactions[txn_id]['prepare_credit'] = credit_prepare_response

            # Save the preliminary logs
            self.save_logs(txn_id)

            # Check the latest logs from TinyDB
            transaction_log = self.db.get(Query().transaction_id == txn_id)

            if transaction_log and transaction_log['prepare_debit'] == 'YES' and transaction_log['prepare_credit'] == 'YES':
                self.transactions[txn_id]['status'] = 'prepared'
                self.save_logs(txn_id)
                print("\nTransaction is prepared")                
                debit_commit_response = self.send_commit(self.debit_url, request)
                credit_commit_response = self.send_commit(self.credit_url, request)
                self.transactions[txn_id]['commit_debit'] = debit_commit_response
                self.transactions[txn_id]['commit_credit'] = credit_commit_response
                self.save_logs(txn_id)
                self.transactions[txn_id]['status'] = 'committed'
                self.save_logs(txn_id)
                print("\nTransaction is committed")
                return 'Transaction is committed'
            else:
                debit_abort_response = self.send_abort(self.debit_url, txn_id)
                credit_abort_response = self.send_abort(self.credit_url, txn_id)
                self.transactions[txn_id]['commit_debit'] = debit_abort_response
                self.transactions[txn_id]['commit_credit'] = credit_abort_response
                self.save_logs(txn_id)
                self.transactions[txn_id]['status'] = 'aborted'
                self.save_logs(txn_id)
                print("\nTransaction is aborted")
                return 'Transaction is aborted'

        # Testcase 1: TC fails before sending PREPARE message 
        if status_flag == '1':
            print(f'\nTestcase {status_flag} : TC fails before sending PREPARE message')
            print(f'\nTransaction Coordinator failing before sending PREPARE message')
            time.sleep(6)
            print(f'\nTransaction Coordinator restarting after Timeout')
            debit_prepare_response = self.send_prepare(self.debit_url, request)
            credit_prepare_response = self.send_prepare(self.credit_url, request)
            # Log the responses
            self.transactions[txn_id]['prepare_debit'] = debit_prepare_response
            self.transactions[txn_id]['prepare_credit'] = credit_prepare_response

            # Save the preliminary logs
            self.save_logs(txn_id)

            # Check the latest logs from TinyDB
            transaction_log = self.db.get(Query().transaction_id == txn_id)

            if transaction_log and transaction_log['prepare_debit'] == 'YES' and transaction_log['prepare_credit'] == 'YES':
                self.transactions[txn_id]['status'] = 'prepared'
                self.save_logs(txn_id)
                print("\nTransaction is prepared")                
                debit_commit_response = self.send_commit(self.debit_url, request)
                credit_commit_response = self.send_commit(self.credit_url, request)
                self.transactions[txn_id]['commit_debit'] = debit_commit_response
                self.transactions[txn_id]['commit_credit'] = credit_commit_response
                self.save_logs(txn_id)
                self.transactions[txn_id]['status'] = 'committed'
                self.save_logs(txn_id)
                print("\nTransaction is committed")
                return 'Transaction is committed'
            else:
                debit_abort_response = self.send_abort(self.debit_url, txn_id)
                credit_abort_response = self.send_abort(self.credit_url, txn_id)
                self.transactions[txn_id]['commit_debit'] = debit_abort_response
                self.transactions[txn_id]['commit_credit'] = credit_abort_response
                self.save_logs(txn_id)
                self.transactions[txn_id]['status'] = 'aborted'
                self.save_logs(txn_id)
                print("\nTransaction is aborted")
                return 'Transaction is aborted'

        # Testcase 2: TC fails after sending COMMIT message to debit node
        if status_flag == '2':
            debit_prepare_response = self.send_prepare(self.debit_url, request)
            credit_prepare_response = self.send_prepare(self.credit_url, request)
    
            # Log the responses
            self.transactions[txn_id]['prepare_debit'] = debit_prepare_response
            self.transactions[txn_id]['prepare_credit'] = credit_prepare_response

            # Save the preliminary logs
            self.save_logs(txn_id)

            # Check the latest logs from TinyDB
            transaction_log = self.db.get(Query().transaction_id == txn_id)

            if transaction_log and transaction_log['prepare_debit'] == 'YES' and transaction_log['prepare_credit'] == 'YES':
                self.transactions[txn_id]['status'] = 'prepared'
                self.save_logs(txn_id)
                print("\nTransaction is prepared")                
                debit_commit_response = self.send_commit(self.debit_url, request)
                print(f'\nTestcase {status_flag} : TC fails after sending one COMMIT message')
                time.sleep(6)
                print(f'\nTransaction Coordinator restarting after Timeout')
                credit_commit_response = self.send_commit(self.credit_url, request)
                self.transactions[txn_id]['commit_debit'] = debit_commit_response
                self.transactions[txn_id]['commit_credit'] = credit_commit_response
                self.save_logs(txn_id)
                self.transactions[txn_id]['status'] = 'committed'
                self.save_logs(txn_id)
                print("\nTransaction is committed")
                return 'Transaction is committed'
            else:
                debit_abort_response = self.send_abort(self.debit_url, txn_id)
                credit_abort_response = self.send_abort(self.credit_url, txn_id)
                self.transactions[txn_id]['commit_debit'] = debit_abort_response
                self.transactions[txn_id]['commit_credit'] = credit_abort_response
                self.save_logs(txn_id)
                self.transactions[txn_id]['status'] = 'aborted'
                self.save_logs(txn_id)
                print("\nTransaction is aborted")
                return 'Transaction is aborted'

    def clear_logs(self):
        self.db.truncate()

    def lock_servers(self):
        for url in self.participants:
            self.send_lock(url)

    def send_lock(self, url):
        with xmlrpc.client.ServerProxy(url) as proxy:
            print("\nLocking the participant nodes for PREPARE")
            response = proxy.lock()

    def send_prepare(self, url, request):
        with xmlrpc.client.ServerProxy(url) as proxy:
            print("\nSending PREPARE message")
            return proxy.prepare(request)

    def send_commit(self, url, request):
        with xmlrpc.client.ServerProxy(url) as proxy:
            print("\nSending COMMIT message")
            return proxy.commit(request)

    def send_abort(self, url, txn_id):
        with xmlrpc.client.ServerProxy(url) as proxy:
           print("\nSending ABORT message")
           return proxy.abort(txn_id)
        
    def log_request(self, request):
        # Log the transaction request into bank_transactions.json
        self.bank_db.insert(request)

    def save_logs(self, txn_id):
        # Insert or update the transaction log in TinyDB
        Transaction = Query()
        existing_log = self.db.get(Transaction.transaction_id == txn_id)
        if existing_log:
            # Update the existing document with new data
            self.db.update(self.transactions[txn_id], Transaction.transaction_id == txn_id)
        else:
            # Insert a new document with the transaction data
            self.db.insert(self.transactions[txn_id])

    def start(self):
        server = xmlrpc.server.SimpleXMLRPCServer(('localhost', 50000), logRequests=False)
        server.register_instance(self)
        print("Coordinator listening on port 50000\n")
        server.serve_forever()

if __name__ == "__main__":
    try:
        coordinator = TransactionCoordinator()
        coordinator.start()
    except KeyboardInterrupt:
        print("Exiting.....")
