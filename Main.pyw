import tkinter as tk
from tkinter import messagebox, PhotoImage
import mysql.connector as connector
import ctypes
import os
import sys
import Assets.Scripts.AddForm as AddForm #local script
import Assets.Scripts.ViewForm as ViewForm #local script
import Assets.Scripts.Utils as Utils #local script
import Assets.Scripts.TextConv as txC #local script
from PIL import Image, ImageTk
import configparser
PROCESS_QUERY_INFORMATION = 0x0400
STILL_ACTIVE = 259


global crashcheck

crashcheck = 1

# Define the path to the lock file
lock_file = "Assets/Logs/lock_file"

# Define the Program Title
title_name = "Ver 1.0"

log_file = Utils.open_log_file()
Utils.print_with_time("--Beginning Log--")

#Utils.print_with_time("application opened.")

# Create a ConfigParser object
config = configparser.ConfigParser()

# Check if the config.ini file exists
if os.path.exists("config.ini"):
    # Read the data from the config.ini file
    config.read("config.ini")

    # Get and then set the current language from the configuration data
    config_language = config.get("Settings", "current_language")
    txC.set_language(config_language)
else:

    # Make english the default language
    default_language = "english"

    # Create a new config.ini file with empty values for current_language and last_input
    config.add_section("Settings")
    config.set("Settings", "current_language", default_language)
    config.set("Settings", "IP", '127.0.0.1')
    config.set("Settings", "last_input", "")
    with open("config.ini", "w") as f:
        config.write(f)

    txC.set_language(default_language)

# Check if the lock file exists
if os.path.exists(lock_file):
    # Read the PID from the lock file
    with open(lock_file, "r") as f:
        pid = int(f.read().strip())

    # Check if a process with that PID is still running
    try:
        # Try to open the process with the specified PID
        process_handle = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_INFORMATION, False, pid)
        if process_handle:
            Utils.print_with_time("process_handle")
            # The process was opened successfully, so check its exit code
            exit_code = ctypes.wintypes.DWORD()
            if ctypes.windll.kernel32.GetExitCodeProcess(process_handle, ctypes.byref(exit_code)):
                Utils.print_with_time("exit_code")
                # The exit code was retrieved successfully
                if exit_code.value == STILL_ACTIVE:
                    # The process is still running, so another instance of the application is already running
                    Utils.print_with_time("instance detected")
                    # Find the window with the specified title
                    window_title = title_name
                    hwnd = ctypes.windll.user32.FindWindowW(None, window_title)
                    # Bring the window to the foreground and give it focus
                    if hwnd != 0:

                        # The lock file exists, so alert the user that another instance of the script is already running
                        messagebox.showerror(txC.get_text("Messages","E1"),txC.get_text("Messages","E2"))

                        # reset the crashcheck value when the user exits to confirm a willing closure.
                        crashcheck = 0
                        Utils.print_with_time("||Closing Log||")
                        sys.exit(0)

            # Close the handle to the process
            ctypes.windll.kernel32.CloseHandle(process_handle)

    except OSError:
        pass

# The lock file does not exist or has been overwritten, so create it and write our PID to it
with open(lock_file, "w") as f:
    f.write(str(os.getpid()))

###PRE-PROCESSES~~~~~~~~~~~~~~~~~~~~~~WINDOW PROCESSES###
# Create window Tkinter
window = tk.Tk()
window.configure(bg = 'white')
window.title(title_name)
window.iconbitmap("Assets/Images/SSSlogo.ico")
window.geometry("1024x768")

# Set the minimum size for the window
window.minsize(1024, 768)

login = False

# Create a label widget in Tkinter
#label = tk.Label(window, text="Click the Button to update this Text",
#font=('Calibri 15 bold'))
#label.pack(pady=20)

def clear_window(container):
    for widget in container.winfo_children():
        widget.destroy()

