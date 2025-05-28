# --- Prediction.py ---
import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
import numpy as np

class PredictionApp:
    def __init__(self, root, df):
        self.root = root
        self.df = df
        self.root.title("🎯 Prediction App")
        self.root.geometry("650x400")
        self.root.configure(bg="#f0f8ff")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#f0f8ff")
        self.style.configure("TLabel", font=("Segoe UI", 10), background="#f0f8ff")
        self.style.configure("TButton", font=("Segoe UI", 10, "bold"), background="#ffffff", foreground="#0078d7")
        self.style.map("TButton", background=[("active", "#e6f2ff")], foreground=[("active", "#005a9e")])

        title = tk.Label(root, text="Prediction App", font=("Segoe UI", 16, "bold"), bg="#4682b4", fg="white", pady=10)
        title.pack(fill="x")

        main_frame = ttk.Frame(root, padding=20)
        main_frame.pack(fill="both", expand=True)

        for i in range(2):
            main_frame.columnconfigure(i, weight=1, uniform="col")

        ttk.Label(main_frame, text="Prediction Type:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.prediction_type = ttk.Combobox(main_frame, state="readonly", values=["Numeric (Linear Regression)", "Categorical (Logistic Regression)"], width=35)
        self.prediction_type.grid(row=0, column=1, sticky="w", pady=5)

        ttk.Label(main_frame, text="Target Column:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.column_dropdown = ttk.Combobox(main_frame, state="readonly", width=35)
        self.column_dropdown.grid(row=1, column=1, sticky="w", pady=5)

        ttk.Label(main_frame, text="Feature Columns (comma):").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.feature_entry = ttk.Entry(main_frame, width=38)
        self.feature_entry.grid(row=2, column=1, sticky="w", pady=5)

        train_button = ttk.Button(main_frame, text="🚀 Train Model", command=self.train_model, width=25)
        train_button.grid(row=3, column=0, columnspan=2, pady=(10, 10))

        ttk.Label(main_frame, text="Prediction Input (comma):").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.value_entry = ttk.Entry(main_frame, width=38)
        self.value_entry.grid(row=4, column=1, sticky="w", pady=5)

        predict_button = ttk.Button(main_frame, text="🔮 Predict", command=self.make_prediction, width=25)
        predict_button.grid(row=5, column=0, columnspan=2, pady=(10, 5))

        self.column_dropdown["values"] = list(self.df.columns)

    def train_model(self):
        target_column = self.column_dropdown.get()
        feature_columns = [col.strip() for col in self.feature_entry.get().split(",")]
        prediction_type = self.prediction_type.get()

        if not target_column or not feature_columns or not prediction_type:
            messagebox.showerror("Error", "Please select all options!")
            return

        try:
            X = self.df[feature_columns].dropna().astype(float)
            y = self.df[target_column].dropna()

            if prediction_type == "Numeric (Linear Regression)":
                self.model = make_pipeline(StandardScaler(), LinearRegression())
            else:
                self.model = make_pipeline(
                    StandardScaler(),
                    LogisticRegression(max_iter=100000, solver='saga')
                )

            self.model.fit(X, y)
            self.feature_columns = feature_columns
            messagebox.showinfo("Success", "Model trained successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Training failed: {e}")

    def make_prediction(self):
        if not hasattr(self, 'model'):
            messagebox.showerror("Error", "Please train the model first!")
            return

        try:
            input_values = np.array([float(val.strip()) for val in self.value_entry.get().split(",")]).reshape(1, -1)
            input_df = pd.DataFrame(input_values, columns=self.feature_columns)
            prediction = self.model.predict(input_df)
            messagebox.showinfo("Prediction Result", f"🔮 Predicted value: {prediction[0]}")
        except Exception as e:
            messagebox.showerror("Error", f"Prediction failed: {e}")
