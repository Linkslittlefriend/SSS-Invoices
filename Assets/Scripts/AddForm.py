from tkinter import Label, Entry, Text, Listbox, Checkbutton, IntVar, filedialog
import tkinter as tk
import tkcalendar
from datetime import date, datetime, timedelta
import mysql.connector as connector
import  qrcode
import PIL.ImageTk as ImageTk
import pickle
from Utils import print_with_time #local script
from TextConv import get_text #local script

columns = [
"InvoiceNo",
"CustomerName",
"PhoneNo",
"InvoiceDate",
"InstallationTeam",
"InstallationDate",
"InvoiceProductCategories",
"InvoiceProductIDs",
"WarrantyLastDate",
"IsReplaced",
"ReplacedProductIDs",
"ReplacedDate",
"Comments",
]

class AddRecordWindow(tk.Toplevel):

    
    def __init__(self, parent, connection):
        super().__init__(parent)

        self.geometry('960x720')
        self.title('Add New Record')
        
        self.generate_form(connection)
    
#region methods for fields

    def generate_invoice_no(root, connection):
        # Create an Entry widget for the InvoiceNo column
        invoice_no_entry = Entry(root)
        invoice_no_entry.pack()
        print_with_time("Field created: #1")
        return invoice_no_entry

    def generate_customer_name(root, connection):
        # Create a validation function that checks the length of the entered text
        def validate_customer_name(text):
            return len(text) <= 50

        # Create an Entry widget for the CustomerName column
        customer_name_entry = Entry(root, validate="key", validatecommand=(root.register(validate_customer_name), "%P"))
        customer_name_entry.pack()
        print_with_time("Field created: #2")
        return customer_name_entry

    def generate_phone_no(root, connection):
        # Create a validation function that checks if the entered text starts with +218 and has a length of at most 15 characters
        def validate_phone_no(text):
            return text.startswith("+218") and len(text) <= 15

        # Create an Entry widget for the PhoneNo column
        phone_no_entry = Entry(root, validate="key", validatecommand=(root.register(validate_phone_no), "%P"))
        phone_no_entry.insert(0, "+218")
        phone_no_entry.pack()
        print_with_time("Field created: #3")
        return phone_no_entry

    def generate_invoice_date(root, connection):
        # Create a tkcalendar.DateEntry widget for the InvoiceDate column
        invoice_date_entry = tkcalendar.DateEntry(root, date_pattern='yyyy-mm-dd')
        # Set the default value to the current date
        invoice_date_entry.set_date(date.today())
        invoice_date_entry.config(state= "disabled")
        invoice_date_entry.pack()
        print_with_time("Field created: #4")
        return invoice_date_entry

    def generate_installation_team(root, connection):
        # Create a validation function that checks the length of the entered text
        def validate_installation_team(text):
            return len(text) <= 200

        # Create an Entry widget for the CustomerName column
        installation_team_entry = Entry(root, validate="key", validatecommand=(root.register(validate_installation_team), "%P"))
        installation_team_entry.pack()
        print_with_time("Field created: #5")
        return installation_team_entry

    def generate_installation_date(root, connection):
        # Create a tkcalendar.DateEntry widget for the InvoiceDate column
        installation_date_entry = tkcalendar.DateEntry(root, date_pattern='yyyy-mm-dd')
        installation_date_entry.pack()
        print_with_time("Field created: #6")
        return installation_date_entry

    def generate_invoice_product_categories(root, connection):
        # Create a Listbox widget for the InvoiceProductCategories column
        invoice_product_categories_listbox = Listbox(root, selectmode='multiple', exportselection=False)
        # Query the database to get the list of available product categories
        cursor = connection.cursor()
        query = "SELECT CategoryID, CategoryName FROM categories"
        cursor.execute(query)
        result = cursor.fetchall()
        # Insert the available CategoryName values into the Listbox
        for row in result:
            invoice_product_categories_listbox.insert('end', row[1])
        invoice_product_categories_listbox.pack()
        print_with_time("Field created: #7")
        
        return invoice_product_categories_listbox

    def generate_invoice_product_ids(root, connection):
        # Create an Entry widget for searching
        search_entry = Entry(root)
        search_entry.pack()
        print_with_time("Field created: #8")

        # Create a Listbox widget for the InvoiceProductIDs column
        invoice_product_ids_listbox = Listbox(root, selectmode='multiple', exportselection=False)
        invoice_product_ids_listbox.pack()

        def update_listbox(*args):
            # Save the current selection
            current_selection = [invoice_product_ids_listbox.get(i) for i in invoice_product_ids_listbox.curselection()]

            # Query the database to get the list of available ProductID values
            cursor = connection.cursor()
            query = "SELECT ProductID FROM products"
            cursor.execute(query)
            result = cursor.fetchall()

            # Filter the results based on the search text
            search_text = search_entry.get().lower()
            result = [row for row in result if search_text in row[0].lower()]

            # Update the Listbox with the available ProductID values
            invoice_product_ids_listbox.delete(0, 'end')
            for row in result:
                invoice_product_ids_listbox.insert('end', row[0])

            # Add back any selected values that were removed by filtering
            for value in current_selection:
                if value not in result:
                    invoice_product_ids_listbox.insert('end', value)

            # Restore the previous selection
            for value in current_selection:
                index = invoice_product_ids_listbox.get(0, 'end').index(value)
                invoice_product_ids_listbox.selection_set(index)

        # Update the Listbox whenever the user types in the search box
        search_entry.bind('<KeyRelease>', update_listbox)

        # Update the Listbox initially
        update_listbox()
        
        return invoice_product_ids_listbox

    def generate_is_replaced(root, connection):
        # Create a variable to store the value of the Checkbutton
        global is_replaced_var
        is_replaced_var = IntVar()
        # Create the Checkbutton
        is_replaced_checkbutton = Checkbutton(root, variable=is_replaced_var)
        is_replaced_checkbutton.pack()
        print_with_time("Field created: #10")
        return is_replaced_checkbutton

    def generate_replaced_product_ids(root, connection):
        # Create an Entry widget for searching
        search_entry = Entry(root)
        search_entry.pack()
        print_with_time("Field created: #11")

        # Create a Listbox widget for the InvoiceProductIDs column
        replaced_product_ids_listbox = Listbox(root, selectmode='multiple', exportselection=False)
        replaced_product_ids_listbox.pack()
        print_with_time("Field created: #12")

        def update_listbox(*args):
            # Save the current selection
            current_selection = [replaced_product_ids_listbox.get(i) for i in replaced_product_ids_listbox.curselection()]

            # Query the database to get the list of available ProductID values
            cursor = connection.cursor()
            query = "SELECT ProductID FROM products"
            cursor.execute(query)
            result = cursor.fetchall()

            # Filter the results based on the search text
            search_text = search_entry.get().lower()
            result = [row for row in result if search_text in row[0].lower()]

            # Update the Listbox with the available ProductID values
            replaced_product_ids_listbox.delete(0, 'end')
            for row in result:
                replaced_product_ids_listbox.insert('end', row[0])

            # Add back any selected values that were removed by filtering
            for value in current_selection:
                if value not in result:
                    replaced_product_ids_listbox.insert('end', value)

            # Restore the previous selection
            for value in current_selection:
                index = replaced_product_ids_listbox.get(0, 'end').index(value)
                replaced_product_ids_listbox.selection_set(index)

        # Update the Listbox whenever the user types in the search box
        search_entry.bind('<KeyRelease>', update_listbox)

        # Update the Listbox initially
        update_listbox()
        
        return replaced_product_ids_listbox

    def generate_replaced_date(root, connection):
        # Create a tkcalendar.DateEntry widget for the InvoiceDate column
        replaced_date_entry = tkcalendar.DateEntry(root, date_pattern='yyyy-mm-dd')
        replaced_date_entry.pack()
        return replaced_date_entry

    def generate_comments(root, connection):
        # Create a Text widget for the Comments column
        comments_text = Text(root, height=5, width=40)
        comments_text.pack()
        print_with_time("Field created: #13")

        def enforce_character_limit(event):
            # Delete any extra characters if the length of the text exceeds the character limit
            comments_text.delete("1.0 + 2000 chars", "end")

        # Bind the function to the KeyRelease event
        comments_text.bind("<KeyRelease>", enforce_character_limit)

        return comments_text

    def generate_warranty_last_date(root, connection):
        # Create a tkcalendar.DateEntry widget for the WarrantyLastDate column
        warranty_last_date_entry = tkcalendar.DateEntry(root, date_pattern='yyyy-mm-dd')
        # Set the default value to 2 years from the current date
        warranty_last_date_entry.set_date(date.today() + timedelta(days=365*2))
        warranty_last_date_entry.config(state= "disabled")
        warranty_last_date_entry.pack()
        print_with_time("Field created: #9")
        return warranty_last_date_entry

