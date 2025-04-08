from tinydb import TinyDB, Query

# Initialize TinyDB and create the database file
db = TinyDB('accounts.json')

# Data to insert
data = [
    {'AccountID': 1, 'AccountName': 'John Doe', 'AccountBalance': 1000.00},
    {'AccountID': 2, 'AccountName': 'Jane Smith', 'AccountBalance': 1500.00},
    {'AccountID': 3, 'AccountName': 'Alice Johnson', 'AccountBalance': 1200.00}
]

# Insert data into the database
db.insert_multiple(data)

print("Data has been added to accounts.json")
