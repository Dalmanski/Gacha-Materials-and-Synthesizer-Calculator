import tkinter as tk
from tkinter import ttk, messagebox

materials = {
    "Green": 123,
    "Blue": 12,
    "Purple": 21,
    "Yellow": 2
}

COST_PER_ITEM = 3

next_material = {
    "Green": "Blue",
    "Blue": "Purple",
    "Purple": "Yellow",
}

def update_slider_range(material):
    material_keys = list(materials.keys())
    material = material_keys[material_keys.index(material) - 1]
    quantity = materials[material_keys[material_keys.index(material)]]
    max_quantity = quantity // COST_PER_ITEM
    slider['to'] = max_quantity
    slider.set(0)
    max_label.config(text=f"Max: {max_quantity}")  # Update max label

def craft():
    material = material_combo.get()
    if material:
        quantity_to_craft = slider.get()
        material_keys = list(materials.keys())
        material = material_keys[material_keys.index(material) - 1]
        available_quantity = materials[material_keys[material_keys.index(material)]]
        cost = quantity_to_craft * COST_PER_ITEM

        if cost <= available_quantity:
            materials[material] -= cost
            next_mat = next_material[material]
            if next_mat:
                materials[next_mat] += quantity_to_craft
            messagebox.showinfo("Success", f"Crafted {quantity_to_craft} items of {next_mat}.")
            update_material_labels()
            update_slider_range(material_combo.get())
        else:
            messagebox.showerror("Error", f"Not enough {material} to craft {quantity_to_craft} items.")
    else:
        messagebox.showwarning("Warning", "Please select a material.")

def update_material_labels():
    for material, label in material_labels.items():
        label.config(text=f"{material}: {materials[material]}")

root = tk.Tk()
root.title("Material Crafting")
root.geometry("500x400")
root.configure(bg="#2E2E2E")

select_label = tk.Label(root, text="Select Color Materials:", bg="#2E2E2E", fg="white")
select_label.grid(row=0, column=1, padx=10, pady=(10, 0))

material_combo = ttk.Combobox(root, values=list(materials.keys())[1:], state="readonly")
material_combo.grid(row=1, column=1, padx=10, pady=10)
material_combo.bind("<<ComboboxSelected>>", lambda e: update_slider_range(material_combo.get()))

slider_label = tk.Label(root, text="Quantity to Craft:", bg="#2E2E2E", fg="white")
slider_label.grid(row=2, column=1, padx=10, pady=(10, 0))
slider = tk.Scale(root, from_=0, to=0, orient="horizontal", bg="#4A4A4A", fg="white", troughcolor="#4A4A4A", sliderlength=20)
slider.grid(row=3, column=1, padx=10, pady=10)

max_label = tk.Label(root, text="Max: 0", bg="#2E2E2E", fg="white")  # Label to show max quantity
max_label.grid(row=3, column=2, padx=(0, 10), pady=10)

craft_button = tk.Button(root, text="Craft", command=craft, bg="#4A4A4A", fg="white")
craft_button.grid(row=4, column=1, padx=10, pady=10)

material_labels = {}
sidebar_frame = tk.Frame(root, bg="#2E2E2E")
sidebar_frame.grid(row=0, column=0, rowspan=8, padx=10, pady=10)

sidebar_title = tk.Label(sidebar_frame, text="Available Materials", font=("Arial", 14, "bold"), bg="#2E2E2E", fg="white")
sidebar_title.pack(pady=10)

for material in materials.keys():
    label = tk.Label(sidebar_frame, text=f"{material}: {materials[material]}", font=("Arial", 12), bg="#2E2E2E", fg="white")
    label.pack(anchor="w")
    material_labels[material] = label

root.mainloop()