#endregion

    def generate_form(self, connection):

        print_with_time("Add a new record selected.")

        entries = {}
        labels = []

        # Create a header label
        header_label = tk.Label(self, text=get_text("New_Record","N14"), font=("Helvetica", 20))
        header_label.pack(side="top", pady=10)

        # Create a canvas and a scrollbar
        canvas = tk.Canvas(self)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame to hold the widgets
        frame = tk.Frame(canvas)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Calculate the center coordinates of the canvas
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        center_x = canvas_width // 2
        center_y = canvas_height // 2

        # Add the frame to the canvas
        canvas.create_window((center_x, center_y), window=frame, anchor="n")

        # Create widgets in the column
        for column_name in columns:

            # Get the section and key for the column label from the column_labels dictionary
            section, key = column_labels[column_name]
            
            # Get the label for the column from the JSON data
            label_text = get_text(section,key)

            # Create a label for the column
            label = Label(frame, text=label_text)
            label.pack(side="top", anchor="center", pady=5)
            labels.append(label)

            # Generate the element for the column using the corresponding function
            if column_name in column_generators:
                entry = column_generators[column_name](frame, connection)
                entry.pack(side="top", fill="x", pady=5)
                entries[column_name] = entry
        
        # Submit button - generate errors for value constraints to be implemented
        submit_new_record = tk.Button(frame, text=get_text("New_Record","N15"), command=lambda: self.confirm_submission(entries, connection))
        submit_new_record.pack()

        # Update the scrollregion of the canvas
        frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

        # Add a binding to scroll the canvas with the mouse wheel
        def on_mousewheel(event):
            # Get the widget under the mouse cursor
            widget = canvas.winfo_containing(event.x_root, event.y_root)
            if isinstance(widget, Listbox):
                # If the widget is a Listbox, do not scroll the canvas
                return
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", on_mousewheel)

        # Place the canvas and the scrollbar
        canvas.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.8)
        scrollbar.place(relx=0.9, rely=0.5, anchor="e", relheight=0.8)

        return entries

    def confirm_submission(self, entries, connection):
        # Display a confirmation dialog
        if tk.messagebox.askyesno(get_text("New_Record","N16"),get_text("New_Record","N17"), parent=self):
            # If the user clicked "Yes", call the on_submit_add_record method
            self.on_submit_add_record(entries, connection)

    def on_submit_add_record(self, entries, connection):

        # Validate the data before attempting to execute
        is_valid, message = self.validate_data(entries, connection)
        if not is_valid:
            # Set the title and message of the error message
            error_title = get_text("Messages","E20")
            error_message = message

            # Display the error message
            tk.messagebox.showerror(error_title, error_message, parent=self)
            return

        cursor = connection.cursor()

        # Extract the values entered in the form
        values = []
        for entry in entries.values():
            if isinstance(entry, Listbox):
                selected_values = [entry.get(i) for i in entry.curselection()]
                value = ','.join(selected_values)
                values.append(value)
            elif isinstance(entry, Checkbutton):
                value = is_replaced_var.get()
                values.append(value)
            elif isinstance(entry, Text):
                value = entry.get("1.0", "end").strip()
                values.append(value)
            else:
                value = entry.get()
                values.append(value)

        # Get the invoice number value from the SQL related statements above
        invoice_number = values[0]

        # Generate a QR code
        qr = self.generate_qr_code(invoice_number)

        # Get the image of the QR code
        qr_code_image = qr.make_image(fill_color="black", back_color="white")

        # Resize the image to 75% of its original size
        width, height = qr_code_image.size
        new_width = int(width * 0.75)
        new_height = int(height * 0.75)
        qr_code_image = qr_code_image.resize((new_width, new_height))

        # Get the numerical value of the QR code
        qr_code_value = qr.modules

        def qr_code_value_to_binary(qr_code_value):
            # Serialize the two-dimensional array of boolean values into binary data
            qr_code_bin = pickle.dumps(qr_code_value)
            return qr_code_bin
        
        def binary_to_qr_code_value(qr_code_bin):
            # Deserialize the binary data back into a two-dimensional array of boolean values
            qr_code_value = pickle.loads(qr_code_bin)
            return qr_code_value

        # Convert the QR Code's value to a storable binary format.
        qr_code_binary = qr_code_value_to_binary(qr_code_value)

        # store the binary qr code value
        values.append(qr_code_binary)

        # Insert the values into the database
        query = """
             INSERT INTO invoices (
               InvoiceNo,
               CustomerName,
               PhoneNo,
               InvoiceDate,
               InstallationTeam,
               InstallationDate,
               InvoiceProductCategories,
               InvoiceProductIDs,
               WarrantyLastDate,
               IsReplaced,
               ReplacedProductIDs,
               ReplacedDate,
               Comments,
               QRCode
           ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        try:
            cursor.execute(query, values)
            connection.commit()

            # Clear all elements on the page
            for widget in self.winfo_children():
                widget.destroy()

            print_with_time(f"{connection.user} successfully added a new record with Invoice number: {invoice_number}")

            # Display a message
            message = tk.Label(self, text=get_text("New_Record","N18"))
            message.pack(side="top", pady=10)
            
            # Convert the image to a PhotoImage object and display it in the Label widget
            # Create a Label widget to display the QR code
            qr_code_label = tk.Label(self)
            qr_code_label.pack()
            photo = ImageTk.PhotoImage(qr_code_image)
            qr_code_label.config(image=photo)
            qr_code_label.image = photo

            # Create a button to add another record
            def add_another_record():
                # Clear all elements on the page
                for widget in self.winfo_children():
                    widget.destroy()
                # Call generate_form again
                self.generate_form(connection)

            # Create a button to print_with_time the QR code
            def save_qr_code():
                # Display a file dialog to choose the location and file name for saving the image
                file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])

                # Save the image to the specified location
                if file_path:
                    qr_code_image.save(file_path)

                print_with_time("saved qr code image file at: " + file_path)

            save_button = tk.Button(self, text=get_text("New_Record","N20"), command=save_qr_code)
            save_button.pack(side="top", pady=10)

            add_another_button = tk.Button(self, text=get_text("New_Record","N21"), command=add_another_record)
            add_another_button.pack(side="top", pady=10)

        except connector.Error as err:
            submit_error = get_text("Messages","E20")
            print_with_time(f"{submit_error} error: {err}")
            tk.messagebox.showerror(submit_error, err, parent=self)
        # Close the cursor
        cursor.close()

    def validate_data(self, entries, connection):
        # Add your validation logic here
        
        cursor = connection.cursor()

        # Check if any required fields are empty - NEEDS REWORK
        required_fields = ["InvoiceNo", "CustomerName", "PhoneNo", "InvoiceDate", "InstallationTeam", "InstallationDate", "InvoiceProductCategories", "InvoiceProductIDs"]
        for field in required_fields:
            entry = entries[field]

            # Store Error text
            empty_error = get_text("Messages", "E11")
            fed_empty_error = empty_error.format(field)
            
            if isinstance(entry, tk.Listbox):

                # Handle Listbox widgets
                if entry.size() == 0:
                    return False, fed_empty_error
            elif isinstance(entry, Entry) or isinstance(entry, tkcalendar.DateEntry):
                # Handle Entry and tkcalendar.DateEntry widgets
                if not entry.get().strip():
                    return False, fed_empty_error
        
        #0-------INVOICE NUMBER-------#
        # Check if the InvoiceNo is a valid number
        try:
            invoice_no = int(entries['InvoiceNo'].get())
        except ValueError:
            return False, get_text("Messages", "E12")
        
        # Check if a record with the same InvoiceNo already exists in the database
        query = "SELECT COUNT(*) FROM invoices WHERE InvoiceNo = %s"
        cursor.execute(query, (invoice_no,))
        result = cursor.fetchone()
        if result[0] > 0:
            return False, get_text("Messages", "E13")
        #-------INVOICE NUMBER-------#

        #1-------CUSTOMER NAME--------#
        # left here for future validation
        #-------CUSTOMER NAME--------#

        #2-------PHONE NUMBER--------#
        # left here for future validation
        #-------PHONE NUMBER--------#

        #3-------INVOICE DATE--------#
        # Check if the InvoiceDate is a valid date
        try:
            invoice_date = datetime.strptime(entries['InvoiceDate'].get(), "%Y-%m-%d")
        except ValueError:
            return False, get_text("Messages", "E14")
        
        # Check if the entered date is today's date
        if invoice_date.date() != date.today():
            return False, get_text("Messages", "E15")
        #-------INVOICE DATE--------#

        #-------INSTALLATION TEAM--------#
        # left here for future validation
        #-------INSTALLATION TEAM--------#

        #-------INSTALLATION DATE--------#
        try:
            installation_date = datetime.strptime(entries['InstallationDate'].get(), "%Y-%m-%d")
        except ValueError:
            return False, get_text("Messages", "E16")
        
        # Check if the entered date is today's date or later, cannot be before.
        if installation_date.date() < date.today():
            return False, get_text("Messages", "E17")
        #-------INSTALLATION DATE--------#

        #-------INVOICE PRODUCT CATEGORIES--------#
        # left here for future validation
        #-------INVOICE PRODUCT CATEGORIES--------#

        #-------INVOICE PRODUCT IDS--------#
        # left here for future validation
        #-------INVOICE PRODUCT IDS--------#

        #-------IS REPLACED--------#
        # left here for future validation
        #-------IS REPLACED--------#

        #-------REPLACED PRODUCT IDS--------#
        # left here for future validation
        #-------REPLACED PRODUCT IDS--------#

        #-------REPLACED DATE--------#
        try:
            replaced_date = datetime.strptime(entries['ReplacedDate'].get(), "%Y-%m-%d")
        except ValueError:
            return False, get_text("Messages","E18")
        
        # Check if the entered date is today's date or later, cannot be before.
        if replaced_date.date() < date.today():
            return False, get_text("Messages","E19")
        #-------REPLACED DATE--------#

        #-------COMMENTS--------#
        # left here for future validation
        #-------COMMENTS--------#

        #-------WARRANTY LAST DATE--------#
        # left here for future validation
        #-------WARRANTY LAST DATE--------#

        # Add more validation checks as needed
        return True, ""

    def generate_qr_code(self, invoice_number):
        
        # Generate a QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
    
        # Set the phone numbers, website, and address
        phone_number_1 = "091-969-4000"  # Replace with desired phone number
        phone_number_2 = "091-969-5000"  # Replace with desired phone number
        phone_number_3 = "091-969-8000"  # Replace with desired phone number
        website = "https://smartsolutions.ly/" 
        address = "الظهرة، شارع سعدون السويحلي، طرابلس -  ليبيا" #Replace with address
        
        # Set the Google Maps link
        google_maps_link = f"https://goo.gl/maps/za25u8e6W7KBAXgn6"

        # Prepare the qr code text for json conversion
        qr_message = get_text("Other","O1")

        # Create a string containing all of the data to be encoded in the QR code
        data = qr_message.format(invoice_number,phone_number_1,phone_number_2,phone_number_3,website,address,google_maps_link)
        
        qr.add_data(data)
        qr.make(fit=True)
        
        return qr

    global column_generators, column_labels

    # Create a dictionary to store the section and key for each column
    column_labels = {
        "InvoiceNo": ("New_Record", "N1"),
        "CustomerName": ("New_Record", "N2"),
        "PhoneNo": ("New_Record", "N3"),
        "InvoiceDate": ("New_Record", "N4"),
        "InstallationTeam": ("New_Record", "N5"),
        "InstallationDate": ("New_Record", "N6"),
        "InvoiceProductCategories": ("New_Record", "N7"),
        "InvoiceProductIDs": ("New_Record", "N8"),
        "WarrantyLastDate": ("New_Record", "N9"),
        "IsReplaced": ("New_Record", "N10"),
        "ReplacedProductIDs": ("New_Record", "N11"),
        "ReplacedDate": ("New_Record", "N12"),
        "Comments": ("New_Record", "N13")
    }

    # Create a dictionary to store the form function for each column
    column_generators= {
        "InvoiceNo": generate_invoice_no,
        "CustomerName": generate_customer_name,
        "PhoneNo": generate_phone_no,
        "InvoiceDate": generate_invoice_date,
        "InstallationTeam": generate_installation_team,
        "InstallationDate": generate_installation_date,
        "InvoiceProductCategories": generate_invoice_product_categories,
        "InvoiceProductIDs": generate_invoice_product_ids,
        "WarrantyLastDate": generate_warranty_last_date,
        "IsReplaced": generate_is_replaced,
        "ReplacedProductIDs": generate_replaced_product_ids,
        "ReplacedDate": generate_replaced_date,
        "Comments": generate_comments,
    }
