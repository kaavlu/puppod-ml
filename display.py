import pandas as pd
import tkinter as tk
from tkinter import ttk

# ------------------- change your filename to view here ------------------------------
file_path = 'data/filtered/dog_filtered.csv'
df = pd.read_csv(file_path)


# ------------------- display gui code -----------------------------------------------
print("Headers of the filtered DataFrame:")
print(df.columns.tolist())

root = tk.Tk()
root.title("Filtered Dog Data")

tree = ttk.Treeview(root)

tree['columns'] = list(df.columns)
tree.column("#0", width=0, stretch=tk.NO)
tree.heading("#0", text="", anchor=tk.W)

for col in tree['columns']:
    tree.column(col, anchor=tk.W, width=100)
    tree.heading(col, text=col, anchor=tk.W)

for index, row in df.iterrows():
    tree.insert("", "end", values=list(row))

tree.pack(fill=tk.BOTH, expand=True)

root.mainloop()
