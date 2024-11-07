import tkinter as tk
from tkinter import ttk

def check_entries():
    # Get the value from the spinbox
    spinbox_value = spinbox.get()

    # Check if spinbox is not zero and if all entries are filled
    all_filled = all(entry.get().strip() for entry in mat_entries) and material_needed_entry.get().strip() and spinbox_value != '0'
    
    # Print the result or take action based on condition
    if all_filled:
        print("All entries are filled and spinbox is not zero!")
    else:
        print("Some entries are missing or spinbox is zero.")

root = tk.Tk()

# Create some entry widgets
mat_entries = [tk.Entry(root) for _ in range(3)]
for entry in mat_entries:
    entry.pack()

# Create a Spinbox widget
spinbox = ttk.Spinbox(root, from_=0, to=10)
spinbox.pack()

# Material needed entry
material_needed_entry = tk.Entry(root)
material_needed_entry.pack()

# Button to check entries
check_button = tk.Button(root, text="Check Entries", command=check_entries)
check_button.pack()

root.mainloop()
