# transactions.py
import datetime
import os

LOGFILE = "transactions.log"

def log_transaction(account_number, operation, amount, balance_after):
    timestamp = datetime.datetime.now().isoformat(sep=" ", timespec="seconds")
    entry = f"{timestamp},{account_number},{operation},{amount:.2f},{balance_after:.2f}\n"
    with open(LOGFILE, "a") as f:
        f.write(entry)

def read_transactions():
    if not os.path.exists(LOGFILE):
        return []
    with open(LOGFILE, "r") as f:
        lines = [l.strip() for l in f if l.strip()]
    # parse into tuple: (timestamp, account_number, operation, amount, balance_after)
    parsed = []
    for line in lines:
        parts = line.split(",")
        if len(parts) < 5:
            continue
        timestamp, acc_num, operation, amount, balance = parts
        parsed.append({
            "timestamp": timestamp,
            "account_number": int(acc_num),
            "operation": operation,
            "amount": float(amount),
            "balance_after": float(balance)
        })
    return parsed

def get_account_transactions(account_number):
    all_tx = read_transactions()
    return [t for t in all_tx if t["account_number"] == int(account_number)]

def todays_withdrawals_total(account_number):
    import datetime
    today = datetime.date.today().isoformat()
    txs = get_account_transactions(account_number)
    total = 0.0
    for t in txs:
        if t["operation"].lower() in ("withdraw", "transfer-debit"):
            if t["timestamp"].split(" ")[0] == today:
                total += t["amount"]
    return total
