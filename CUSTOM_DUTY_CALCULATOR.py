import tkinter as tk
from tkinter import ttk, messagebox
from fpdf import FPDF

class CustomsDutyCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Customs Duty Calculator")
        self.root.geometry("600x700")
        self.root.configure(bg="#f0f0f0")

        self.valid_hs_codes = {
            "Vehicles": "8703",
            "Pharmaceutical Goods": "3006",
            "Laptop, Mobile Phones, Desktop and Personal Computers": "8471",
            "Printers, Keyboards, USB Devices": "8528",
            "Precious Metals": "7113",
            "Toy Items": "9503"
        }

        self.setup_ui()

    def setup_ui(self):
        # Title
        tk.Label(self.root, text="Customs Duty Calculator", font=("Helvetica", 24, "bold"), bg="#f0f0f0", fg="#000080").pack(pady=20)

        # Main frame
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Type of Goods
        tk.Label(main_frame, text="Type of Goods (HS Code):", font=("Helvetica", 12), bg="#f0f0f0").pack(anchor="w", pady=5)
        self.hs_code_entry = tk.Entry(main_frame, font=("Helvetica", 12), width=30)
        self.hs_code_entry.pack(fill="x", pady=5)

        # Value of Goods
        tk.Label(main_frame, text="Value of Goods (in local currency):", font=("Helvetica", 12), bg="#f0f0f0").pack(anchor="w", pady=5)
        self.value_entry = tk.Entry(main_frame, font=("Helvetica", 12), width=30)
        self.value_entry.pack(fill="x", pady=5)

        # Shipping Cost
        tk.Label(main_frame, text="Shipping Cost:", font=("Helvetica", 12), bg="#f0f0f0").pack(anchor="w", pady=5)
        self.shipping_entry = tk.Entry(main_frame, font=("Helvetica", 12), width=30)
        self.shipping_entry.pack(fill="x", pady=5)

        # Insurance Cost
        tk.Label(main_frame, text="Insurance Cost:", font=("Helvetica", 12), bg="#f0f0f0").pack(anchor="w", pady=5)
        self.insurance_entry = tk.Entry(main_frame, font=("Helvetica", 12), width=30)
        self.insurance_entry.pack(fill="x", pady=5)

        # Basic Customs Duty Rate
        tk.Label(main_frame, text="Basic Customs Duty Rate (%):", font=("Helvetica", 12), bg="#f0f0f0").pack(anchor="w", pady=5)
        self.bcd_rate_entry = tk.Entry(main_frame, font=("Helvetica", 12), width=30)
        self.bcd_rate_entry.pack(fill="x", pady=5)

        # IGST Rate
        tk.Label(main_frame, text="IGST Rate (%):", font=("Helvetica", 12), bg="#f0f0f0").pack(anchor="w", pady=5)
        self.igst_rate = tk.StringVar()
        igst_options = ["0%", "5%", "12%", "18%", "28%"]
        self.igst_rate_combo = ttk.Combobox(main_frame, textvariable=self.igst_rate, values=igst_options, state="readonly", font=("Helvetica", 12))
        self.igst_rate_combo.set("18%")  # Default value
        self.igst_rate_combo.pack(fill="x", pady=5)

        # Calculate button
        calculate_button = tk.Button(main_frame, text="Calculate", command=self.calculate, bg="#007bff", fg="white",
                                     font=("Helvetica", 12, "bold"))
        calculate_button.pack(pady=20)

        # Result frame with scrollbar
        self.result_frame = tk.Frame(main_frame, bg="white", bd=2, relief="ridge")
        self.result_frame.pack(fill="both", expand=True, pady=20)

        self.canvas = tk.Canvas(self.result_frame, bg="white")
        self.scrollbar = tk.Scrollbar(self.result_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="white")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Convert to PDF button
        pdf_button = tk.Button(main_frame, text="Convert to PDF", command=self.convert_to_pdf, bg="#28a745", fg="white",
                               font=("Helvetica", 12, "bold"))
        pdf_button.pack(pady=10)

    def calculate(self):
        try:
            hs_code = self.hs_code_entry.get()
            if hs_code not in self.valid_hs_codes.values():
                messagebox.showerror("Error", "Invalid HS Code. Please enter a valid HS Code.")
                return

            value_of_goods = float(self.value_entry.get())
            shipping_cost = float(self.shipping_entry.get())
            insurance_cost = float(self.insurance_entry.get())
            bcd_rate = float(self.bcd_rate_entry.get()) / 100
            igst_rate = float(self.igst_rate.get().strip('%')) / 100

            # Example calculation logic (these rates would need to be customized for the specific country and regulations)
            cess_rate = 0.03  # Cess rate

            bcd = value_of_goods * bcd_rate
            subtotal = value_of_goods + bcd + shipping_cost + insurance_cost
            igst = subtotal * igst_rate
            cess = subtotal * cess_rate
            total_duty = bcd + igst + cess

            # Clear previous results
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()

            # Display results
            tk.Label(self.scrollable_frame, text="Breakdown of Customs Duty", font=("Helvetica", 14, "bold"), bg="white").pack(pady=10)
            self.create_result_row("Basic Customs Duty (BCD):", bcd)
            self.create_result_row("Integrated GST (IGST):", igst)
            self.create_result_row("Cess:", cess)
            self.create_result_row("Total Customs Duty:", total_duty)

            # Store the result for PDF conversion
            self.results = {
                "Basic Customs Duty (BCD)": bcd,
                "Integrated GST (IGST)": igst,
                "Cess": cess,
                "Total Customs Duty": total_duty
            }

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for the amounts and BCD rate.")

    def create_result_row(self, label_text, value):
        frame = tk.Frame(self.scrollable_frame, bg="white")
        frame.pack(fill="x", pady=5)
        tk.Label(frame, text=label_text, font=("Helvetica", 10), bg="white").pack(side="left")
        value_label = tk.Label(frame, text=f"₹ {value:.2f}", font=("Helvetica", 10, "bold"), bg="white")
        value_label.pack(side="right")

    def convert_to_pdf(self):
        if not hasattr(self, 'results') or not self.results:
            messagebox.showerror("Error", "No results to convert. Please calculate customs duty first.")
            return

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Breakdown of Customs Duty", ln=True, align='C')
        pdf.ln(10)

        for key, value in self.results.items():
            pdf.cell(200, 10, txt=f"{key}: ₹ {value:.2f}", ln=True)

        pdf.output("Customs_Duty_Breakdown.pdf")
        messagebox.showinfo("Success", "PDF has been created successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CustomsDutyCalculator(root)
    root.mainloop()
