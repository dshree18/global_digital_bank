# global_digital_bank
# Global Digital Bank (GDB) - CLI App

This is a Python CLI banking system implementing the project docket features.

## Requirements
- Python 3.8+
- No external libraries required (uses stdlib)

## Files
- `main.py` — CLI entrypoint
- `bank.py` — core business logic (features B1–B6 and F1–F24)
- `account.py` — Account class
- `storage.py` — load/save accounts to `accounts.csv`
- `transactions.py` — writes `transactions.log`
- `utils.py` — input helpers
- `accounts.csv` — persisted account data (auto-created if missing)
- `transactions.log` — transaction log (auto-created)

## Run
1. Place all files in a folder.
2. (Optional) create a sample `accounts_import.csv` if you want to test import.
3. Run:
```bash
python main.py
