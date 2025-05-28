# --- Visulization.py ---
import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

class DataVisualizationApp:
    def __init__(self, root, df):
        self.root = root
        self.df = df
        self.root.title("📊 Advanced Data Visualization App")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)
        self.root.configure(bg="#f4f8fc")

        title_label = tk.Label(root, text="📊 Data Visualization Dashboard", font=("Arial Rounded MT Bold", 20), bg="#4682B4", fg="white", pady=12)
        title_label.pack(fill='x')

        form_frame = tk.Frame(root, bg="#f4f8fc")
        form_frame.pack(pady=5, padx=20, fill='x')

        tk.Label(form_frame, text="X-axis Column:", font=("Arial", 11), bg="#f4f8fc").grid(row=0, column=0, padx=10, pady=8, sticky="w")
        self.x_column_dropdown = ttk.Combobox(form_frame, width=30, state="readonly")
        self.x_column_dropdown.grid(row=0, column=1, padx=10, pady=8)

        tk.Label(form_frame, text="Y-axis Column:", font=("Arial", 11), bg="#f4f8fc").grid(row=1, column=0, padx=10, pady=8, sticky="w")
        self.y_column_dropdown = ttk.Combobox(form_frame, width=30, state="readonly")
        self.y_column_dropdown.grid(row=1, column=1, padx=10, pady=8)

        btn_frame = tk.Frame(root, bg="#f4f8fc")
        btn_frame.pack(pady=10, padx=20, fill='both', expand=True)

        chart_buttons = [
            ("📈 Line Graph", self.plot_line_graph),
            ("📊 Bar Graph", self.plot_bar_graph),
            ("🔵 Scatter Plot", self.plot_scatter_plot),
            ("🥧 Pie Chart", self.plot_pie_chart),
            ("💠 Heatmap", self.plot_heatmap),
            ("📦 Boxplot", self.plot_boxplot),
            ("🔶 Pairplot", self.plot_pairplot),
            ("🌐 Interactive Scatter", self.plot_interactive_scatter),
            ("📊 Interactive Bar", self.plot_interactive_bar),
        ]

        for i, (text, cmd) in enumerate(chart_buttons):
            btn = tk.Button(btn_frame, text=text, command=cmd, font=("Arial", 11, "bold"), bg="#3498db", fg="white", relief="raised", padx=10, pady=8, cursor="hand2")
            btn.grid(row=i // 2, column=i % 2, padx=10, pady=8, sticky="ew")

        for i in range(2):
            btn_frame.grid_columnconfigure(i, weight=1)

        self.x_column_dropdown['values'] = list(self.df.columns)
        self.y_column_dropdown['values'] = list(self.df.columns)

    def get_selected_columns(self):
        x_col = self.x_column_dropdown.get()
        y_col = self.y_column_dropdown.get()
        if x_col not in self.df.columns or y_col not in self.df.columns:
            messagebox.showerror("Error", "Please select valid columns!")
            return None, None
        return x_col, y_col

    def plot_line_graph(self):
        x_col, y_col = self.get_selected_columns()
        if x_col and y_col:
            self.df.plot(x=x_col, y=y_col, kind='line', marker='o', title="Line Graph")
            plt.grid(True)
            plt.tight_layout()
            plt.show()

    def plot_bar_graph(self):
        x_col, y_col = self.get_selected_columns()
        if x_col and y_col:
            self.df.plot(x=x_col, y=y_col, kind='bar', title="Bar Graph")
            plt.tight_layout()
            plt.show()

    def plot_scatter_plot(self):
        x_col, y_col = self.get_selected_columns()
        if x_col and y_col:
            self.df.plot(x=x_col, y=y_col, kind='scatter', title="Scatter Plot")
            plt.tight_layout()
            plt.show()

    def plot_pie_chart(self):
        column = self.x_column_dropdown.get()
        if column in self.df.columns:
            self.df[column].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90, shadow=True)
            plt.title(f"Pie Chart of {column}")
            plt.ylabel("")
            plt.tight_layout()
            plt.show()

    def plot_heatmap(self):
        corr = self.df.corr()
        sns.heatmap(corr, annot=True, cmap="coolwarm", center=0)
        plt.title("Correlation Heatmap")
        plt.tight_layout()
        plt.show()

    def plot_boxplot(self):
        x_col, y_col = self.get_selected_columns()
        if x_col and y_col:
            sns.boxplot(x=self.df[x_col], y=self.df[y_col], color="lightblue")
            plt.title(f"Boxplot of {x_col} vs {y_col}")
            plt.tight_layout()
            plt.show()

    def plot_pairplot(self):
        sns.pairplot(self.df)
        plt.tight_layout()
        plt.show()

    def plot_interactive_scatter(self):
        x_col, y_col = self.get_selected_columns()
        if x_col and y_col:
            fig = px.scatter(self.df, x=x_col, y=y_col, title="Interactive Scatter Plot")
            fig.show()

    def plot_interactive_bar(self):
        x_col, y_col = self.get_selected_columns()
        if x_col and y_col:
            fig = px.bar(self.df, x=x_col, y=y_col, title="Interactive Bar Graph")
            fig.show()
