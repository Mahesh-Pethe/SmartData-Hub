import tkinter as tk
from tkinter import messagebox, filedialog
import webbrowser
from PIL import Image, ImageTk,ImageDraw
import pandas as pd

# Import functional windows
from Cleaning import DataCleaningApp
from Clustrening import ClusteringApp
from Mining import DataFilterApp
from Predection import PredictionApp
from Visulization import DataVisualizationApp

# Global shared dataframe
shared_df = None

def open_link(url):
    webbrowser.open(url, new=2)

def show_info(task):
    task_info = {
        "Data Cleaning": {
            "description": "🧹 Data cleaning is the process of identifying and rectifying errors or inconsistencies in datasets.",
            "link": "https://www.tableau.com/learn/articles/what-is-data-cleaning"
        },
        "Visualization": {
            "description": "📊 Data visualization is the graphical representation of data. It helps to identify patterns and insights.",
            "link": "https://www.restack.io/p/data-centric-product-development-answer-data-visualization-techniques-cat-ai"
        },
        "Mining": {
            "description": "⛏️ Data mining involves extracting useful patterns or knowledge from large datasets.",
            "link": "https://www.investopedia.com/terms/d/datamining.asp"
        },
        "Prediction": {
            "description": "🔮 Prediction involves forecasting future values based on past data using models like Linear Regression or Time Series.",
            "link": "https://www.ibm.com/think/topics/linear-regression"
        },
        "Clustering": {
            "description": "🧠 Clustering is the process of grouping similar data points into clusters. K-means is a common clustering algorithm.",
            "link": "https://www.tpointtech.com/clustering-in-machine-learning"
        }
    }

    info = task_info.get(task)
    if info:
        info_window = tk.Toplevel()
        info_window.title(f"{task} Information")
        info_window.geometry("550x320")
        info_window.configure(bg="#dff9fb")

        # Header block
        header = tk.Frame(info_window, bg="#6ab04c", height=50)
        header.pack(fill="x")
        title = tk.Label(header, text=f"📘 {task} Information", font=("Helvetica", 16, "bold"), bg="#6ab04c", fg="white")
        title.pack(pady=10)

        # Main content
        content = tk.Frame(info_window, bg="#f6f6f6", padx=20, pady=20)
        content.pack(expand=True, fill="both")

        desc_label = tk.Label(content, text=info["description"], font=("Arial", 12), bg="#f6f6f6", wraplength=480, justify="left", fg="#2c3e50")
        desc_label.pack(pady=10)

        # Styled link
        link_label = tk.Label(content, text="🌐 Learn more here", font=("Arial", 12, "underline"), fg="#2980b9", cursor="hand2", bg="#f6f6f6")
        link_label.pack(pady=10)

        def on_hover_link(e):
            link_label.config(fg="#1abc9c")

        def on_leave_link(e):
            link_label.config(fg="#2980b9")

        link_label.bind("<Button-1>", lambda e: open_link(info["link"]))
        link_label.bind("<Enter>", on_hover_link)
        link_label.bind("<Leave>", on_leave_link)

        # Close button
        close_btn = tk.Button(content, text="Close ❌", command=info_window.destroy,
                              font=("Arial", 11, "bold"), bg="#eb4d4b", fg="white", relief="flat",
                              activebackground="#ff7979", cursor="hand2")
        close_btn.pack(pady=10)