# Create a connection with MySQL server
def create_connection(ip, user_name, user_password):
    global connection, login

    # connection setup to MySQL server
    connection = None
    try:
        connection = connector.connect(
            host=ip,
            user=user_name,
            passwd=user_password,
            database='sssinvoices'
        )
        login = True
        Utils.print_with_time(f"{user_name} Logged in successfully")
        Utils.print_with_time(f"Connection in create_connection: {connection}")
    
    except connector.Error as e:
        Utils.print_with_time(f"Failure To connect. Error: '{e}' has occurred.")

    return connection

# Generate Page to write server credentials
def create_login_page():
    global user_label, host_entry, user_entry, password_entry, submit_button

    # Create a frame widget
    frame = tk.Frame(window, bg='#F7F9FE')
    frame.pack()

    # Load an image and display it on the canvas
    logo_image = PhotoImage(file="Assets/Images/Logo.png")

        # Set the desired size for the images
    desired_width = 300
    desired_height = 300


    # Get the size of the images
    logo_width, logo_height = logo_image.width(), logo_image.height()

    # Calculate the subsampling factor for the add image
    logo_width_factor = logo_width // desired_width
    logo_height_factor = logo_height // desired_height

    # Reduce the size of the logo image
    logo_image = logo_image.subsample(logo_width_factor, logo_height_factor)

    image_label = tk.Label(frame, image=logo_image, bg='#F7F9FE')
    image_label.image = logo_image # Keep a reference to the PhotoImage object
    image_label.pack()

    # Create the login form
    user_label = tk.Label(frame, font="Helvetica 25 bold", text=txC.get_text("Login_page","L1"), fg='#00C3FF', bg='#F7F9FE')
    user_label.pack(pady=20)

    user_entry = tk.Entry(frame)
    user_entry.pack(padx=10)

    # Get the last input from the configuration data
    last_input = config.get("Settings", "last_input")

    # Check if the last input is not empty
    if last_input:
        # Insert the last input into the user_entry widget
        user_entry.insert(0, last_input)

    password_label = tk.Label(frame, font="Helvetica 25 bold", fg='#00C3FF', bg='#F7F9FE', text=txC.get_text("Login_page","L2"))
    password_label.pack(pady=20)

    password_entry = tk.Entry(frame, show="*")
    password_entry.pack()

    def on_return(event):
        on_login_submit()

    password_entry.bind("<Return>", on_return)

    submit_button = tk.Button(frame, font="Calibri 20 bold", text=txC.get_text("Login_page","L3"), bg='#FDC35D', command=on_login_submit)
    submit_button.pack(pady=20)
    
    # Place to write IP for the server
    host_entry = tk.Entry(window)
    host_entry.place(x=0, y=0, anchor="nw")
    
    # Get the IP from the configuration data
    host_input = config.get("Settings", "IP")

    # Check if the IP is not empty
    if host_input:
        # Insert the last input into the host_entry widget
        host_entry.insert(0, host_input)

    # Open the image using the Image class
    globe_image = Image.open("Assets/Images/globe.png")

    # Convert the image to a PhotoImage object using the ImageTk class
    globe_photo = ImageTk.PhotoImage(globe_image)

    # Create a button with the globe image and the text "Language"
    language_button = tk.Button(window, font="Calibri 25 bold", text=txC.get_text("Other","O2"), image=globe_photo, compound="left", command=language_process)

    language_button.image = globe_photo

    # Position the button at the bottom left of the window
    language_button.place(x=0, rely=1.0, anchor="sw")

    Utils.print_with_time("Login page generated")

def language_process():
    # Switch the language first
    txC.switch_language(config)

    # Then clear window elements
    clear_window(window)
    
    # Then re-create the home page
    create_login_page()

