import tkinter as tk
from tkinter import ttk

FONT_FAMILY = "MS PGothic"
FONT_SIZE = 13

# Light mode theme
TEXT_COLOR = "black"
BG_COLOR = "#FFFFFF"
ENTRY_BG = "#F0F0F0"
SCROLLBAR_BG = "#D3D3D3"

def color_theme(theme):
    global TEXT_COLOR, BG_COLOR, ENTRY_BG, SCROLLBAR_BG
    if theme == "contrast dark mode":
        TEXT_COLOR = "white"
        BG_COLOR = "black"
        ENTRY_BG = "#121212"
        SCROLLBAR_BG = "#121212"
    elif theme == "modern dark mode":
        TEXT_COLOR = "white"
        BG_COLOR = "#2E2E2E"
        ENTRY_BG = "#5C5C5C"
        SCROLLBAR_BG = "#3E3E3E"

color_theme("contrast dark mode")

ranks = ["yellow", "purple", "blue", "green"]
mats = [0, 0, 0, 0]

def matCount():
    global mats
    for i in range(len(mat_entries)):
        mats[start_idx + i] = int(mat_entries[i].get())

def calculate(idx, reqCount):
    global mats
    temp = reqCount
    clear_tktext()

    text = f"\nYour {ranks[idx]} material needed: {reqCount}\n"
    text += "\nResults:"
    
    for i in range(idx + 1, len(ranks)):
        total = 0
        for j in range(len(ranks) - 1, idx, -1):
            total = (total // 3) + mats[j]

        if (temp * 3) <= mats[i]:
            text += f"\n\nYou have enough {ranks[i]} material."
            text += f"\nYou can now buy {temp} pieces on {ranks[i - 1]} material."
            if ranks[i - 1] != ranks[idx]:
                text += f"\n\nCraft all materials from {ranks[i - 1]} to {ranks[idx]} materials "
                text += f"to get a total of {reqCount} {ranks[idx]} material."
            text += f"\n\nIf you want to craft ALL of them, your total {ranks[idx]} material is {total} pieces."
            break
        else:
            temp = (temp * 3) - mats[i]
            if i != len(ranks) - 1:
                text += f"\n{ranks[i].capitalize()} material missing {temp} pieces"
            else:
                text += f"\n\nYou need {temp} more in {ranks[i]} material.\n"

    result_tktext_in_center(text)

def perform_calculation():
    rankNeed = rank_combobox.get().lower()
    reqCount = int(mat_needed_entry.get())
    matCount()
    idxRank = ranks.index(rankNeed)
    action = action_combobox.get()

    if action == "Keep" or action == "":
        calculate(idxRank, reqCount)
    elif action == "Deduct":
        calculate(idxRank, reqCount - mats[idxRank])
    elif action == "Add":
        calculate(idxRank, reqCount + mats[idxRank])

def on_rank_select(event):
    global start_idx
    rankNeed = rank_combobox.get().lower()
    if rankNeed not in ranks:
        return  
    start_idx = ranks.index(rankNeed)    

    for widget in mat_frame.winfo_children():
        widget.destroy()   

    global mat_entries
    mat_entries = []

    def validate_input(P):
        if P == "" or P.isdigit(): return True
        else: return False
    validate = mat_frame.register(validate_input)
    
    for i in range(start_idx, len(ranks)):
        label = tk.Label(mat_frame, text=f"How many {ranks[i]} material today?", bg=BG_COLOR, fg=TEXT_COLOR, font=(FONT_FAMILY, FONT_SIZE))
        label.grid(row=i, column=0, sticky="w")
        entry = tk.Spinbox(mat_frame, from_=0, to=999999, increment=1, width=15, bg=ENTRY_BG, fg=TEXT_COLOR, justify='center', font=(FONT_FAMILY, FONT_SIZE), validate="key", validatecommand=(validate, "%P"))
        entry.grid(row=i, column=1)
        mat_entries.append(entry)
        entry.bind("<ButtonRelease-1>", check_inputs)
        entry.bind("<KeyRelease>", check_inputs)

    req_label = tk.Label(mat_frame, text=f"How many {ranks[start_idx]} material do you need?", bg=BG_COLOR, fg=TEXT_COLOR, font=(FONT_FAMILY, FONT_SIZE))
    req_label.grid(row=len(ranks), column=0, sticky="w", pady=(20, 5))
    req_entry = tk.Spinbox(mat_frame, from_=0, to=999999, increment=1, width=15, bg=ENTRY_BG, fg=TEXT_COLOR, justify='center', font=(FONT_FAMILY, FONT_SIZE), validate="key", validatecommand=(validate, "%P"))
    req_entry.grid(row=len(ranks), column=1, sticky="w", pady=(20, 5))
    req_entry.bind("<ButtonRelease-1>", check_inputs)
    req_entry.bind("<KeyRelease>", check_inputs)

    global mat_needed_entry
    mat_needed_entry = req_entry

def check_inputs(event=None):

    def format_entry(entries):
        if entries.get().strip() == "":
            entries.delete(0, tk.END)
            entries.insert(0, "0")
        else:
            formatted_value = str(int(entries.get()))
            entries.delete(0, tk.END)
            entries.insert(0, formatted_value)

    for entry in mat_entries:
        format_entry(entry)

    format_entry(mat_needed_entry)
    
    if mat_needed_entry.get().strip() != '0':
        rankNeed = rank_combobox.get().lower()
        reqCount = int(mat_needed_entry.get())
        matCount()     
        action_label.grid(row=3, column=0, columnspan=2, pady=5)
        action_combobox.grid(row=4, column=0, columnspan=2)
        calc_button.grid(row=5, column=0, columnspan=2, pady=10)
        texted = f"Do you want to keep your {rankNeed} material count at {reqCount}\n"
        action_combobox["values"] = ["Keep"]
        if reqCount > mats[start_idx]:  
            if mats[start_idx] != 0:
                action_combobox["values"] = ["Keep", "Deduct", "Add"]
                texted += f"or add your current count ({reqCount} + {mats[start_idx]} = {reqCount + mats[start_idx]})?\n"
                texted += f"or deduct your current count ({reqCount} - {mats[start_idx]} = {reqCount - mats[start_idx]})?"
            else:
                texted = f"Since 0 is your current {rankNeed} material count,\nwe should compute this right away."
                action_combobox.grid_forget()                      
        else:
            action_combobox["values"] = ["Keep", "Add"]
            texted += f"or add your current count ({reqCount} + {mats[start_idx]} = {reqCount + mats[start_idx]})?"
            
        action_label.config(text = texted)
    else:
        action_label.grid_forget()
        action_combobox.grid_forget()
        calc_button.grid_forget()


root = tk.Tk()
root.title("Gacha Materials and Synthesizer Calculator")
window_width, window_height = 460, 620
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = (screen_height // 2) - (window_height // 2)
position_right = (screen_width // 2) - (window_width // 2)
root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
root.resizable(False, False)
root.configure(bg=BG_COLOR)

content_frame = tk.Frame(root, bg=BG_COLOR)
content_frame.pack(pady=10, fill="both", expand=True)

rank_label = tk.Label(content_frame, text="What rank material do you need?", bg=BG_COLOR, fg=TEXT_COLOR, font=(FONT_FAMILY, FONT_SIZE))
rank_label.grid(row=0, column=0, columnspan=2, pady=5)

rank_combobox = ttk.Combobox(content_frame, values=["Yellow", "Purple", "Blue"], state="readonly", style="TCombobox", justify='center', font=(FONT_FAMILY, FONT_SIZE))
rank_combobox.set("Yellow")
rank_combobox.bind("<<ComboboxSelected>>", on_rank_select)
rank_combobox.grid(row=1, column=0, columnspan=2)

mat_frame = tk.Frame(content_frame, bg=BG_COLOR)
mat_frame.grid(row=2, column=0, columnspan=2, pady=10)
mat_entries = []
start_idx = 0

action_label = tk.Label(content_frame, text="", bg=BG_COLOR, fg=TEXT_COLOR, font=(FONT_FAMILY, FONT_SIZE))
action_label.grid(row=3, column=0, columnspan=2, pady=5)
action_label.grid_forget()

action_combobox = ttk.Combobox(content_frame, state="readonly", style="TCombobox", justify='center', font=(FONT_FAMILY, FONT_SIZE))
action_combobox.set("Keep")
action_combobox.grid(row=4, column=0, columnspan=2)
action_combobox.grid_forget()

calc_button = tk.Button(content_frame, text="Calculate", command=perform_calculation, bg=ENTRY_BG, fg=TEXT_COLOR, font=(FONT_FAMILY, FONT_SIZE))
calc_button.grid(row=5, column=0, columnspan=2, pady=10)
calc_button.grid_forget()

result_output = tk.Text(content_frame, height=10, width=45, state="disabled", wrap="word", bg=SCROLLBAR_BG, fg=TEXT_COLOR, font=(FONT_FAMILY, FONT_SIZE))

style = ttk.Style()
style.theme_use("default")
style.configure("TScrollbar", background=SCROLLBAR_BG, troughcolor=BG_COLOR, bordercolor=BG_COLOR, arrowcolor=TEXT_COLOR)

style.map("TCombobox", 
          fieldbackground=[("readonly", SCROLLBAR_BG)],
          background=[("readonly", SCROLLBAR_BG)],
          foreground=[("readonly", TEXT_COLOR)],
          arrowcolor=[("readonly", TEXT_COLOR)])

style.configure("TCombobox",
                fieldbackground = SCROLLBAR_BG,
                background = SCROLLBAR_BG,
                foreground = TEXT_COLOR,
                bordercolor = BG_COLOR,
                lightcolor = BG_COLOR,
                darkcolor = BG_COLOR,
                arrowcolor = TEXT_COLOR)

v_scroll = ttk.Scrollbar(content_frame, orient="vertical", command=result_output.yview, style="TScrollbar")
result_output.configure(yscrollcommand=v_scroll.set)

result_output.grid(row=6, column=0, pady=10, sticky="nsew")
v_scroll.grid(row=6, column=1, sticky="ns")
v_scroll.grid_remove()

def check_scrollbar():
    result_output.update_idletasks() 
    if result_output.yview() == (0.0, 1.0): 
        v_scroll.grid_remove()  
    else: v_scroll.grid()

def clear_tktext():
    result_output.config(state="normal")
    result_output.delete(1.0, tk.END)
    result_output.config(state="disabled")

def result_tktext_in_center(text):
    result_output.config(state='normal')
    lines = text.split('\n')
    for line in lines:
        result_output.tag_configure("tag-center", justify='center')
        result_output.insert('end', line + '\n' ,'tag-center')
    result_output.config(state='disabled')
    check_scrollbar()

result_tktext_in_center("\nHi, Welcome to Gacha Materials and Synthesizer Calculator")
on_rank_select("yellow")

def on_closing():
    root.quit()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()