# bank.py
from account import Account
from storage import save_accounts_to_file, load_accounts_from_file
import transactions as txn
from typing import List, Optional
import itertools
import datetime
import csv

DEFAULT_START_ACC = 1001
MAX_SINGLE_DEPOSIT = 100000.0
DAILY_WITHDRAW_LIMIT = 50000.0

class Bank:
    def __init__(self, accounts_file="accounts.csv"):
        self.accounts_file = accounts_file
        self.accounts: List[Account] = load_accounts_from_file(accounts_file)
        self._acc_gen = self._init_acc_generator()
        # Validate next account number generator based on existing
        self._ensure_seq()

    def _init_acc_generator(self):
        # generator starting at DEFAULT_START_ACC
        n = DEFAULT_START_ACC
        while True:
            yield n
            n += 1

    def _ensure_seq(self):
        if self.accounts:
            max_existing = max(a.account_number for a in self.accounts)
            # advance generator to max_existing + 1
            g = self._init_acc_generator()
            # consume until > max_existing
            while True:
                val = next(g)
                if val > max_existing:
                    self._acc_gen = itertools.chain([val], g)
                    break

    def next_account_number(self):
        # get next number from generator
        if isinstance(self._acc_gen, itertools.chain):
            return next(self._acc_gen)
        return next(self._acc_gen)

    # ---------- Base features ----------
    def create_account(self, name: str, age: int, acc_type: str, initial_deposit: float, pin: Optional[int]=None):
        # F19: Age verification
        if age < 18:
            raise ValueError("Age must be 18 or older to create an account.")
        acc_type = acc_type.capitalize()
        if acc_type not in ("Savings", "Current"):
            raise ValueError("Account type must be 'Savings' or 'Current'.")

        # minimum deposit rules
        if acc_type == "Savings" and initial_deposit < 500:
            raise ValueError("Savings account requires at least ₹500 initial deposit.")
        if acc_type == "Current" and initial_deposit < 1000:
            raise ValueError("Current account requires at least ₹1,000 initial deposit.")

        acc_num = self.next_account_number()
        account = Account(
            account_number=acc_num,
            name=name,
            age=age,
            balance=float(initial_deposit),
            account_type=acc_type,
            status="Active",
            pin=pin
        )
        self.accounts.append(account)
        txn.log_transaction(acc_num, "Create", initial_deposit, account.balance)
        return account

    def find_by_account_number(self, account_number: int) -> Optional[Account]:
        for acc in self.accounts:
            if acc.account_number == account_number:
                return acc
        return None

    def find_by_name(self, name: str):
        name_lower = name.strip().lower()
        return [a for a in self.accounts if name_lower in a.name.strip().lower()]

    def deposit(self, account_number: int, amount: float):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        if amount > MAX_SINGLE_DEPOSIT:
            raise ValueError(f"Cannot deposit more than ₹{MAX_SINGLE_DEPOSIT} in a single deposit.")
        acc = self.find_by_account_number(account_number)
        if not acc:
            raise LookupError("Account not found.")
        if acc.status != "Active":
            raise PermissionError("Cannot deposit into inactive account.")
        acc.balance += amount
        txn.log_transaction(account_number, "Deposit", amount, acc.balance)
        return acc.balance

    def withdraw(self, account_number: int, amount: float):
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        acc = self.find_by_account_number(account_number)
        if not acc:
            raise LookupError("Account not found.")
        if acc.status != "Active":
            raise PermissionError("Account is inactive.")
        # check daily limit
        today_total = txn.todays_withdrawals_total(account_number)
        if today_total + amount > DAILY_WITHDRAW_LIMIT:
            raise PermissionError(f"Daily withdrawal limit of ₹{DAILY_WITHDRAW_LIMIT} exceeded for today. Already withdrawn ₹{today_total:.2f}.")
        # minimum balance check
        min_remain = 500.0 if acc.account_type == "Savings" else 1000.0
        if acc.balance - amount < min_remain:
            raise PermissionError(f"Cannot withdraw. Account must maintain minimum balance of ₹{min_remain}")
        acc.balance -= amount
        txn.log_transaction(account_number, "Withdraw", amount, acc.balance)
        return acc.balance

    def balance_inquiry(self, account_number: int):
        acc = self.find_by_account_number(account_number)
        if not acc:
            raise LookupError("Account not found.")
        return acc

    def close_account(self, account_number: int):
        acc = self.find_by_account_number(account_number)
        if not acc:
            raise LookupError("Account not found.")
        if acc.status != "Active":
            raise PermissionError("Account already inactive.")
        acc.status = "Inactive"
        txn.log_transaction(account_number, "Close", 0.0, acc.balance)
        return acc

    # ---------- Extended features ----------
    def list_active_accounts(self):
        return [a for a in self.accounts if a.status == "Active"]

    def list_closed_accounts(self):
        return [a for a in self.accounts if a.status != "Active"]

    def reopen_account(self, account_number: int):
        acc = self.find_by_account_number(account_number)
        if not acc:
            raise LookupError("Account not found.")
        if acc.status == "Active":
            raise PermissionError("Account is already active.")
        acc.status = "Active"
        txn.log_transaction(account_number, "Reopen", 0.0, acc.balance)
        return acc

    def rename_account_holder(self, account_number: int, new_name: str):
        acc = self.find_by_account_number(account_number)
        if not acc:
            raise LookupError("Account not found.")
        acc.name = new_name
        txn.log_transaction(account_number, "Rename", 0.0, acc.balance)
        return acc

    def count_active_accounts(self):
        return len(self.list_active_accounts())

    def delete_all_accounts(self, admin_confirm=False):
        if not admin_confirm:
            raise PermissionError("Admin confirmation required to delete all accounts.")
        self.accounts.clear()
        # also truncate transactions log
        open(txn.LOGFILE, "w").close()
        # save empty accounts.csv
        save_accounts_to_file(self.accounts, filename=self.accounts_file)
        return True

    def transfer_funds(self, from_acc_num: int, to_acc_num: int, amount: float):
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        from_acc = self.find_by_account_number(from_acc_num)
        to_acc = self.find_by_account_number(to_acc_num)
        if not from_acc or not to_acc:
            raise LookupError("One or both accounts not found.")
        if from_acc.status != "Active" or to_acc.status != "Active":
            raise PermissionError("Both accounts must be active for transfer.")
        # min balance check for sender
        min_remain = 500.0 if from_acc.account_type == "Savings" else 1000.0
        if from_acc.balance - amount < min_remain:
            raise PermissionError("Sender does not have sufficient funds respecting minimum balance.")
        # daily limit check for withdrawals (transfer counts as debit)
        today_total = txn.todays_withdrawals_total(from_acc_num)
        if today_total + amount > DAILY_WITHDRAW_LIMIT:
            raise PermissionError("Daily withdrawal/transfer limit exceeded.")
        from_acc.balance -= amount
        to_acc.balance += amount
        txn.log_transaction(from_acc_num, "Transfer-Debit", amount, from_acc.balance)
        txn.log_transaction(to_acc_num, "Transfer-Credit", amount, to_acc.balance)
        return from_acc.balance, to_acc.balance

    def transaction_history(self, account_number: int):
        return txn.get_account_transactions(account_number)

    def minimum_balance_check(self, account_number: int):
        acc = self.find_by_account_number(account_number)
        if not acc:
            raise LookupError("Account not found.")
        return 500.0 if acc.account_type == "Savings" else 1000.0

    def simple_interest_calculator(self, account_number: int, rate_percent: float, years: float):
        acc = self.find_by_account_number(account_number)
        if not acc:
            raise LookupError("Account not found.")
        # Simple interest on current balance
        return acc.balance * (rate_percent/100.0) * years

    def average_balance(self):
        if not self.accounts:
            return 0.0
        return sum(a.balance for a in self.accounts) / len(self.accounts)

    def youngest_account_holder(self):
        if not self.accounts:
            return None
        return min(self.accounts, key=lambda a: a.age)

    def oldest_account_holder(self):
        if not self.accounts:
            return None
        return max(self.accounts, key=lambda a: a.age)

    def top_n_accounts_by_balance(self, n=5):
        return sorted(self.accounts, key=lambda a: a.balance, reverse=True)[:n]

    def set_pin(self, account_number: int, pin: int):
        acc = self.find_by_account_number(account_number)
        if not acc:
            raise LookupError("Account not found.")
        if not (1000 <= pin <= 9999):
            raise ValueError("PIN must be a 4 digit number.")
        acc.pin = pin
        txn.log_transaction(account_number, "Set-PIN", 0.0, acc.balance)
        return True

    def export_accounts_to_file(self, filename="export_accounts.csv"):
        save_accounts_to_file(self.accounts, filename)
        return filename

    def import_accounts_from_file(self, filename="accounts_import.csv"):
        # load CSV and append accounts (ensure unique account numbers)
        try:
            with open(filename, "r", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # basic validation
                    try:
                        name = row["name"].strip()
                        age = int(row["age"])
                        acc_type = row.get("type", "Savings")
                        balance = float(row.get("balance", 0.0))
                    except Exception:
                        continue
                    try:
                        # Note: imported accounts will be assigned new unique numbers to avoid duplicates
                        new_acc = self.create_account(name, age, acc_type, balance, pin=None)
                    except Exception:
                        # skip invalid rows
                        continue
            return True
        except FileNotFoundError:
            raise

    def autosave_and_exit(self):
        save_accounts_to_file(self.accounts, filename=self.accounts_file)
        print("Data saved to", self.accounts_file)