def resize_bg(event):
    global bg_image, bg_photo
    new_width = event.width
    new_height = event.height
    resized = bg_image.resize((new_width, new_height), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(resized)
    background_label.config(image=bg_photo)

def on_enter(e): 
    e.widget['background'] = '#2980b9'
def on_leave(e): 
    e.widget['background'] = '#3498db'
def on_info_enter(e): 
    e.widget['background'] = '#27ae60'
def on_info_leave(e): 
    e.widget['background'] = '#2ecc71'

# Function to display About Us information
def show_about_us():
    about_window = tk.Toplevel()
    about_window.title("About Us")
    about_window.geometry("700x500")  # Increased the window size for better visibility
    about_window.configure(bg="#f9e79f")

    # Header Section
    header = tk.Frame(about_window, bg="#f39c12", height=60)
    header.pack(fill="x")
    title = tk.Label(header, text="About Us", font=("Helvetica", 18, "bold"), bg="#f39c12", fg="white")
    title.pack(pady=10)

    # Content Section
    content = tk.Frame(about_window, bg="#f6f6f6", padx=20, pady=20)
    content.pack(expand=True, fill="both")

    # Description Section
    desc_text = (
        "SmartData Hub is a Data Science Operations tool designed to assist in Data Cleaning, "
        "Visualization, Mining, Prediction, and Clustering.\nWe aim to provide a powerful platform "
        "for data analysis and modeling. The tool supports various machine learning models, visualization, "
        "and real-time results to enhance your data processing workflow."
    )

    desc_label = tk.Label(content, text=desc_text,
                          font=("Arial", 12), bg="#f6f6f6", wraplength=640, justify="left", fg="#2c3e50")
    desc_label.pack(pady=15)

    # Creator's Section
    creators_label = tk.Label(content, text="Created By:",
                               font=("Arial", 14, "bold"), bg="#f6f6f6", fg="#2c3e50")
    creators_label.pack(pady=15)

    # Creator's Images Section
    creators_images = [
        {"name": "Shubham Sontakke", "image": "shubham.png"},
        {"name": "Dnyanraj Aher", "image": "dnyanraj.jpg"},
        {"name": "Mahesh Pethe", "image": "mahesh.png"},
        {"name": "Tanisha Patre", "image": "tanisha.jpg"}
    ]

    image_frame = tk.Frame(content, bg="#f6f6f6")
    image_frame.pack(pady=20)

    for i, creator in enumerate(creators_images):
        # Add images with rounded corners
        creator_img = Image.open(creator["image"]).resize((100, 100))  # Resize image
        creator_img = creator_img.convert("RGBA")
        
        # Create a circular mask for the image
        mask = Image.new("L", (100, 100), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 100, 100), fill=255)
        creator_img.putalpha(mask)
        
        creator_img = ImageTk.PhotoImage(creator_img)

        creator_photo = tk.Label(image_frame, image=creator_img, bg="#f6f6f6")
        creator_photo.image = creator_img  # Keep a reference to the image
        creator_photo.grid(row=0, column=i, padx=20)

        creator_name_label = tk.Label(image_frame, text=creator["name"], font=("Arial", 12), bg="#f6f6f6", fg="#2c3e50")
        creator_name_label.grid(row=1, column=i, pady=5)

    # Guide Section
    guide_name = tk.Label(content, text="Guided By: Dr. Devidas S. Thosar\nDr. Deepika Ajalkar", font=("Arial", 12),
                          bg="#f6f6f6", fg="#2c3e50")
    guide_name.pack(pady=10)

    # Contact Information
    contact_label = tk.Label(content, text="Contact:\nPhone: 7666740724\nEmail: 85prasadjain@gmail.com", font=("Arial", 12),
                             bg="#f6f6f6", fg="#2c3e50")
    contact_label.pack(pady=10)

    # Close Button
    close_btn = tk.Button(content, text="Close ❌", command=about_window.destroy,
                          font=("Arial", 11, "bold"), bg="#eb4d4b", fg="white", relief="flat",
                          activebackground="#ff7979", cursor="hand2")
    close_btn.pack(pady=20)

