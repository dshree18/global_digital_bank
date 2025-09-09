# utils.py
def prompt_int(prompt_text, min_val=None, max_val=None):
    while True:
        try:
            v = int(input(prompt_text))
            if min_val is not None and v < min_val:
                print(f"Value must be >= {min_val}")
                continue
            if max_val is not None and v > max_val:
                print(f"Value must be <= {max_val}")
                continue
            return v
        except ValueError:
            print("Please enter a valid integer.")

def prompt_float(prompt_text, min_val=None, max_val=None):
    while True:
        try:
            v = float(input(prompt_text))
            if min_val is not None and v < min_val:
                print(f"Value must be >= {min_val}")
                continue
            if max_val is not None and v > max_val:
                print(f"Value must be <= {max_val}")
                continue
            return v
        except ValueError:
            print("Please enter a valid number.")
