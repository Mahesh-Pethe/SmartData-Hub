import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import os

class AboutPage:
    def __init__(self, root):
        self.root = root
        self.root.title("About - SmartData Hub")
        self.root.state('zoomed')  # Maximize window

        # Gradient background
        self.bg_color_start = "#4c8bf5"  # Blue gradient
        self.bg_color_end = "#72c2fc"    # Lighter blue
        self.text_color = "#2a3b52"
        self.heading_color = "#1d3e5e"
        self.root.configure(bg=self.bg_color_start)

        self.font_title = ("Segoe UI", 30, "bold")
        self.font_subtitle = ("Segoe UI", 18, "bold")
        self.font_text = ("Segoe UI", 14)

        self.setup_scrollable_frame()
        self.create_about_section()

    def setup_scrollable_frame(self):
        canvas = tk.Canvas(self.root, bg=self.bg_color_start, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)

        self.scroll_frame = tk.Frame(canvas, bg=self.bg_color_start)
        self.scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((self.root.winfo_screenwidth() // 2, 0), window=self.scroll_frame, anchor="n")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_about_section(self):
        # Heading section
        tk.Label(self.scroll_frame, text="SmartData Hub", font=self.font_title,
                 bg=self.bg_color_start, fg=self.heading_color).pack(pady=(30, 10))

        tk.Label(self.scroll_frame,
                 text="A Comprehensive Tool for Data Visualization, Mining, Cleaning & Prediction",
                 font=self.font_text, wraplength=1000, justify="center",
                 bg=self.bg_color_start, fg=self.text_color).pack(pady=(0, 30))

        self.add_image_section([
            {"name": "Shubham Atul Sontakke", "image": "shubham.png"},
            {"name": "Dnyanraj Arvind Aher", "image": "dnyanraj.jpg"},
            {"name": "Mahesh Ramdas Pethe", "image": "mahesh.png"},
            {"name": "Tanisha Chandrakant Patre", "image": "tanisha.jpg"}
        ])

        self.add_text_section("Guided By", "Dr. Devidas S. Thosar\nDr. Deepika Ajalkar")
        self.add_text_section("Contact", "Phone: 7666740724\nEmail: 85prasadjain@gmail.com")

        self.add_text_section("Purpose", 
            "SmartData Hub is your all-in-one data science companion designed for intuitive data preprocessing, "
            "visualization, mining, and prediction.\n\n"
            "✨ Features:\n"
            "• No-code Machine Learning\n"
            "• Real-time Results & Visualizations\n"
            "• Algorithm Understanding\n"
            "• Supports CSV and Excel Inputs\n"
            "• Student & Industry Friendly")

    def add_image_section(self, people):
        team_frame = tk.Frame(self.scroll_frame, bg=self.bg_color_start)
        team_frame.pack(pady=(20, 40))

        tk.Label(team_frame, text="Created By", font=self.font_subtitle,
                 bg=self.bg_color_start, fg=self.heading_color).pack(pady=10)

        image_frame = tk.Frame(team_frame, bg=self.bg_color_start)
        image_frame.pack()

        for i, person in enumerate(people):
            col = tk.Frame(image_frame, bg=self.bg_color_start, padx=25)
            col.grid(row=i // 2, column=i % 2, pady=10)

            img = self.get_circular_image(person["image"], size=(120, 120))
            if img:
                label_img = tk.Label(col, image=img, bg=self.bg_color_start)
                label_img.image = img
                label_img.pack()

            tk.Label(col, text=person["name"], font=self.font_text,
                     bg=self.bg_color_start, fg=self.text_color, wraplength=180, justify="center").pack(pady=5)

    def add_text_section(self, heading, content):
        section = tk.Frame(self.scroll_frame, bg=self.bg_color_start)
        section.pack(pady=15)

        tk.Label(section, text=heading, font=self.font_subtitle,
                 bg=self.bg_color_start, fg=self.heading_color).pack(pady=5)

        tk.Label(section, text=content, font=self.font_text,
                 bg=self.bg_color_start, fg=self.text_color, justify="center").pack()

    def get_circular_image(self, path, size=(100, 100)):
        try:
            if os.path.exists(path):
                img = Image.open(path).resize(size, Image.Resampling.LANCZOS).convert("RGBA")
                mask = Image.new('L', size, 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0) + size, fill=255)
                img.putalpha(mask)

                output = Image.new("RGBA", size, (255, 255, 255, 0))
                output.paste(img, (0, 0), mask)
                return ImageTk.PhotoImage(output)
        except Exception as e:
            print(f"Error loading image {path}: {e}")
        return None
