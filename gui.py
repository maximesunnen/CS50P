import tkinter as tk
from tkinter import ttk
from db import load_db

DB_FILE_NAME = "inv.db"
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 800

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory in Tkinter")
        
        # Set window size
        root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        # Frame for navigation buttons
        self.nav_frame = tk.Frame(root)
        
        # Buttons for nav frame
        display_button = tk.Button(self.nav_frame, text="Inventory", command=self.show_display_view)
        display_button.pack(side=tk.LEFT)
        
        # Create buttons and entry widgets in the find frame
        find_button = tk.Button(self.nav_frame, text="Find item", command=self.show_find_view)
        find_button.pack(side=tk.LEFT)
        
        # Pack nav frame
        self.nav_frame.pack(side=tk.TOP, pady=10)

        # Frame for the display view (not packed yet!)
        self.display_frame = tk.Frame(root)
        self.create_display_view()

        # Frame for the find view (not packed yet!)
        self.find_frame = tk.Frame(root)
        self.create_find_view()
        
        # Create tree for displaying inventory
        self.tree = ttk.Treeview(root, column=("c1", "c2"), show="headings", height=100)

        # Define tree headings
        self.tree.column("#1", anchor=tk.CENTER)
        self.tree.heading("#1", text="ITEM")
        self.tree.column("#2", anchor=tk.CENTER)
        self.tree.heading("#2", text="QUANTITY")

    def create_display_view(self):
        # Create buttons in the display frame (the buttons are created and packed, but the frame they're in is not yet packed!)
        display_inventory_button = tk.Button(self.display_frame, text="Display inventory", command=self.display_inventory)
        display_inventory_button.pack()

    def create_find_view(self):
        #Create buttons in the find frame (the buttons are created and packed, but the frame they're in is not yet packed!)
        back_button = tk.Button(self.nav_frame, text="Back to main menu", command=self.show_display_view)
        back_button.pack(side=tk.LEFT)

        entry_label = tk.Label(self.find_frame, text="Enter Item:")
        entry_label.pack()

        entry_widget = tk.Entry(self.find_frame)
        entry_widget.pack()

        find_item_button = tk.Button(self.find_frame, text="Find")
        find_item_button.pack()

    def show_display_view(self):
        self.find_frame.pack_forget()
        self.display_frame.pack()

    def show_find_view(self):
        self.display_frame.pack_forget()
        self.tree.pack_forget()
        self.find_frame.pack()
        
    def display_inventory(self):
        # load the inventory
        inv = load_db(DB_FILE_NAME)
        
        # create list from inventory
        inv_list = []
        for key in sorted(inv.keys()):
            inv_list.append([key, inv[key]])

        self.tree.delete(*self.tree.get_children())
        
        for list_item in sorted(inv_list):
            self.tree.insert("", tk.END, values=list_item)

        self.tree.pack(fill=tk.X, side=tk.BOTTOM)

# Create the main Tkinter window
root = tk.Tk()
app = App(root)

# Start the Tkinter event loop
root.mainloop()
