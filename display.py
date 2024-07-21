import pandas as pd
import tkinter as tk
from tkinter import ttk

# ------------------- Change your filenames to view here ------------------------------
file_paths = ['data/filtered/merged_data.csv']

# Function to create a Treeview for a given DataFrame
def create_treeview(frame, df):
    tree = ttk.Treeview(frame)

    tree['columns'] = list(df.columns)
    tree.column("#0", width=0, stretch=tk.NO)
    tree.heading("#0", text="", anchor=tk.W)

    for col in tree['columns']:
        tree.column(col, anchor=tk.W, width=100)
        tree.heading(col, text=col, anchor=tk.W)

    for index, row in df.iterrows():
        tree.insert("", "end", values=list(row))

    tree.pack(fill=tk.BOTH, expand=True)

# ------------------- Display GUI code -----------------------------------------------
root = tk.Tk()
root.title("Filtered Data")

notebook = ttk.Notebook(root)

# Create a tab for each file
for file_path in file_paths:
    df = pd.read_csv(file_path)
    print(f"Headers of the DataFrame from {file_path}:")
    print(df.columns.tolist())
    
    frame = ttk.Frame(notebook)
    notebook.add(frame, text=file_path.split('/')[-1])  # Tab title is the filename
    create_treeview(frame, df)

notebook.pack(fill=tk.BOTH, expand=True)

root.mainloop()
