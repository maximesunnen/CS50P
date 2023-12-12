import sys

def get_item_input(msg):
    """
    """
    try:
        return input(f"{msg}: ").upper().strip()
    except EOFError:
        print("\nExiting program...")
        return None
    
def get_quantity_input(msg):
    """
    """
    try:
        return int(input(f"{msg}: "))
    except EOFError:
        print("\nExiting program...")
        return None