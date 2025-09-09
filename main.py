# main.py
from bank import Bank
from utils import prompt_int, prompt_float
import sys

def print_account_basic(acc):
    print(f"Account #{acc.account_number} | Name: {acc.name} | Age: {acc.age} | Type: {acc.account_type} | Balance: ₹{acc.balance:.2f} | Status: {acc.status}")

def main():
    bank = Bank()
    print("--- Welcome to Global Digital Bank ---")
    while True:
        print("\nMenu:")
        print("1) Create Account")
        print("2) Deposit")
        print("3) Withdraw")
        print("4) Balance Inquiry")
        print("5) Close Account")
        print("6) List All Active Accounts")
        print("7) Transfer Funds")
        print("8) Transaction History")
        print("9) Set PIN for Account")
        print("10) Import Accounts from File (accounts_import.csv)")
        print("11) Export Accounts to export_accounts.csv")
        print("12) Rename Account Holder")
        print("13) Reopen Closed Account")
        print("14) Count Active Accounts")
        print("15) Delete All Accounts (Admin)")
        print("16) Analytics: Top N Accounts by Balance")
        print("17) Analytics: Average Balance")
        print("18) Youngest & Oldest Account Holder")
        print("19) Simple Interest Calculator")
        print("20) Search by Name")
        print("21) Search by Account Number")
        print("22) List All Closed Accounts")
        print("23) System Exit with Autosave")
        print("24) Help / Show Menu")
        try:
            choice = prompt_int("Enter your choice: ", min_val=1, max_val=24)
            
            if choice == 1:
                # Your version of Create Account
                name = input("Enter name: ").strip()
                age = int(input("Enter age: ").strip())  # Ensure age is integer
                acc_type = input("Enter account type (Savings/Current): ").strip()
                initial = prompt_float("Enter initial deposit: ", min_val=0)
                pin_choice = input("Do you want to set a 4-digit PIN now? (y/n): ").strip().lower()
                pin = None
                if pin_choice == "y":
                    pin = prompt_int("Enter 4-digit PIN: ", min_val=1000, max_val=9999)
                try:
                    acc = bank.create_account(name, age, acc_type, initial, pin=pin)
                    print("Account created successfully!")
                    print_account_basic(acc)
                except Exception as e:
                    print("Error:", e)

            elif choice == 2:
                accnum = prompt_int("Enter account number: ")
                amt = prompt_float("Enter deposit amount: ", min_val=0.01)
                try:
                    newbal = bank.deposit(accnum, amt)
                    print(f"Deposit successful. New balance: ₹{newbal:.2f}")
                except Exception as e:
                    print("Error:", e)

            elif choice == 3:
                accnum = prompt_int("Enter account number: ")
                amt = prompt_float("Enter withdrawal amount: ", min_val=0.01)
                try:
                    newbal = bank.withdraw(accnum, amt)
                    print(f"Withdrawal successful. New balance: ₹{newbal:.2f}")
                except Exception as e:
                    print("Error:", e)

            elif choice == 4:
                accnum = prompt_int("Enter account number: ")
                try:
                    acc = bank.balance_inquiry(accnum)
                    print_account_basic(acc)
                except Exception as e:
                    print("Error:", e)

            elif choice == 5:
                accnum = prompt_int("Enter account number to close: ")
                try:
                    acc = bank.close_account(accnum)
                    print("Account closed.")
                except Exception as e:
                    print("Error:", e)

            elif choice == 6:
                acts = bank.list_active_accounts()
                print(f"Active accounts ({len(acts)}):")
                for a in acts:
                    print_account_basic(a)

            elif choice == 7:
                from_acc = prompt_int("From account #: ")
                to_acc = prompt_int("To account #: ")
                amt = prompt_float("Amount to transfer: ", min_val=0.01)
                try:
                    fb, tb = bank.transfer_funds(from_acc, to_acc, amt)
                    print(f"Transfer successful. Sender balance: ₹{fb:.2f}, Receiver balance: ₹{tb:.2f}")
                except Exception as e:
                    print("Error:", e)

            elif choice == 8:
                accnum = prompt_int("Enter account number: ")
                try:
                    txs = bank.transaction_history(accnum)
                    if not txs:
                        print("No transactions found.")
                    else:
                        for t in txs:
                            print(f"{t['timestamp']} | {t['operation']} | ₹{t['amount']:.2f} | Balance: ₹{t['balance_after']:.2f}")
                except Exception as e:
                    print("Error:", e)

            elif choice == 9:
                accnum = prompt_int("Enter account number: ")
                pin = prompt_int("Enter 4-digit PIN to set: ", min_val=1000, max_val=9999)
                try:
                    bank.set_pin(accnum, pin)
                    print("PIN set successfully.")
                except Exception as e:
                    print("Error:", e)

            elif choice == 10:
                fname = input("Enter import filename (default accounts_import.csv): ").strip() or "accounts_import.csv"
                try:
                    bank.import_accounts_from_file(fname)
                    print("Import completed.")
                except FileNotFoundError:
                    print("File not found.")
                except Exception as e:
                    print("Error importing:", e)

            elif choice == 11:
                out = bank.export_accounts_to_file("export_accounts.csv")
                print("Exported accounts to", out)

            elif choice == 12:
                accnum = prompt_int("Enter account number: ")
                newname = input("Enter new name: ").strip()
                try:
                    bank.rename_account_holder(accnum, newname)
                    print("Name updated.")
                except Exception as e:
                    print("Error:", e)

            elif choice == 13:
                accnum = prompt_int("Enter account number to reopen: ")
                try:
                    bank.reopen_account(accnum)
                    print("Account reopened.")
                except Exception as e:
                    print("Error:", e)

            elif choice == 14:
                print("Total active accounts:", bank.count_active_accounts())

            elif choice == 15:
                confirm = input("Type 'DELETE ALL' to confirm admin deletion: ")
                if confirm == "DELETE ALL":
                    try:
                        bank.delete_all_accounts(admin_confirm=True)
                        print("All accounts deleted and logs cleared.")
                    except Exception as e:
                        print("Error:", e)
                else:
                    print("Deletion cancelled.")

            elif choice == 16:
                n = prompt_int("Top N (default 5): ", min_val=1)
                top = bank.top_n_accounts_by_balance(n)
                for a in top:
                    print_account_basic(a)

            elif choice == 17:
                print(f"Average balance across accounts: ₹{bank.average_balance():.2f}")

            elif choice == 18:
                y = bank.youngest_account_holder()
                o = bank.oldest_account_holder()
                print("Youngest:", y and f"{y.name} | Age: {y.age} | Acc#: {y.account_number}")
                print("Oldest:", o and f"{o.name} | Age: {o.age} | Acc#: {o.account_number}")

            elif choice == 19:
                accnum = prompt_int("Account #: ")
                rate = float(input("Rate percent per year (e.g., 5): "))
                years = float(input("Years: "))
                try:
                    si = bank.simple_interest_calculator(accnum, rate, years)
                    print(f"Simple interest: ₹{si:.2f}")
                except Exception as e:
                    print("Error:", e)

            elif choice == 20:
                name = input("Enter name to search: ")
                res = bank.find_by_name(name)
                if not res:
                    print("No matches.")
                else:
                    for a in res:
                        print_account_basic(a)

            elif choice == 21:
                accnum = prompt_int("Enter account number to search: ")
                acc = bank.find_by_account_number(accnum)
                if not acc:
                    print("Not found.")
                else:
                    print_account_basic(acc)

            elif choice == 22:
                closed = bank.list_closed_accounts()
                print(f"Closed accounts ({len(closed)}):")
                for a in closed:
                    print_account_basic(a)

            elif choice == 23:
                # autosave and exit
                bank.autosave_and_exit()
                print("Goodbye!")
                sys.exit(0)

            elif choice == 24:
                # show menu again
                continue

        except KeyboardInterrupt:
            print("\nDetected Ctrl-C. Autosaving and exiting.")
            bank.autosave_and_exit()
            sys.exit(0)

if __name__ == "__main__":
    main()
