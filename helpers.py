from termcolor import cprint, colored

def get_item_input(msg):
    """
    Get item input from the user. Return None if the user wants to exit the program using CTRL+D
    :param str msg: Message used when prompting the user for input
    """
    
    try:
        return input(f"{msg}: ").upper().strip()
    except EOFError:
        cprint("\nExiting program...", "black", "on_white")
        return None
    
def get_quantity_input(msg):
    """
    Get quantity input from the user. Return None if the user wants to exit the program using CTRL+D
    :param str msg: Message used when prompting the user for input
    """
    
    try:
        return input(f"{msg}: ")
    except EOFError:
        cprint("\nExiting program...", "black", "on_white")
        return None
    
def is_valid_quantity(quantity):
    """
    Return True if quantity is larger than 0. Return False otherwise or if a ValueError exception is raised.
    """
    try:
        quantity = int(quantity)
        if quantity > 0:
            return quantity
        else:
            return False
    except ValueError:
        print(colored("Invalid quantity!", "yellow"))
        return False