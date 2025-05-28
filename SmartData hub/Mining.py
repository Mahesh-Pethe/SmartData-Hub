# --- Mining.py ---
import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd

class DataFilterApp:
    def __init__(self, root, df):
        self.root = root
        self.df = df
        self.root.title("🔍 Data Mining & Filter Tool")
        self.root.geometry("900x650")
        self.root.configure(bg="#e6f2ff")

        title_label = tk.Label(root, text="📊 Dynamic Data Mining Tool", font=("Helvetica", 20, "bold"), bg="#e6f2ff", fg="#003366")
        title_label.pack(pady=15)

        control_frame = tk.LabelFrame(root, text="🔧 Filter Options", font=("Arial", 12, "bold"), bg="#e6f2ff", fg="#003366", padx=10, pady=10)
        control_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(control_frame, text="Column:", bg="#e6f2ff").grid(row=0, column=0, sticky="e", pady=5)
        self.column_dropdown = ttk.Combobox(control_frame, state="readonly")
        self.column_dropdown.grid(row=0, column=1, padx=10)

        tk.Label(control_frame, text="Condition / Keyword:", bg="#e6f2ff").grid(row=1, column=0, sticky="e", pady=5)
        self.condition_entry = tk.Entry(control_frame, width=30)
        self.condition_entry.grid(row=1, column=1, padx=10)

        search_btn = tk.Button(control_frame, text="🔎 Apply Filter", bg="#28a745", fg="white", font=("Arial", 12), command=self.filter_data)
        search_btn.grid(row=2, column=1, pady=10)

        reset_btn = tk.Button(control_frame, text="🔄 Reset Filters", bg="#ffc107", fg="black", font=("Arial", 12), command=self.reset_filters)
        reset_btn.grid(row=2, column=2, padx=10)

        self.status_label = tk.Label(root, text="🔔 Filter data using conditions.", font=("Arial", 10, "italic"), bg="#e6f2ff", fg="gray")
        self.status_label.pack()

        result_frame = tk.Frame(root)
        result_frame.pack(fill="both", expand=True, padx=10, pady=10)
        vsb = ttk.Scrollbar(result_frame, orient="vertical")
        hsb = ttk.Scrollbar(result_frame, orient="horizontal")

        self.result_tree = ttk.Treeview(result_frame, yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.config(command=self.result_tree.yview)
        hsb.config(command=self.result_tree.xview)

        self.result_tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")

        self.column_dropdown['values'] = list(self.df.columns)
        self.display_results(self.df)

    def filter_data(self):
        column = self.column_dropdown.get()
        search_value = self.condition_entry.get().strip()
        if not column or not search_value:
            messagebox.showerror("Error", "Please select a column and enter a condition!")
            return

        try:
            if any(op in search_value for op in ['>', '<', '>=', '<=', '=']):
                filtered_df = self.df.query(f"`{column}` {search_value}")
            else:
                filtered_df = self.df[self.df[column].astype(str).str.contains(search_value, na=False, case=False)]
            self.display_results(filtered_df)
            self.status_label.config(text=f"✅ Showing results for: {column} {search_value}")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid condition: {e}")
            self.status_label.config(text="❌ Filter error.")

    def reset_filters(self):
        self.column_dropdown.set('')
        self.condition_entry.delete(0, tk.END)
        self.display_results(self.df)
        self.status_label.config(text="🔄 Filters reset. Showing all data.")

    def display_results(self, data):
        self.result_tree.delete(*self.result_tree.get_children())
        self.result_tree["columns"] = list(data.columns)
        self.result_tree["show"] = "headings"
        for col in data.columns:
            self.result_tree.heading(col, text=col)
            self.result_tree.column(col, width=150, anchor="center")
        for _, row in data.iterrows():
            self.result_tree.insert("", "end", values=list(row))
