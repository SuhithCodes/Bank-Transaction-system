# Import necessary modules
import xmlrpc.client  # For making XML-RPC calls to the server
from datetime import datetime  # For generating timestamps for transactions

# Define the URL for the XML-RPC server
Txn_crdt_url = 'http://localhost:50000'

# Create a proxy client to interact with the server
client_proxy = xmlrpc.client.ServerProxy

def send_request(request):
    with client_proxy(Txn_crdt_url) as proxy:
        response = proxy.initiate_transaction(request)
        print(f"\nClient received: {response}\n")

def get_user_input(status_flag):
    print("\nEnter transaction details:")
    return {
        'transaction_id': datetime.now().strftime('%Y%m%d%H%M%S'),  # Generate a unique transaction ID based on the current timestamp
        'amount': float(input("  Amount: ")),  # Amount for the transaction
        'from_account': input("  From Account: "),  # Source account
        'to_account': input("  To Account: "),  # Destination account
        'request_status': status_flag  # Status of the request
    }


def faulty_menu():
    print("\nTesting Fault Tolerance:")
    print("1. TC fails before sending PREPARE message")
    print("2. Send COMMIT to one Node and fail")
    print("3. Both Nodes send 'NO' to PREPARE")
    print("4. One Node sends 'NO' to PREPARE")
    print("5. Node fails after sending 'YES' to 'PREPARE'")
    print("6. Exit\n")

def show_menu():
    print("\nMenu:")
    print("1. Initiate a new transaction")
    print("2. Test Fault tolerance")
    print("3. Exit")

def main():
    while True:
        show_menu()
        choice = input("Enter your choice: ")
        if choice == '1':
            # Initiate a new transaction
            request = get_user_input('0')
            send_request(request)
        elif choice == '2':
            # Test fault tolerance scenarios
            while True:
                print("Fault Tolerance")
                faulty_menu()
                f_choice = input("Enter your option for fault tolerance scenario: ")
                if f_choice != '6':
                    # Get user input for the selected fault tolerance scenario
                    f_request = get_user_input(f_choice)
                    send_request(f_request)
                elif f_choice == '6':
                    # Exit fault tolerance testing
                    print("Exiting...")
                    break
                else:
                    # Handle invalid choices
                    print("Invalid choice, please select again.")
        elif choice == '3':
            # Exit the program
            print("Exiting...")
            break
        else:
            # Handle invalid choices
            print("Invalid choice, please select again.")

if __name__ == "__main__":
    main()
