from tkinter import ttk, Frame
import tkinter.font as tkFont
import tkinter as tk
import time
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

class ViewRecords(tk.Toplevel):
    
    def __init__(self, parent, connection):
        super().__init__(parent)

        self.geometry('1350x720')
        self.title('Records')
        
        self.generate_records(connection)
    
    def generate_records(self, connection):
        
        print_with_time("View records selected.")

        # Create a Style object
        style = ttk.Style()

        # Create a custom style for the Treeview widget
        style.theme_use("clam")
        style.configure("Custom.Treeview", background = "white", foreground = "black", rowheight = 50, fieldbackground= "white", borderwidth=1)
        style.configure("Custom.Treeview.Heading", borderwidth=1)

        #change select color
        style.map("Custom.Treeview", background = [('selected', 'blue')])
        style.layout("Custom.Treeview", [('Custom.Treeview.treearea', {'sticky': 'nswe'})])

        # Treeview frame
        tree_frame = Frame(self)
        tree_frame.pack(pady=20)

        # Treeview vertical scrollbar
        tree_yscroll = tk.Scrollbar(tree_frame)
        tree_yscroll.pack(side="right", fill="y") 
        
        # Treeview horizontak scrollbar
        tree_xscroll = tk.Scrollbar(tree_frame, orient="horizontal")
        tree_xscroll.pack(side="bottom", fill="x")

        # Create the Treeview widget
        tree = ttk.Treeview(tree_frame, style="Custom.Treeview", yscrollcommand=tree_yscroll.set, xscrollcommand=tree_xscroll.set, height=12)
        
        # Pack the Treeview widget with fill and expand options
        tree.pack(fill="both", expand=True)

        global last_click_time
        last_click_time = 0
        double_click_threshold = 0.17  # seconds

        def handle_click(col_name):
            global last_click_time
            current_time = time.time()
            if current_time - last_click_time < double_click_threshold:
                handle_double_click(col_name)
            last_click_time = current_time
        
            # Check if the records are already sorted by this column
            if tree.sort_column == col_name:
                # Reverse the sort order
                tree.sort_order = not tree.sort_order
            else:
                # Set the sort column and order
                tree.sort_column = col_name
                tree.sort_order = False

            # Sort the records
            l = [(tree.set(k, col_name), k) for k in tree.get_children('')]
            l.sort(reverse=tree.sort_order)

            # Rearrange the records in the Treeview widget
            for index, (val, k) in enumerate(l):
                tree.move(k, '', index)

        # Add sort_column and sort_order attributes to the Treeview widget
        tree.sort_column = ''
        tree.sort_order = False

        def handle_double_click(column_name):
            # Get the data in the column
            col_data = [tree.set(item, column_name) for item in tree.get_children()]
            
            # Get the font used by the Treeview widget
            font_config = style.lookup("Custom.Treeview", "font")
            
            # Create a Font object with the specified font
            font = tkFont.Font(font=font_config)
            
            # Find the maximum width required to display the data
            max_width = max([font.measure(item) for item in col_data])
            
            # Get the current column width
            current_width = tree.column(column_name, "width")
            
            # Set the column width if the current width is less than max_width
            if current_width < max_width:
                tree.column(column_name, width=max_width + 10)

        # Configure scrollbars so they move
        tree_xscroll.config(command=tree.xview)
        tree_yscroll.config(command=tree.yview)

        # Style tags for record rows
        tree.tag_configure('oddrow', background = "white")
        tree.tag_configure('evenrow', background = "lightgray")

        # Hide the tree column
        tree["show"] = "headings"

        # Define the columns
        tree["columns"] = columns


        # Create a cursor
        cursor = connection.cursor()

        # Execute the SELECT statement
        query = f"SELECT {', '.join(columns)} FROM invoices ORDER BY InvoiceDate DESC"
        cursor.execute(query)

        # Fetch the data
        data = cursor.fetchall()

        # Close the cursor
        cursor.close()
        
        # Counter for rows
        global count
        count = 0

        # Format the columns
        for col in columns:

            # Get the section and key for the column label from the column_labels dictionary
            section, key = column_view_labels[col]
            
            # Get the label for the column from the JSON data
            col_text = get_text(section,key)

            tree.column(col, width=100, stretch=False)
            tree.heading(col, text=col_text, command=lambda c=col: handle_click(c))

        # Add the data to the table
        for row in data:
            if count % 2 == 0:
                tree.insert("", "end", values=row, tags=('evenrow',))
            else:
                tree.insert("", "end", values=row, tags=('oddrow',))
            count += 1
        
        for item in tree.get_children():
            # Get the value of the IsReplaced column for this item
            is_replaced = tree.set(item, "IsReplaced")
            
            # Check if the value is 0 or 1 and convert it to yes or no
            if is_replaced == "0":
                tree.set(item, "IsReplaced", "No")
            elif is_replaced == "1":
                tree.set(item, "IsReplaced", "Yes")

        print_with_time(f"{count} total records called.")

global column_view_labels

# Create a dictionary to store the section and key for each column
column_view_labels = {
    "InvoiceNo": ("View_Records", "V1"),
    "CustomerName": ("View_Records", "V2"),
    "PhoneNo": ("View_Records", "V3"),
    "InvoiceDate": ("View_Records", "V4"),
    "InstallationTeam": ("View_Records", "V5"),
    "InstallationDate": ("View_Records", "V6"),
    "InvoiceProductCategories": ("View_Records", "V7"),
    "InvoiceProductIDs": ("View_Records", "V8"),
    "WarrantyLastDate": ("View_Records", "V9"),
    "IsReplaced": ("View_Records", "V10"),
    "ReplacedProductIDs": ("View_Records", "V11"),
    "ReplacedDate": ("View_Records", "V12"),
    "Comments": ("View_Records", "V13")
}