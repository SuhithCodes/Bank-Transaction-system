import xmlrpc.server
from datetime import datetime, timedelta
from tinydb import TinyDB, Query
import time

# Global variables to hold the start and end time of the lock period
start_time = None
end_time = None

# Initialize TinyDB and specify the database file
account_db = TinyDB('accounts.json')

class CreditNode:
    def __init__(self, name):
        self.name = name
        self.transactions = {}
        self.db = TinyDB('transaction_logs.json')  # Initialize TinyDB database

    def lock(self):
        global start_time, end_time
        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=5)
        print(f"\nLock received. Timer started at {start_time}. Will end at {end_time}.")
        return "Lock received"

    def is_account_valid(self, account_id):
        # Retrieve all accounts
        all_accounts = account_db.all()
        account_ids = [account['AccountID'] for account in all_accounts]    
        return account_id in account_ids

    def prepare(self, request):
        current_time = datetime.now()
        status_flag = request.get('request_status')
        account_id = int(request.get('to_account'))
        global start_time, end_time
        txn_id = request.get('transaction_id')
        if not self.is_account_valid(account_id):
            print(f"\n{account_id} does not exist")
            return "NO"
        if not txn_id:
            print(f"\n{self.name} received prepare request without a transaction_id.")
            return False
        if status_flag == '3':
            print(f"\nTestcase 3: credit_node sending NO to Prepare")
            return False        
        if start_time is not None and end_time is not None and start_time <= current_time <= end_time:
            self.transactions[txn_id] = 'prepared'
            self.save_logs(txn_id, 'prepared')
            print(f"\nPrepare received within the lock period. Transaction ID: {txn_id}, Current time: {current_time}.")
            return "YES"
        else:
            print(f"\nPrepare received outside the lock period. Transaction ID: {txn_id}, Current time: {current_time}.")
            return "NO"
    
    def commit(self, request):
        current_time = datetime.now()
        account_id = int(request.get('to_account'))
        txn_id = request.get('transaction_id')
        amount_to_add = float(request.get('amount'))  # Assume the amount to add is provided in the request
        print(f"\nCommit received. Transaction ID: {txn_id}, Current time: {current_time}.")
        # Load transaction logs to verify the prepare status
        Transaction = Query()
        logs = self.db.search(Transaction.transaction_id == txn_id)
        # Check if the transaction was prepared
        for log in logs:
            if log['status'] == 'prepared':
                print(f"\nTransaction ID: {txn_id} committed successfully.")
                self.add_balance(account_id, amount_to_add)
                return 'YES'
        return 'NO'

    def add_balance(self, account_id, amount_to_add):
        print(f"Attempting to update balance for Account ID: {account_id} by {amount_to_add}")
        # Find the account by its ID
        Account = Query()
        account = account_db.search(Account.AccountID == account_id)
        if account:
            # Get the current balance
            current_balance = account[0]['AccountBalance']
            new_balance = current_balance + amount_to_add
            print(f"Current balance: {current_balance}, New balance: {new_balance}")
            # Update the record in the database
            account_db.update({'AccountBalance': new_balance}, Account.AccountID == account_id)
            print(f"Balance updated successfully for Account ID: {account_id}")
        else:
            print(f"Account ID {account_id} not found.")


    def abort(self, txn_id):
        # Process abort logic here
        current_time = datetime.now()
        print(f"\nAbort received. Transaction ID: {txn_id}, Current time: {current_time}.")
        return 'NO'

    def save_logs(self, txn_id, status):
        # Update or insert the transaction status in TinyDB
        Transaction = Query()
        self.db.upsert({'transaction_id': txn_id, 'status': status}, Transaction.transaction_id == txn_id)

    def start(self):
        server = xmlrpc.server.SimpleXMLRPCServer(('localhost', 50002), logRequests=False)
        server.register_instance(self)
        print("\nCreditNode listening on port 50002")
        server.serve_forever()

if __name__ == "__main__":
    try:
        credit_node = CreditNode("Node2")
        credit_node.start()
    except KeyboardInterrupt:
        print("Exiting.....")
