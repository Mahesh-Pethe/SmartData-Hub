import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import numpy as np
import pandas as pd
import os
import warnings

class DataCleaningApp:
    def __init__(self, root, df):
        self.root = root
        self.root.title("\U0001F4CA Interactive Data Cleaning App")
        self.root.geometry("900x1000")
        self.df = df

        self.bg_color = "#e0f7fa"
        self.section_color = "#b2ebf2"
        self.button_color = "#00796b"
        self.text_color = "#004d40"

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Segoe UI", 10, "bold"), foreground="white", background=self.button_color, padding=10)
        self.root.configure(bg=self.bg_color)

        tk.Label(root, text="\U0001F4C1 Data Cleaning Dashboard", font=("Segoe UI", 18, "bold"), bg=self.bg_color, fg=self.text_color).pack(pady=15)

        self.create_section("\U0001FA9C️ Cleaning Operations", [
            ("\U0001F50D Show Data", self.show_data),
            ("❓ Handle Missing Data", self.handle_missing_data),
            ("\u274C Remove Duplicates", self.remove_duplicates),
            ("\U0001F4CA Handle Outliers", self.handle_outliers),
            ("\U0001F9AE Feature Engineering", self.feature_engineering),
            ("\u2796 Handle Zero/Negative Values", self.zero_negative_values),
            ("\U0001F4C9 Remove Low Variance Columns", self.low_variance_columns),
            ("\U0001F516 Clean Index and Labels", self.clean_index_labels),
        ])

        ttk.Button(self.root, text="\U0001F4BE Save File", command=self.save_file).pack(pady=10)

        self.create_output_section()

    def create_section(self, title, buttons):
        frame = tk.LabelFrame(self.root, text=title, font=("Segoe UI", 12, "bold"), bg=self.section_color, fg="#00332d", padx=10, pady=10, bd=2, relief="ridge")
        frame.pack(padx=10, pady=10, fill="x")
        button_frame = tk.Frame(frame, bg=self.section_color)
        button_frame.pack()

        for index, (text, command) in enumerate(buttons):
            btn = ttk.Button(button_frame, text=text, command=command)
            btn.grid(row=index//3, column=index%3, padx=10, pady=10, ipadx=10, ipady=10, sticky="nsew")

        for col in range(3):
            button_frame.grid_columnconfigure(col, weight=1)

    def create_output_section(self):
        tk.Label(self.root, text="\U0001F4CB Output Log", font=("Segoe UI", 12, "bold"), bg=self.bg_color, fg="#00332d").pack(pady=5)
        frame = tk.Frame(self.root, bg=self.bg_color)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.output_text = tk.Text(frame, height=10, wrap="word", font=("Consolas", 11), bg="black", fg="white", bd=2, relief="sunken")
        self.output_text.pack(side="left", fill="both", expand=True)
        scrollbar = tk.Scrollbar(frame, command=self.output_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.output_text.config(yscrollcommand=scrollbar.set)
        ttk.Button(self.root, text="\U0001F9B9 Clear Output", command=lambda: self.output_text.delete("1.0", "end")).pack(pady=5)

    def log(self, message):
        self.output_text.insert("end", message + "\n")
        self.output_text.see("end")

    def show_data(self):
        top = tk.Toplevel()
        top.title("\U0001F50D Data Preview")
        top.geometry("800x400")
        text = tk.Text(top, wrap='none', font=("Consolas", 10))
        text.insert('end', self.df.head(20).to_string())
        text.pack(expand=True, fill="both")

    def handle_missing_data(self):
        missing = self.df.isnull().sum()
        self.log("[❓] Missing values:\n" + str(missing[missing > 0]))

        options = [
            "0",
            "Unknown",
            "Custom Value",
            "Previous Value (ffill)",
            "Next Value (bfill)",
            "Mode Value"
        ]

        for col in missing[missing > 0].index:
            choice = simpledialog.askstring("Missing Value",
                                            f"Column '{col}' has missing values.\nChoose strategy:\n"
                                            "0 / Unknown / Custom / ffill / bfill / mode").strip().lower()

            if choice == "0":
                self.df[col] = self.df[col].fillna(0)
            elif choice == "unknown":
                self.df[col] = self.df[col].fillna("Unknown")
            elif choice == "custom":
                custom_value = simpledialog.askstring("Custom Value", f"Enter custom value for '{col}':")
                self.df[col] = self.df[col].fillna(custom_value)
            elif choice == "ffill":
                self.df[col] = self.df[col].ffill()  # Forward fill
            elif choice == "bfill":
                self.df[col] = self.df[col].bfill()  # Backward fill
            elif choice == "mode":
                mode_val = self.df[col].mode()
                if not mode_val.empty:
                    self.df[col] = self.df[col].fillna(mode_val[0])
                else:
                    self.df[col] = self.df[col].fillna(0)
            else:
                self.df[col] = self.df[col].fillna(0)
                self.log(f"[!] Unknown choice for '{col}', used default (0)")

        self.log("[✅] Missing values handled with selected strategies.")

    def remove_duplicates(self):
        before = len(self.df)
        self.df.drop_duplicates(inplace=True)
        after = len(self.df)
        self.log(f"[\U0001F9F9] Duplicates removed: {before - after}")

    def handle_outliers(self):
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        handled_cols = []
        for col in numeric_cols:
            q1, q3 = self.df[col].quantile([0.25, 0.75])
            iqr = q3 - q1
            lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
            outliers = self.df[(self.df[col] < lower) | (self.df[col] > upper)][col]
            if not outliers.empty:
                action = simpledialog.askstring("Outliers", f"Outliers in '{col}'. Action? (remove/positive/zero):")
                if action == 'remove':
                    self.df = self.df[~self.df[col].isin(outliers)]
                elif action == 'positive':
                    self.df[col] = self.df[col].apply(lambda x: abs(x) if x in outliers else x)
                elif action == 'zero':
                    self.df[col] = self.df[col].apply(lambda x: 0 if x in outliers else x)
                handled_cols.append(col)
        if handled_cols:
            self.log(f"[⚠️] Outliers handled in columns: {', '.join(handled_cols)}")
        else:
            self.log("[⚠️] No outliers found.")

    def feature_engineering(self):
        nums = self.df.select_dtypes(include=[np.number]).columns
        if len(nums) >= 2:
            self.df['Total'] = self.df[nums].sum(axis=1)
            self.log("[✨] Feature 'Total' added.")

    def zero_negative_values(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=FutureWarning)
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            self.df[numeric_cols] = self.df[numeric_cols].apply(lambda col: np.where(col < 0, 0, col))
        self.log("[0️⃣] Negative values replaced with 0.")

    def low_variance_columns(self):
        drop = [col for col in self.df.columns if self.df[col].nunique() == 1]
        self.df.drop(columns=drop, inplace=True)
        self.log(f"[\U0001F4C9] Dropped low variance columns: {drop}")

    def clean_index_labels(self):
        self.df.columns = self.df.columns.str.strip().str.lower().str.replace(' ', '_')
        self.df.reset_index(drop=True, inplace=True)
        self.log("[\U0001F516] Index and labels cleaned.")

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv")],
                                                 title="Save cleaned DataFrame")
        if file_path:
            self.df.to_csv(file_path, index=False)
            self.log(f"[💾] File saved: {os.path.basename(file_path)}")
