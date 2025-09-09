# storage.py
import csv
from account import Account
from typing import List

FIELDNAMES = ["account_number", "name", "age", "balance", "type", "status", "pin"]

def save_accounts_to_file(accounts: List[Account], filename="accounts.csv"):
    if not accounts:
        # create empty CSV with header
        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
        return
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for acc in accounts:
            writer.writerow(acc.to_dict())

def load_accounts_from_file(filename="accounts.csv"):
    accounts = []
    try:
        with open(filename, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # skip empty lines
                if not row.get("account_number"):
                    continue
                accounts.append(Account.from_dict(row))
    except FileNotFoundError:
        # return empty list
        pass
    return accounts