# Confirm submission of Login information.
def on_login_submit():
    
    ip = host_entry.get()
    user = user_entry.get()
    password = password_entry.get()

    connection = create_connection(ip, user, password)
    if connection is not None:
        # Update the last input and ip in the configuration data
        config.set("Settings", "IP", host_entry.get())
        config.set("Settings", "last_input", user_entry.get())
        # Write the updated configuration data back to the config.ini file
        with open("config.ini", "w") as f:
            config.write(f)
        messagebox.showinfo(txC.get_text("Messages","E5"),txC.get_text("Messages","E6"))
        window.after(500, switch_main_menu)
    else:
        messagebox.showerror(txC.get_text("Messages","E7"),txC.get_text("Messages","E8"))

# Log out the user and delete all window elements, then generate login page
def switch_log_out():
    global login, connection

    # Clear window elements
    clear_window(window)

    Utils.print_with_time(connection.user + " logged out.")

    # close the connection with the database and flag login false
    connection.close()
    login = False

    # reset to login page
    create_login_page()

# LOGIN ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ MAIN MENU

# happens after login
def create_main_menu():
    global top_left_button, frame, new_page_label, add_image, view_image, add_record, edit_record

    top_left_button = tk.Button(window, text=txC.get_text("Main_Menu","M1"), command=switch_log_out)
    top_left_button.place(x=0, y=0)

    # frame created after log-in to contain and clear page elements with ease.
    frame = tk.Frame(window, bg='white')
    frame.pack(pady = 60)

    # Create a frame to hold the buttons
    button_frame = tk.Frame(frame)

    new_page_label = tk.Label(frame, text=txC.get_text("Main_Menu","M2") , font=("Helvetica 50 bold"), fg='#0077FF', bg = 'white', padx=10, pady=10)
    new_page_label.pack()

    # Load the original images
    add_image = PhotoImage(file="Assets/Images/Add.png")
    view_image = PhotoImage(file="Assets/Images/View.png")

    # Get the size of the images
    add_width, add_height = add_image.width(), add_image.height()
    view_width, view_height = view_image.width(), view_image.height()

    # Set the desired size for the images
    desired_width = 300
    desired_height = 300

    # Calculate the subsampling factor for the add image
    add_width_factor = add_width // desired_width
    add_height_factor = add_height // desired_height

    # Reduce the size of the add image
    add_image = add_image.subsample(add_width_factor, add_height_factor)

    # Calculate the subsampling factor for the view image
    view_width_factor = view_width // desired_width
    view_height_factor = view_height // desired_height

    # Reduce the size of the view image
    view_image = view_image.subsample(view_width_factor, view_height_factor)

    # Create buttons with the resized images
    add_record = tk.Button(button_frame, text=txC.get_text("Main_Menu","M3"), image=add_image, command=create_add_record, bg='#F7F9FE')
    view_record = tk.Button(button_frame, text=txC.get_text("Main_Menu","M4"), padx=5, image=view_image, command=create_view_record, bg='#F7F9FE')

    # Add the buttons to the window
    add_record.pack(side="left", anchor="center")
    view_record.pack(side="left", anchor="center")

    # Center the frame in the middle of the window
    button_frame.pack(anchor="center")


def switch_main_menu():
    
    # Clear window elements
    clear_window(window)

    # afterwards, create the main menu
    create_main_menu()

# MAIN MENU ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ADD RECORD

def create_add_record():
    
    WindowCreate = AddForm.AddRecordWindow(window, connection)


# ADD RECORD ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ EDIT RECORD

def create_view_record():
    WindowCreate = ViewForm.ViewRecords(window, connection)

# Main starts here.

def on_close():
    global crashcheck

    if(login):
        # warn the user to log-out before closing
        messagebox.showerror(txC.get_text("Messages","E3"),txC.get_text("Messages","E4"))
    else:
        crashcheck = 0
        Utils.print_with_time("||Closing Log||")

        if crashcheck == 1:
            Utils.print_with_time("++Warning! Program has crashed or been forcibly closed.++")
        
        # Delete the lock file when the script exits
        os.unlink(lock_file)
        Utils.close_log_file(log_file)
        window.destroy()

create_login_page()

window.protocol("WM_DELETE_WINDOW", on_close)

window.mainloop()