import tkinter as tk
from tkinter import messagebox

class GSTOffsetCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("GST Offset Calculator")
        self.root.geometry("700x400")
        self.root.configure(bg="#003366")

        # Title
        tk.Label(self.root, text="GST Offset Calculator", font=("Helvetica", 24, "bold"), bg="#003366", fg="white").pack(pady=20)

        # Table Frame
        table_frame = tk.Frame(self.root, bg="#003366")
        table_frame.pack(pady=20)

        # Table Headings
        headings = ["GST HEAD", "INPUT GST as per GSTR1", "OUTPUT GST as per GSTR3B"]
        for col, heading in enumerate(headings):
            tk.Label(table_frame, text=heading, font=("Helvetica", 14, "bold"), bg="#007bff", fg="white", width=20, wraplength=150, justify="center").grid(row=0, column=col, padx=5, pady=5)

        # Table Inputs
        gst_heads = ["IGST", "CGST", "SGST"]
        self.input_entries = []
        self.output_entries = []

        for row, gst_head in enumerate(gst_heads, start=1):
            tk.Label(table_frame, text=gst_head, font=("Helvetica", 14), bg="#003366", fg="white", width=20, wraplength=150, justify="center").grid(row=row, column=0, padx=5, pady=5)
            input_entry = tk.Entry(table_frame, font=("Helvetica", 14), width=20)
            input_entry.grid(row=row, column=1, padx=5, pady=5)
            self.input_entries.append(input_entry)
            output_entry = tk.Entry(table_frame, font=("Helvetica", 14), width=20)
            output_entry.grid(row=row, column=2, padx=5, pady=5)
            self.output_entries.append(output_entry)

        # Calculate Button
        tk.Button(self.root, text="Calculate", command=self.calculate_gst_offset, bg="#007bff", fg="white", font=("Helvetica", 14)).pack(pady=20)

        # Result Label
        self.result_label = tk.Label(self.root, font=("Helvetica", 16, "bold"), bg="#003366", fg="white")
        self.result_label.pack(pady=10)

    def calculate_gst_offset(self):
        try:
            input_gst = [float(entry.get()) for entry in self.input_entries]
            output_gst = [float(entry.get()) for entry in self.output_entries]

            total_input_gst = sum(input_gst)
            total_output_gst = sum(output_gst)

            gst_payable = total_output_gst - total_input_gst

            if gst_payable > 0:
                result = f"GST to be Paid: ${gst_payable}"
            elif gst_payable < 0:
                result = f"Input Tax Credit left: ${abs(gst_payable)}"
            else:
                result = "No GST to be Paid"

            self.result_label.config(text=result)
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid numbers")

if __name__ == "__main__":
    root = tk.Tk()
    app = GSTOffsetCalculator(root)
    root.mainloop()
