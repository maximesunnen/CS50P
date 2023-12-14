from termcolor import cprint

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