import tkinter as tk
from tkinter import ttk, messagebox

FONT_FAMILY = "Segoe UI"

ranks = ["yellow", "purple", "blue", "green"]
mats = [0, 0, 0, 0]

def matCnt():
    global mats
    try:
        for i in range(len(mat_entries)):
            mats[start_idx + i] = int(mat_entries[i].get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for material counts.")

def calc(idx, reqCnt):
    global mats
    temp = reqCnt
    result_output.config(state="normal")
    result_output.delete(1.0, tk.END)
    result_output.insert(tk.END, "\nResult:\n")
    
    for i in range(idx + 1, len(ranks)):
        if (temp * 3) <= mats[i]:
            result_output.insert(tk.END, 
                f"\nYou have enough {ranks[i]} material."
                f"\nYou can now buy {temp * 3} on {ranks[i - 1]} material."
                f"\nCraft all materials from {ranks[i - 1]} to {ranks[idx]} materials "
                f"to get a total of {reqCnt} {ranks[idx]} material."
            )
            break
        else:
            temp = (temp * 3) - mats[i]
            result_output.insert(tk.END, f"{ranks[i]} material missing {temp} pieces\n".capitalize())
            if i == len(ranks) - 1:
                result_output.insert(tk.END, f"\nYou need {temp} more in {ranks[i]} material.\n")
    result_output.config(state="disabled")

def perform_calculation():
    rankNeed = rank_combobox.get()
    if rankNeed not in ranks:
        messagebox.showerror("Selection Error", "Please select a valid rank.")
        return
    
    try:
        reqCnt = int(material_needed_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number for required material.")
        return

    matCnt()
    idxRank = ranks.index(rankNeed)

    action = action_combobox.get()
    if action == "Keep" or action == "":
        calc(idxRank, reqCnt)
    elif action == "Deduct":
        calc(idxRank, reqCnt - mats[idxRank])

def on_rank_select(event):
    global start_idx
    rankNeed = rank_combobox.get()
    if rankNeed not in ranks:
        return
    
    start_idx = ranks.index(rankNeed)
    
    for widget in mat_frame.winfo_children():
        widget.destroy()
    
    global mat_entries
    mat_entries = []
    
    for i in range(start_idx, len(ranks)):
        label = tk.Label(mat_frame, text=f"How many {ranks[i]} material today?", bg="#2E2E2E", fg="white", font=(FONT_FAMILY, 12))
        label.grid(row=i, column=0, sticky="w")
        entry = tk.Entry(mat_frame, bg="#5C5C5C", fg="white", justify='center', font=(FONT_FAMILY, 12))
        entry.grid(row=i, column=1)
        mat_entries.append(entry)
        entry.bind("<KeyRelease>", check_inputs)

    req_label = tk.Label(mat_frame, text=f"How many {ranks[start_idx]} material do you need?", bg="#2E2E2E", fg="white", font=(FONT_FAMILY, 12))
    req_label.grid(row=len(ranks), column=0, sticky="w", pady=(20, 5))
    req_entry = tk.Entry(mat_frame, bg="#5C5C5C", fg="white", justify='center', font=(FONT_FAMILY, 12))
    req_entry.grid(row=len(ranks), column=1)
    req_entry.bind("<KeyRelease>", check_inputs)

    global material_needed_entry
    material_needed_entry = req_entry

def check_inputs(event=None):
    all_filled = all(entry.get().strip() for entry in mat_entries) and material_needed_entry.get().strip()
    if all_filled:
        rankNeed = rank_combobox.get()
        reqCnt = int(material_needed_entry.get())
        matCnt()
        action_label.config(text=f"Do you want to keep your {rankNeed} material count at {reqCnt},\n"
                                 f"or deduct your current count ({reqCnt} - {mats[start_idx]})?")
        
        action_label.grid(row=3, column=0, columnspan=2, pady=5)
        action_combobox.grid(row=4, column=0, columnspan=2)
        calc_button.grid(row=5, column=0, columnspan=2, pady=10)
    else:
        action_label.grid_forget()
        action_combobox.grid_forget()
        calc_button.grid_forget()

root = tk.Tk()
root.title("Material Calculator")
root.geometry("460x600")
root.resizable(False, False)
root.configure(bg="#2E2E2E")

content_frame = tk.Frame(root, bg="#2E2E2E")
content_frame.pack(pady=10, fill="both", expand=True)

rank_label = tk.Label(content_frame, text="What rank material do you need?", bg="#2E2E2E", fg="white", font=(FONT_FAMILY, 12))
rank_label.grid(row=0, column=0, columnspan=2, pady=5)

rank_combobox = ttk.Combobox(content_frame, values=["yellow", "purple", "blue"])
rank_combobox.bind("<<ComboboxSelected>>", on_rank_select)
rank_combobox.grid(row=1, column=0, columnspan=2)

mat_frame = tk.Frame(content_frame, bg="#2E2E2E")
mat_frame.grid(row=2, column=0, columnspan=2, pady=10)
mat_entries = []
start_idx = 0

action_label = tk.Label(content_frame, text="", bg="#2E2E2E", fg="white", font=(FONT_FAMILY, 12))
action_label.grid(row=3, column=0, columnspan=2, pady=5)
action_label.grid_forget()

action_combobox = ttk.Combobox(content_frame, values=["Keep", "Deduct"], state="readonly")
action_combobox.grid(row=4, column=0, columnspan=2)
action_combobox.grid_forget()

calc_button = tk.Button(content_frame, text="Calculate", command=perform_calculation, bg="#5C5C5C", fg="white", font=(FONT_FAMILY, 12))
calc_button.grid(row=5, column=0, columnspan=2, pady=10)
calc_button.grid_forget()

result_output = tk.Text(content_frame, height=10, width=45, state="disabled", wrap="word", bg="#3E3E3E", fg="white", font=(FONT_FAMILY, 12))
result_output.grid(row=6, column=0, columnspan=2, pady=10)

def center_align_text_widget(widget):
    widget.config(state='normal')
    widget.delete(1.0, tk.END)
    text = "\nHi, Welcome to Gacha Materials and Synthesize Calculator"
    widget.insert(tk.END, text)
    widget.config(state='disabled')

center_align_text_widget(result_output)

def on_closing():
    root.quit()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
