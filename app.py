import streamlit as st
import‘pysqlite3’
import sys
sys.modules[‘sqlite3’] = sys.modules.pop(‘pysqlite3’)
# Connect to the database
conn = sqlite3.connect('banking.db')
c = conn.cursor()

# Create accounts table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS accounts
             (id INTEGER PRIMARY KEY AUTOINCREMENT, account_type TEXT, customer_name TEXT, balance REAL)''')

# Create transactions table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS transactions
             (id INTEGER PRIMARY KEY AUTOINCREMENT, account_id INTEGER, transaction_type TEXT, amount REAL)''')

# Function to create a new account
def create_account(account_type, customer_name):
    c.execute("INSERT INTO accounts (account_type, customer_name, balance) VALUES (?, ?, 0.0)", (account_type, customer_name))
    conn.commit()
    st.success("Account created successfully.")

# Function to display all created accounts
def list_accounts():
    c.execute("SELECT * FROM accounts")
    accounts = c.fetchall()

    if not accounts:
        st.info("No accounts found.")
    else:
        for account in accounts:
            st.write(f"Account ID: {account[0]}, Account Type: {account[1]}, Customer Name: {account[2]}, Balance: {account[3]}")

# Function to create a transaction
def create_transaction(account_id, transaction_type, amount):
    c.execute("INSERT INTO transactions (account_id, transaction_type, amount) VALUES (?, ?, ?)", (account_id, transaction_type, amount))
    conn.commit()
    st.success("Transaction created successfully.")

# Function to display all transactions
def list_transactions():
    c.execute('''SELECT transactions.id, accounts.account_type, accounts.customer_name, transactions.transaction_type, transactions.amount
                 FROM transactions
                 INNER JOIN accounts ON transactions.account_id = accounts.id''')
    transactions = c.fetchall()

    if not transactions:
        st.info("No transactions found.")
    else:
        for transaction in transactions:
            st.write(f"Transaction ID: {transaction[0]}, Account Type: {transaction[1]}, Customer Name: {transaction[2]}, Transaction Type: {transaction[3]}, Amount: {transaction[4]}")

# Function to search transactions by account ID or customer name
def search_transactions(search_key):
    c.execute('''SELECT transactions.id, accounts.account_type, accounts.customer_name, transactions.transaction_type, transactions.amount
                 FROM transactions
                 INNER JOIN accounts ON transactions.account_id = accounts.id
                 WHERE accounts.customer_name LIKE ? OR accounts.id = ?''', (f"%{search_key}%", search_key))
    transactions = c.fetchall()

    if not transactions:
        st.info("No transactions found.")
    else:
        for transaction in transactions:
            st.write(f"Transaction ID: {transaction[0]}, Account Type: {transaction[1]}, Customer Name: {transaction[2]}, Transaction Type: {transaction[3]}, Amount: {transaction[4]}")

# Function to retrieve top 5 customers with the highest account balances
def retrieve_top_customers():
    c.execute("SELECT customer_name, balance FROM accounts ORDER BY balance DESC LIMIT 5")
    top_customers = c.fetchall()

    if not top_customers:
        st.info("No customers found.")
    else:
        for customer in top_customers:
            st.write(f"Customer Name: {customer[0]}, Balance: {customer[1]}")

# Streamlit app
def main():
    st.title("Banking Application")

    # Sidebar
    menu = ["Create Account", "List Accounts", "Create Transaction", "List Transactions", "Search Transactions", "Top Customers"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Create Account":
        st.subheader("Create a New Account")
        account_type = st.selectbox("Account Type", ["Current", "Savings", "KYC Lite"])
        customer_name = st.text_input("Customer Name")
        if st.button("Create"):
            create_account(account_type, customer_name)

    elif choice == "List Accounts":
        st.subheader("List of Created Accounts")
        list_accounts()

    elif choice == "Create Transaction":
        st.subheader("Create a New Transaction")
        account_id = st.number_input("Account ID")
        transaction_type = st.selectbox("Transaction Type", ["Deposit", "Withdraw"])
        amount = st.number_input("Amount")
        if st.button("Create"):
            create_transaction(account_id, transaction_type, amount)

    elif choice == "List Transactions":
        st.subheader("List of Transactions")
        list_transactions()

    elif choice == "Search Transactions":
        st.subheader("Search Transactions")
        search_key = st.text_input("Search by Account ID or Customer Name")
        if st.button("Search"):
            search_transactions(search_key)

    elif choice == "Top Customers":
        st.subheader("Top Customers")
        retrieve_top_customers()

T
