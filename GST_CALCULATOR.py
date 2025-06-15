import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import win32print
import win32api
import tempfile
import os
from datetime import datetime


class DetailedGSTInvoice:
    def __init__(self, company_details, customer_details, transportation_details, items, totals):
        self.company_details = company_details
        self.customer_details = customer_details
        self.transportation_details = transportation_details
        self.items = items
        self.totals = totals

    def generate_pdf(self, filename):
        doc = SimpleDocTemplate(filename, pagesize=A4, leftMargin=0.5 * inch, rightMargin=0.5 * inch,
                                topMargin=0.5 * inch, bottomMargin=0.5 * inch)
        elements = []

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='CenterAlign', alignment=1, fontSize=16, fontName="Helvetica-Bold"))
        styles.add(ParagraphStyle(name='LeftAlign', alignment=0, fontSize=10, fontName="Helvetica"))
        styles.add(ParagraphStyle(name='RightAlign', alignment=2, fontSize=10, fontName="Helvetica"))

        # Title
        elements.append(Paragraph("GST INVOICE RECEIPT", styles['CenterAlign']))
        elements.append(Spacer(1, 0.2 * inch))

        # Company and Transportation details
        data = [
            [Paragraph(f"<b>{self.company_details['name']}</b>", styles['LeftAlign']),
             Paragraph("<b>Transportation Mode:</b> Apply for Supply of Goods", styles['LeftAlign'])],
            [f"GSTIN: {self.company_details['gstin']}", f"Vehicle No.: {self.transportation_details['vehicle_no']}"],
            [f"Address: {self.company_details['address']}",
             f"Date and Time of Supply: {self.transportation_details['supply_date']}"],
            [f"Serial No. of Invoice: {self.company_details['invoice_no']}",
             f"Place of Supply: {self.transportation_details['supply_place']}"],
            [f"Date of Invoice: {self.company_details['invoice_date']}", ""]
        ]
        t = Table(data, colWidths=[doc.width / 2 - 6, doc.width / 2 - 6])
        t.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 0.2 * inch))

        # Customer details
        data = [
            ["Details of Receiver (Billed to)", "Details of Consignee (Shipped to)"],
            [f"Name: {self.customer_details['name']}", f"Name: {self.customer_details['ship_name']}"],
            [f"Address: {self.customer_details['address']}", f"Address: {self.customer_details['ship_address']}"],
            [f"State: {self.customer_details['state']}", f"State: {self.customer_details['ship_state']}"],
            [f"State Code: {self.customer_details['state_code']}",
             f"State Code: {self.customer_details['ship_state_code']}"],
            [f"GSTIN/Unique ID: {self.customer_details['gstin']}",
             f"GSTIN/Unique ID: {self.customer_details['ship_gstin']}"]
        ]
        t = Table(data, colWidths=[doc.width / 2 - 6, doc.width / 2 - 6])
        t.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 0.2 * inch))

        # Items
        data = [
            ["Sr. No.", "Description", "HSN", "Qty.", "Unit", "Rate", "Total", "Discount", "Taxable", "CGST", "SGST",
             "IGST"]]
        for idx, item in enumerate(self.items, start=1):
            data.append([
                idx,
                item['description'],
                item['hsn'],
                item['qty'],
                item['unit'],
                f"₹{item['rate']:.2f}",
                f"₹{item['total']:.2f}",
                f"₹{item['discount']:.2f}",
                f"₹{item['taxable_value']:.2f}",
                f"{item['cgst_rate']}%\n₹{item['cgst_amount']:.2f}",
                f"{item['sgst_rate']}%\n₹{item['sgst_amount']:.2f}",
                f"{item['igst_rate']}%\n₹{item['igst_amount']:.2f}"
            ])

        # Adjust these widths to fit your page and content
        col_widths = [0.5 * cm, 3 * cm, 1 * cm, 0.8 * cm, 0.8 * cm, 1.5 * cm, 1.5 * cm, 1.5 * cm, 1.5 * cm, 1.5 * cm,
                      1.5 * cm, 1.5 * cm]
        t = Table(data, colWidths=col_widths)
        t.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),  # Reduce font size if needed
            ('TOPPADDING', (0, 0), (-1, -1), 1),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 0.2 * inch))

        # Totals
        elements.append(
            Paragraph(f"Total Invoice Value (In figure): ₹{self.totals['total_value']:.2f}", styles['RightAlign']))
        elements.append(
            Paragraph(f"Total Invoice Value (In Words): {self.totals['total_in_words']}", styles['RightAlign']))
        elements.append(Paragraph(f"Amount of Tax subject to Reverse Charges: ₹{self.totals['reverse_charge']:.2f}",
                                  styles['RightAlign']))
        elements.append(Spacer(1, 0.2 * inch))

        # Declaration and Signature
        elements.append(Paragraph("Declaration:", styles['LeftAlign']))
        elements.append(Paragraph(
            "We declare that this invoice shows the actual price of the goods described and that all particulars are true and correct.",
            styles['LeftAlign']))
        elements.append(Spacer(1, 0.5 * inch))
        elements.append(Paragraph("Signature:", styles['RightAlign']))
        elements.append(Paragraph("Name of the Signatory:", styles['RightAlign']))
        elements.append(Paragraph("Designation / Status:", styles['RightAlign']))

        doc.build(elements)


class GSTCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("GST Calculator")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        self.gst_arr = [3, 5, 12, 18, 28]
        self.gst_type = tk.StringVar(value="exclusive")
        self.gst_percent = tk.StringVar(value="5%")
        self.amount = tk.StringVar()
        self.profit_ratio = tk.StringVar(value="0")
        self.total_selling_price = tk.StringVar(value="0.00")
        self.total_profit = tk.StringVar(value="₹ 0.00")
        self.total_gst = tk.StringVar(value="₹ 0.00")

        self.setup_ui()

    def setup_ui(self):
        # Title
        tk.Label(self.root, text="GST Calculator", font=("Helvetica", 24, "bold"), bg="#f0f0f0", fg="#000080").pack(
            pady=20)

        # Subtitle
        tk.Label(self.root, text="The easiest way for businesses to calculate their GST", font=("Helvetica", 12),
                 bg="#f0f0f0").pack()

        # Main frame
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Left frame
        left_frame = tk.Frame(main_frame, bg="#f0f0f0")
        left_frame.pack(side="left", fill="both", expand=True)

        # GST Type selector
        gst_type_frame = tk.Frame(left_frame, bg="#f0f0f0")
        gst_type_frame.pack(fill="x", pady=10)
        tk.Radiobutton(gst_type_frame, text="Exclusive of GST", variable=self.gst_type, value="exclusive", bg="#f0f0f0",
                       command=self.update_input_label).pack(side="left")
        tk.Radiobutton(gst_type_frame, text="Inclusive of GST", variable=self.gst_type, value="inclusive", bg="#f0f0f0",
                       command=self.update_input_label).pack(side="left", padx=(20, 0))

        # Cost of Goods / Services
        self.price_label = tk.Label(left_frame, text="Pre-GST Price:", font=("Helvetica", 12), bg="#f0f0f0")
        self.price_label.pack(anchor="w", pady=(10, 5))
        self.price_entry = tk.Entry(left_frame, textvariable=self.amount, font=("Helvetica", 12), width=30)
        self.price_entry.pack(fill="x", pady=5)

        # Add Profit Ratio
        profit_frame = tk.Frame(left_frame, bg="#f0f0f0")
        profit_frame.pack(fill="x", pady=5)
        tk.Label(profit_frame, text="Profit Ratio (%):", font=("Helvetica", 12), bg="#f0f0f0").pack(side="left")
        tk.Entry(profit_frame, textvariable=self.profit_ratio, font=("Helvetica", 12), width=10).pack(side="left",
                                                                                                      padx=5)

        # Select GST Rate
        tk.Label(left_frame, text="Select GST Rate", font=("Helvetica", 12), bg="#f0f0f0").pack(anchor="w",
                                                                                                pady=(10, 5))
        self.gst_percent_combobox = ttk.Combobox(left_frame, values=[f"{rate}%" for rate in self.gst_arr], width=10,
                                                 state='readonly')
        self.gst_percent_combobox.set("5%")
        self.gst_percent_combobox.pack(pady=5)

        # Calculate button
        calculate_button = tk.Button(left_frame, text="Calculate", command=self.calculate, bg="#007bff", fg="white",
                                     font=("Helvetica", 12, "bold"))
        calculate_button.pack(pady=20)

        # Right frame (Results)
        right_frame = tk.Frame(main_frame, bg="white", bd=2, relief="ridge")
        right_frame.pack(side="right", fill="both", expand=True, padx=(20, 0))

        tk.Label(right_frame, text="Total Selling Price will be", font=("Helvetica", 12), bg="white").pack(pady=(10, 0))
        tk.Label(right_frame, textvariable=self.total_selling_price, font=("Helvetica", 36, "bold"), bg="white",
                 fg="#007bff").pack()

        result_frame = tk.Frame(right_frame, bg="white")
        result_frame.pack(fill="x", pady=20, padx=20)

        self.pre_gst_value = self.create_result_field(result_frame, "Pre-GST Price:")
        self.profit_value = self.create_result_field(result_frame, "Profit Amount:")
        self.post_gst_value = self.create_result_field(result_frame, "Post-GST Price:")
        self.gst_value = self.create_result_field(result_frame, "GST Amount:")
        self.cgst_value = self.create_result_field(result_frame, "CGST Amount:")
        self.sgst_value = self.create_result_field(result_frame, "SGST Amount:")

        breakup_label = tk.Label(right_frame, text="Check Full Breakup", font=("Helvetica", 10), fg="blue", bg="white",
                                 cursor="hand2")
        breakup_label.pack(pady=10)
        breakup_label.bind("<Button-1>", lambda e: self.show_full_breakup())

        # Add Enter Invoice Details button
        invoice_button = tk.Button(right_frame, text="Enter Invoice Details", command=self.open_invoice_details_window,
                                   bg="#ffc107", fg="black", font=("Helvetica", 10, "bold"))
        invoice_button.pack(pady=10)

    def create_result_field(self, parent, label):
        frame = tk.Frame(parent, bg="white")
        frame.pack(fill='x', pady=5)
        tk.Label(frame, text=label, bg="white").pack(side=tk.LEFT)
        entry = tk.Entry(frame, state='readonly', width=15)
        entry.pack(side=tk.RIGHT)
        return entry

    def update_input_label(self):
        if self.gst_type.get() == "exclusive":
            self.price_label.config(text="Pre-GST Price:")
        else:
            self.price_label.config(text="Post-GST Price:")

    def calculate(self):
        try:
            gst_percent = float(self.gst_percent_combobox.get().replace("%", ""))
            input_price = float(self.amount.get())
            profit_ratio = float(self.profit_ratio.get()) / 100

            if self.gst_type.get() == "exclusive":
                pre_gst_price = input_price
                profit_amount = pre_gst_price * profit_ratio
                taxable_value = pre_gst_price + profit_amount
                gst_amount = (taxable_value * gst_percent) / 100
                post_gst_price = taxable_value + gst_amount
            else:  # inclusive
                post_gst_price = input_price
                pre_gst_price = (post_gst_price * 100) / (100 + gst_percent)
                profit_amount = pre_gst_price * profit_ratio
                taxable_value = pre_gst_price + profit_amount
                gst_amount = post_gst_price - taxable_value

            self.update_result_field(self.pre_gst_value, pre_gst_price)
            self.update_result_field(self.profit_value, profit_amount)
            self.update_result_field(self.post_gst_value, post_gst_price)
            self.update_result_field(self.gst_value, gst_amount)
            self.update_result_field(self.cgst_value, gst_amount / 2)
            self.update_result_field(self.sgst_value, gst_amount / 2)

            self.total_selling_price.set(f"{post_gst_price:.2f}")
            self.total_gst.set(f"₹ {gst_amount:.2f}")
            self.total_profit.set(f"₹ {profit_amount:.2f}")

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for the price and profit ratio.")

    def update_result_field(self, field, value):
        field.config(state='normal')
        field.delete(0, tk.END)
        field.insert(0, f"{value:.2f}")
        field.config(state='readonly')

    def show_full_breakup(self):
        breakup_window = tk.Toplevel(self.root)
        breakup_window.title("Full Breakup")
        breakup_window.geometry("400x550")
        breakup_window.configure(bg="white")

        tk.Label(breakup_window, text="Invoice", font=("Helvetica", 18, "bold"), bg="white").pack(pady=10)

        frame = tk.Frame(breakup_window, bg="white")
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        headers = ["Item", "Amount"]
        for col, header in enumerate(headers):
            tk.Label(frame, text=header, font=("Helvetica", 12, "bold"), bg="white").grid(row=0, column=col, padx=5,
                                                                                          pady=5, sticky="w")

        items = [
            ("Pre-GST Price", self.pre_gst_value.get()),
            ("Profit Amount", self.profit_value.get()),
            ("Taxable Value", f"{float(self.pre_gst_value.get()) + float(self.profit_value.get()):.2f}"),
            ("GST Amount", self.gst_value.get()),
            ("CGST Amount", self.cgst_value.get()),
            ("SGST Amount", self.sgst_value.get()),
            ("Post-GST Price", self.post_gst_value.get())
        ]

        for row, (item, amount) in enumerate(items, start=1):
            tk.Label(frame, text=item, bg="white").grid(row=row, column=0, padx=5, pady=5, sticky="w")
            tk.Label(frame, text=amount, bg="white").grid(row=row, column=1, padx=5, pady=5, sticky="e")

        tk.Label(breakup_window, text=f"Total Amount: {self.total_selling_price.get()}", font=("Helvetica", 14, "bold"),
                 bg="white").pack(pady=10)

    def open_invoice_details_window(self):
        details_window = tk.Toplevel(self.root)
        details_window.title("Invoice Details")
        details_window.geometry("600x700")
        details_window.configure(bg="#ffffff")

        # Create a main frame
        main_frame = tk.Frame(details_window, bg="#ffffff")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Create a canvas
        canvas = tk.Canvas(main_frame, bg="#ffffff")
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a scrollbar to the canvas
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Create another frame inside the canvas
        inner_frame = tk.Frame(canvas, bg="#ffffff")

        # Add that new frame to a window in the canvas
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        # Title
        tk.Label(inner_frame, text="Invoice Details", font=("Helvetica", 18, "bold"), bg="#ffffff", fg="#007bff").grid(
            row=0, column=0, columnspan=2, pady=10, sticky="w")

        # Company Details
        tk.Label(inner_frame, text="Company Details", font=("Helvetica", 14, "bold"), bg="#ffffff", fg="#28a745").grid(
            row=1, column=0, columnspan=2, pady=(20, 10), sticky="w")

        company_fields = [
            ("Company Name:", "company_name"),
            ("Company GSTIN:", "company_gstin"),
            ("Company Address:", "company_address"),
            ("Invoice Number:", "invoice_no"),
        ]

        for i, (label, var_name) in enumerate(company_fields):
            tk.Label(inner_frame, text=label, bg="#ffffff").grid(row=i + 2, column=0, pady=5, padx=5, sticky="w")
            setattr(self, var_name, tk.StringVar())
            tk.Entry(inner_frame, textvariable=getattr(self, var_name), width=40).grid(row=i + 2, column=1, pady=5,
                                                                                       padx=5, sticky="w")

        # Customer Details
        tk.Label(inner_frame, text="Customer Details", font=("Helvetica", 14, "bold"), bg="#ffffff", fg="#28a745").grid(
            row=len(company_fields) + 2, column=0, columnspan=2, pady=(20, 10), sticky="w")

        customer_fields = [
            ("Customer Name:", "customer_name"),
            ("Customer Address:", "customer_address"),
            ("Customer State:", "customer_state"),
            ("Customer State Code:", "customer_state_code"),
            ("Customer GSTIN:", "customer_gstin"),
        ]

        for i, (label, var_name) in enumerate(customer_fields):
            tk.Label(inner_frame, text=label, bg="#ffffff").grid(row=i + len(company_fields) + 3, column=0, pady=5,
                                                                 padx=5, sticky="w")
            setattr(self, var_name, tk.StringVar())
            tk.Entry(inner_frame, textvariable=getattr(self, var_name), width=40).grid(row=i + len(company_fields) + 3,
                                                                                       column=1, pady=5, padx=5,
                                                                                       sticky="w")

        # Shipping Details
        tk.Label(inner_frame, text="Shipping Details", font=("Helvetica", 14, "bold"), bg="#ffffff", fg="#28a745").grid(
            row=len(company_fields) + len(customer_fields) + 3, column=0, columnspan=2, pady=(20, 10), sticky="w")

        shipping_fields = [
            ("Shipping Name:", "shipping_name"),
            ("Shipping Address:", "shipping_address"),
            ("Shipping State:", "shipping_state"),
            ("Shipping State Code:", "shipping_state_code"),
            ("Shipping GSTIN:", "shipping_gstin"),
        ]

        for i, (label, var_name) in enumerate(shipping_fields):
            tk.Label(inner_frame, text=label, bg="#ffffff").grid(row=i + len(company_fields) + len(customer_fields) + 4,
                                                                 column=0, pady=5, padx=5, sticky="w")
            setattr(self, var_name, tk.StringVar())
            tk.Entry(inner_frame, textvariable=getattr(self, var_name), width=40).grid(
                row=i + len(company_fields) + len(customer_fields) + 4, column=1, pady=5, padx=5, sticky="w")

        # Transportation Details
        tk.Label(inner_frame, text="Transportation Details", font=("Helvetica", 14, "bold"), bg="#ffffff",
                 fg="#28a745").grid(row=len(company_fields) + len(customer_fields) + len(shipping_fields) + 4, column=0,
                                    columnspan=2, pady=(20, 10), sticky="w")

        transportation_fields = [
            ("Vehicle Number:", "vehicle_no"),
            ("Date and Time of Supply:", "supply_date"),
            ("Place of Supply:", "supply_place"),
        ]

        for i, (label, var_name) in enumerate(transportation_fields):
            tk.Label(inner_frame, text=label, bg="#ffffff").grid(
                row=i + len(company_fields) + len(customer_fields) + len(shipping_fields) + 5, column=0, pady=5, padx=5,
                sticky="w")
            setattr(self, var_name, tk.StringVar())
            tk.Entry(inner_frame, textvariable=getattr(self, var_name), width=40).grid(
                row=i + len(company_fields) + len(customer_fields) + len(shipping_fields) + 5, column=1, pady=5, padx=5,
                sticky="w")

        # Buttons
        button_frame = tk.Frame(inner_frame, bg="#ffffff")
        button_frame.grid(
            row=len(company_fields) + len(customer_fields) + len(shipping_fields) + len(transportation_fields) + 5,
            column=0, columnspan=2, pady=20)

        tk.Button(button_frame, text="Save as PDF", command=lambda: self.save_as_pdf(details_window), bg="#28a745",
                  fg="white", font=("Helvetica", 10, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Print PDF", command=lambda: self.print_invoice(details_window), bg="#007bff",
                  fg="white", font=("Helvetica", 10, "bold")).pack(side=tk.LEFT, padx=5)

    def get_user_input(self):
        company_details = {
            "name": self.company_name.get(),
            "gstin": self.company_gstin.get(),
            "address": self.company_address.get(),
            "invoice_no": self.invoice_no.get(),
            "invoice_date": datetime.now().strftime("%Y-%m-%d")
        }

        customer_details = {
            "name": self.customer_name.get(),
            "address": self.customer_address.get(),
            "state": self.customer_state.get(),
            "state_code": self.customer_state_code.get(),
            "gstin": self.customer_gstin.get(),
            "ship_name": self.shipping_name.get(),
            "ship_address": self.shipping_address.get(),
            "ship_state": self.shipping_state.get(),
            "ship_state_code": self.shipping_state_code.get(),
            "ship_gstin": self.shipping_gstin.get()
        }

        transportation_details = {
            "vehicle_no": self.vehicle_no.get(),
            "supply_date": self.supply_date.get(),
            "supply_place": self.supply_place.get()
        }

        return company_details, customer_details, transportation_details

    def generate_detailed_invoice(self):
        company_details, customer_details, transportation_details = self.get_user_input()

        items = [
            {
                "description": "Product A",
                "hsn": "1234",
                "qty": 1,
                "unit": "Nos",
                "rate": float(self.pre_gst_value.get()),
                "total": float(self.post_gst_value.get()),
                "discount": 0,
                "taxable_value": float(self.pre_gst_value.get()) + float(self.profit_value.get()),
                "cgst_rate": float(self.gst_percent_combobox.get().replace("%", "")) / 2,
                "cgst_amount": float(self.cgst_value.get()),
                "sgst_rate": float(self.gst_percent_combobox.get().replace("%", "")) / 2,
                "sgst_amount": float(self.sgst_value.get()),
                "igst_rate": 0,
                "igst_amount": 0
            }
        ]

        totals = {
            "total_value": float(self.total_selling_price.get()),
            "total_in_words": self.number_to_words(float(self.total_selling_price.get())),
            "reverse_charge": 0
        }

        return DetailedGSTInvoice(company_details, customer_details, transportation_details, items, totals)

    def save_as_pdf(self, parent_window):
        file_path = filedialog.asksaveasfilename(parent=parent_window, defaultextension=".pdf",
                                                 filetypes=[("PDF files", "*.pdf")])
        if file_path:
            invoice = self.generate_detailed_invoice()
            invoice.generate_pdf(file_path)
            messagebox.showinfo("Success", f"PDF saved successfully at {file_path}", parent=parent_window)

    def print_invoice(self, parent_window):
        temp_file = tempfile.mktemp(".pdf")
        invoice = self.generate_detailed_invoice()
        invoice.generate_pdf(temp_file)

        printer_name = win32print.GetDefaultPrinter()
        if not printer_name:
            messagebox.showerror("Error", "No default printer found.", parent=parent_window)
            return

        try:
            win32api.ShellExecute(0, "print", temp_file, f'/d:"{printer_name}"', ".", 0)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to print: {str(e)}", parent=parent_window)
        finally:
            try:
                os.remove(temp_file)
            except:
                pass

    def number_to_words(self, number):
        def convert_group(n):
            ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
            tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
            teens = ["Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen",
                     "Nineteen"]

            if len(n) == 1:
                return ones[int(n)]
            elif len(n) == 2:
                if n[0] == '1':
                    return teens[int(n[1])]
                elif n[1] == '0':
                    return tens[int(n[0])]
                else:
                    return tens[int(n[0])] + ' ' + ones[int(n[1])]
            elif len(n) == 3:
                if n == '000':
                    return ''
                elif n[1:] == '00':
                    return ones[int(n[0])] + ' Hundred'
                else:
                    return ones[int(n[0])] + ' Hundred ' + convert_group(n[1:])

        if number == 0:
            return "Zero Rupees"

        rupees = int(number)
        paise = int((number - rupees) * 100)

        result = []
        if rupees:
            crores = convert_group(f"{rupees:012d}"[:3])
            lakhs = convert_group(f"{rupees:012d}"[3:5])
            thousands = convert_group(f"{rupees:012d}"[5:7])
            hundreds = convert_group(f"{rupees:012d}"[7:])

            if crores:
                result.append(f"{crores} Crore")
            if lakhs:
                result.append(f"{lakhs} Lakh")
            if thousands:
                result.append(f"{thousands} Thousand")
            if hundreds:
                result.append(hundreds)

            result = " ".join(result) + " Rupees"

        if paise:
            result += f" and {convert_group(f'{paise:02d}')} Paise"

        return result.strip()

        def print_invoice(self):
            temp_file = tempfile.mktemp(".pdf")
            invoice = self.generate_detailed_invoice()
            invoice.generate_pdf(temp_file)

            printer_name = win32print.GetDefaultPrinter()
            if not printer_name:
                messagebox.showerror("Error", "No default printer found.")
                return

            try:
                win32api.ShellExecute(0, "print", temp_file, f'/d:"{printer_name}"', ".", 0)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to print: {str(e)}")
            finally:
                try:
                    os.remove(temp_file)
                except:
                    pass

        def save_as_pdf(self):
            file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if file_path:
                invoice = self.generate_detailed_invoice()
                invoice.generate_pdf(file_path)
                messagebox.showinfo("Success", f"PDF saved successfully at {file_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = GSTCalculator(root)
    root.mainloop()

