import tkinter as tk
from tkinter import ttk, messagebox

class CompositionSchemeCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Composition Scheme Eligibility Calculator")
        self.root.geometry("500x350")

        # Define colors
        self.bg_color = "#ffffff"  # White background
        self.primary_color = "#007bff"  # Primary color (blue)
        self.secondary_color = "#f0f0f0"  # Secondary color (light gray)

        self.setup_ui()

    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(padx=20, pady=20)

        # Title
        tk.Label(main_frame, text="Composition Scheme Eligibility Calculator", font=("Helvetica", 18, "bold"),
                 bg=self.bg_color, fg=self.primary_color).grid(row=0, columnspan=2, pady=(0, 20))

        # Input 1: Annual Turnover
        tk.Label(main_frame, text="1. Annual Turnover (in Rs.):", font=("Helvetica", 12), bg=self.bg_color).grid(row=1, column=0, sticky="w", pady=10, padx=10)
        self.turnover_entry = tk.Entry(main_frame, font=("Helvetica", 12))
        self.turnover_entry.grid(row=1, column=1, padx=10)

        # Input 2: Nature of Business
        tk.Label(main_frame, text="2. Nature of Business:", font=("Helvetica", 12), bg=self.bg_color).grid(row=2, column=0, sticky="w", pady=10, padx=10)
        self.business_type_var = tk.StringVar()
        self.business_type_combobox = ttk.Combobox(main_frame, textvariable=self.business_type_var,
                                                   values=["Goods", "Services", "Both"], font=("Helvetica", 12))
        self.business_type_combobox.grid(row=2, column=1, padx=10)

        # Input 3: Interstate Sales
        tk.Label(main_frame, text="3. Interstate Sales (Yes/No):", font=("Helvetica", 12), bg=self.bg_color).grid(row=3, column=0, sticky="w", pady=10, padx=10)
        self.interstate_sales_var = tk.StringVar()
        self.interstate_sales_combobox = ttk.Combobox(main_frame, textvariable=self.interstate_sales_var,
                                                      values=["Yes", "No"], font=("Helvetica", 12))
        self.interstate_sales_combobox.grid(row=3, column=1, padx=10)

        # Input 4: GST Registration Status and Type
        tk.Label(main_frame, text="4. GST Registration Status:", font=("Helvetica", 12), bg=self.bg_color).grid(row=4, column=0, sticky="w", pady=10, padx=10)
        self.gst_registered_var = tk.StringVar()
        self.gst_registered_combobox = ttk.Combobox(main_frame, textvariable=self.gst_registered_var,
                                                    values=["Registered Regular", "Registered Composition", "Not Registered"], font=("Helvetica", 12))
        self.gst_registered_combobox.grid(row=4, column=1, padx=10)

        # Button to check eligibility
        self.check_eligibility_button = tk.Button(main_frame, text="Check Eligibility", command=self.check_eligibility,
                                                  bg=self.primary_color, fg="white", font=("Helvetica", 12, "bold"))
        self.check_eligibility_button.grid(row=5, columnspan=2, pady=20)

    def check_eligibility(self):
        try:
            # Get inputs
            turnover = float(self.turnover_entry.get())
            business_type = self.business_type_var.get()
            interstate_sales = self.interstate_sales_var.get()
            gst_registration = self.gst_registered_var.get()

            # Validate turnover input
            if turnover <= 0:
                messagebox.showerror("Error", "Annual Turnover must be greater than zero.")
                return

            # Determine eligibility based on criteria
            if turnover <= 15000000 and business_type in ["Goods", "Both"] and interstate_sales == "No" and gst_registration in ["Registered Regular", "Not Registered"]:
                messagebox.showinfo("Eligibility Result", "You are eligible for Composition Scheme.")
            else:
                # Provide a suggestion based on why they are not eligible
                suggestion = ""
                if turnover > 15000000:
                    suggestion += "Your turnover exceeds the maximum limit for Composition Scheme.\n"
                if business_type not in ["Goods", "Both"]:
                    suggestion += "Composition Scheme is applicable only for businesses dealing in goods or both goods and services.\n"
                if interstate_sales == "Yes":
                    suggestion += "Interstate sales are not allowed under the Composition Scheme.\n"
                if gst_registration == "Registered Composition":
                    suggestion += "You are already registered under the Composition Scheme.\n"

                messagebox.showinfo("Eligibility Result", f"You are not eligible for Composition Scheme.\n\nSuggestions:\n{suggestion}")

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric value for Annual Turnover.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CompositionSchemeCalculator(root)
    root.mainloop()
