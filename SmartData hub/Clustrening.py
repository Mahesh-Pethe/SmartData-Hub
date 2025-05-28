import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import pandas as pd
from sklearn.cluster import KMeans
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram
import matplotlib.pyplot as plt
import numpy as np

class ClusteringApp:
    def __init__(self, root, df):
        self.root = root
        self.df = df
        self.root.title("✨ CSV Clustering App ✨")
        self.root.geometry("600x430")
        self.root.configure(bg="#f0f4f7")
        self.root.resizable(True, True)

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#f0f4f7")
        self.style.configure("TLabel", font=("Segoe UI", 10), background="#f0f4f7", foreground="#333")
        self.style.configure("TButton", font=("Segoe UI", 10, "bold"), background="#ffffff", foreground="#0078d7")
        self.style.map("TButton", background=[("active", "#e6f2ff")], foreground=[("active", "#005a9e")])

        main_frame = ttk.Frame(root, padding=20, style="TFrame")
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Select column for clustering:").pack(anchor="w", pady=(10, 0))
        self.column_dropdown = ttk.Combobox(main_frame, state="readonly")
        self.column_dropdown.pack(fill="x", pady=5)

        ttk.Label(main_frame, text="Enter number of clusters (K):").pack(anchor="w", pady=(10, 0))
        vcmd = (root.register(lambda P: P.isdigit() or P == ""), "%P")
        self.k_entry = ttk.Entry(main_frame, validate="key", validatecommand=vcmd)
        self.k_entry.pack(fill="x", pady=5)

        ttk.Label(main_frame, text="Select clustering type:").pack(anchor="w", pady=(10, 0))
        self.cluster_type = ttk.Combobox(main_frame, state="readonly", values=["K-Means", "Hierarchical"])
        self.cluster_type.pack(fill="x", pady=5)
        self.cluster_type.set("K-Means")

        cluster_btn = ttk.Button(main_frame, text="🔍 Perform Clustering", command=self.perform_clustering)
        cluster_btn.pack(pady=20)

        self.status_label = ttk.Label(root, text="Data loaded. Ready for clustering.", relief="sunken", anchor="w", background="#e0e0e0")
        self.status_label.pack(fill="x", side="bottom")

        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        self.column_dropdown["values"] = numeric_cols
        if numeric_cols:
            self.column_dropdown.set(numeric_cols[0])

    def perform_clustering(self):
        column = self.column_dropdown.get()
        cluster_type = self.cluster_type.get()
        k_value = self.k_entry.get()

        if not column or not cluster_type or not k_value.isdigit():
            messagebox.showerror("Error", "Please fill all fields correctly!")
            return

        k_value = int(k_value)
        data = self.df[[column]].dropna().astype(float)

        if cluster_type == "K-Means":
            self.k_means_clustering(data, column, k_value)
        else:
            self.hierarchical_clustering(data, column, k_value)

        self.save_result()

    def k_means_clustering(self, data, column, k_value):
        kmeans = KMeans(n_clusters=k_value, n_init=10, random_state=42)
        cluster_labels = kmeans.fit_predict(data)
        self.df.loc[data.index, 'Cluster'] = cluster_labels
        centers = kmeans.cluster_centers_

        plt.figure(figsize=(10, 5))
        cmap = plt.get_cmap('tab10')
        for i in range(k_value):
            color = cmap(i % 10)
            cluster_points = data.loc[self.df['Cluster'] == i]
            plt.scatter(cluster_points[column], [0] * len(cluster_points), color=color, label=f'Cluster {i}')
            plt.scatter(centers[i], 0, color='black', marker='x', s=100)
            plt.axvline(x=centers[i], color=color, linestyle='dashed')

        plt.title(f'K-Means Clustering on {column}')
        plt.xlabel(column)
        plt.yticks([])
        plt.grid(True)
        plt.tight_layout()
        plt.legend()
        plt.show()

    def hierarchical_clustering(self, data, column, k_value):
        linkage_matrix = linkage(data, method='ward')
        cluster_labels = fcluster(linkage_matrix, k_value, criterion='maxclust')
        self.df.loc[data.index, 'Cluster'] = cluster_labels

        plt.figure(figsize=(10, 6))
        dendrogram(linkage_matrix, labels=data.index)
        plt.title(f'Hierarchical Clustering on {column}')
        plt.xlabel("Data Points")
        plt.ylabel("Distance")
        plt.tight_layout()
        plt.show()

    def save_result(self):
        base_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")],
            title="Save clustered data - base name only"
        )

        if not base_path:
            return

        # Remove extension from base name
        if base_path.endswith(".csv"):
            ext = ".csv"
            base_path = base_path[:-4]
        elif base_path.endswith(".xlsx"):
            ext = ".xlsx"
            base_path = base_path[:-5]
        else:
            ext = ".csv"  # Default

        try:
            for label in sorted(self.df['Cluster'].unique()):
                cluster_df = self.df[self.df['Cluster'] == label]
                filename = f"{base_path}_Cluster{label}{ext}"
                if ext == ".csv":
                    cluster_df.to_csv(filename, index=False)
                else:
                    cluster_df.to_excel(filename, index=False)
            messagebox.showinfo("Saved", f"Clustered files saved with base name:\n{base_path}_ClusterX{ext}")
        except Exception as e:
            messagebox.showerror("Save Error", f"Error saving clustered files:\n{str(e)}")
