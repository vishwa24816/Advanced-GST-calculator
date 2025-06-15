import tkinter as tk
from tkinter import ttk, messagebox

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("GST Management System")
        self.root.geometry("800x600")
        self.root.configure(bg="#003366")

        self.gst_data = {
            "0%": [
                "Fresh fruits and vegetables", "Unprocessed grains", "Books and newspapers",
                "Healthcare services", "Education services", "Public transportation services",
                "Hotels and lodges with tariffs below a specified threshold", "Non-AC restaurants"
            ],
            "5%": [
                "Household necessities", "Railways and air travel tickets below certain classes",
                "Ayurvedic, Unani, Siddha, and Homeopathic medicines", "Apparel below certain price",
                "Footwear below certain price", "Cream, skimmed milk powder", "Branded paneer",
                "Frozen vegetables", "Coffee (not instant)", "Tea", "Packed curd", "Insulin",
                "Agro-based products"
            ],
            "12%": [
                "Computers and processed food items", "Mobile phones", "Spectacles and lenses",
                "Umbrellas, sewing machines, and household appliances", "Butter, ghee, cheese",
                "Fruit juices", "Packed coconut water", "Tooth powder", "Ayurvedic medicines"
            ],
            "18%": [
                "Refrigerators and washing machines", "Telecom services", "Mineral water and beverages",
                "Hotels with tariffs above a certain threshold", "AC restaurants", "IT services",
                "Biscuits", "Instant coffee", "Toothpaste", "Hair oil", "Soap", "Industrial intermediaries"
            ],
            "28%": [
                "Automobiles and motorcycles", "High-end motorcycles", "Consumer durables like ACs and refrigerators",
                "Aerated drinks, tobacco products, and luxury items", "Cigarettes and cigars", "Private jets",
                "Perfume", "Makeup", "Deodorants", "Washing machines", "Paints", "Varnishes"
            ]
        }

        self.setup_main_ui()

    def setup_main_ui(self):
        # Title
        tk.Label(self.root, text="GST Management System", font=("Helvetica", 24, "bold"), bg="#003366", fg="white").pack(pady=40)

        # Search frame
        search_frame = tk.Frame(self.root, bg="#003366")
        search_frame.pack(pady=20)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.search_gst)
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=("Helvetica", 14), width=40)
        search_entry.pack(side="left", padx=10)

        # Search button
        search_button = tk.Button(search_frame, text="Search", command=self.search_gst, bg="#007bff", fg="white", font=("Helvetica", 12, "bold"))
        search_button.pack(side="left")

        # Suggestions listbox
        self.suggestions_listbox = tk.Listbox(self.root, font=("Helvetica", 12), bg="white", fg="black", width=60)
        self.suggestions_listbox.pack(pady=20)
        self.suggestions_listbox.bind("<<ListboxSelect>>", self.fill_search_entry)

        # Button frame
        button_frame = tk.Frame(self.root, bg="#003366")
        button_frame.pack(expand=True)

        buttons = [
            ("GST Calculator", self.open_gst_calculator),
            ("GST Setoff Calculator", self.placeholder),
            ("GST Customs Calculator", self.placeholder),
            ("GST Composition Eligibility Calculator", self.placeholder)
        ]

        for text, command in buttons:
            btn = tk.Button(button_frame, text=text, command=command,
                            bg="#007bff", fg="white", font=("Helvetica", 14),
                            width=30, height=1)
            btn.pack(pady=10)

    def open_gst_calculator(self):
        calculator_window = tk.Toplevel(self.root)
        GSTCalculator(calculator_window)

    def placeholder(self):
        messagebox.showinfo("Info", "This feature is not implemented yet.")

    def search_gst(self, *args):
        search_term = self.search_var.get().lower()
        self.suggestions_listbox.delete(0, tk.END)
        if search_term.strip() == "":
            return

        for gst_rate, categories in self.gst_data.items():
            for category in categories:
                if search_term in category.lower():
                    self.suggestions_listbox.insert(tk.END, category)

        if self.suggestions_listbox.size() == 0:
            self.suggestions_listbox.insert(tk.END, "No matching category found.")

    def fill_search_entry(self, event):
        selection = self.suggestions_listbox.get(self.suggestions_listbox.curselection())
        if selection != "No matching category found.":
            messagebox.showinfo("Search Result", f"{selection} falls under {self.get_gst_rate(selection)} GST")

    def get_gst_rate(self, category):
        for gst_rate, categories in self.gst_data.items():
            if category in categories:
                return gst_rate
        return "Unknown"

class GSTCalculator:
    def _init_(self, root):
        self.root = root
        self.root.title("GST Calculator")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()