# Load a file (CSV, Excel, Word, PDF) and store it globally
def load_file():
    global shared_df
    file_path = filedialog.askopenfilename(
        filetypes=[
            ("Supported Files", "*.csv *.xlsx *.xls *.docx *.pdf"),
            ("All Files", "*.*")
        ]
    )
    if file_path:
        try:
            if file_path.endswith('.csv'):
                shared_df = pd.read_csv(file_path)
            elif file_path.endswith(('.xlsx', '.xls')):
                shared_df = pd.read_excel(file_path)
            elif file_path.endswith('.docx'):
                import docx
                doc = docx.Document(file_path)
                data = []
                for table in doc.tables:
                    for row in table.rows:
                        data.append([cell.text for cell in row.cells])
                if data:
                    shared_df = pd.DataFrame(data[1:], columns=data[0])  # First row as header
                else:
                    raise ValueError("No table found in the Word document.")
            elif file_path.endswith('.pdf'):
                import tabula
                dfs = tabula.read_pdf(file_path, pages='all', multiple_tables=True)
                if dfs:
                    shared_df = dfs[0]  # Take the first table
                else:
                    raise ValueError("No table found in the PDF document.")
            else:
                raise ValueError("Unsupported file format selected.")
            messagebox.showinfo("Success", f"File loaded successfully: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{e}")

# Launch functional window with shared DataFrame
def launch_task_window(task):
    if shared_df is None:
        messagebox.showwarning("⚠️ Warning", "Please load a file first.")
        return

    new_window = tk.Toplevel(root)
    if task == "Data Cleaning":
        DataCleaningApp(new_window, shared_df.copy())
    elif task == "Visualization":
        DataVisualizationApp(new_window, shared_df.copy())
    elif task == "Mining":
        DataFilterApp(new_window, shared_df.copy())
    elif task == "Prediction":
        PredictionApp(new_window, shared_df.copy())
    elif task == "Clustering":
        ClusteringApp(new_window, shared_df.copy())

# Main window setup
root = tk.Tk()
root.title("Data Science Operations")
root.geometry("900x600")

bg_image = Image.open("clean.jpg")
bg_photo = ImageTk.PhotoImage(bg_image)
background_label = tk.Label(root, image=bg_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

main_frame = tk.Frame(root, bg="#ffffff", bd=0)
main_frame.place(relx=0.5, rely=0.5, anchor="center")

title_label = tk.Label(main_frame, text="🌟 Data Science Operations 🌟", font=("Helvetica", 22, "bold"), bg="#ffffff", fg="#2c3e50")
title_label.pack(pady=20)

# Load File button
load_button = tk.Button(main_frame, text="📂 Load File", font=("Arial", 13), bg="#2ecc71", fg="white",
                        width=20, relief="flat", bd=0, activebackground="#27ae60", cursor="hand2", command=load_file)
load_button.pack(pady=10)

# Feature buttons
tasks = ["Data Cleaning", "Visualization", "Mining", "Prediction", "Clustering"]

for task in tasks:
    button_frame = tk.Frame(main_frame, bg="#ffffff")
    button_frame.pack(pady=7)

    operation_button = tk.Button(button_frame, text=task, font=("Arial", 14), bg="#3498db", fg="white",
                                 width=20, relief="flat", bd=0, activebackground="#2980b9", cursor="hand2",
                                 command=lambda t=task: launch_task_window(t))
    operation_button.pack(side="left", padx=10)
    operation_button.bind("<Enter>", on_enter)
    operation_button.bind("<Leave>", on_leave)

    info_button = tk.Button(button_frame, text="i", font=("Arial", 12, "bold"), bg="#2ecc71", fg="white",
                            width=3, relief="flat", bd=0, command=lambda t=task: show_info(t), cursor="hand2")
    info_button.pack(side="left")
    info_button.bind("<Enter>", on_info_enter)
    info_button.bind("<Leave>", on_info_leave)

# About Us button
about_button = tk.Button(main_frame, text="About Us", font=("Arial", 13), bg="#f39c12", fg="white",
                         width=20, relief="flat", bd=0, activebackground="#e67e22", cursor="hand2", command=show_about_us)
about_button.pack(pady=10)

root.bind("<Configure>", resize_bg)
root.mainloop()
