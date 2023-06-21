import tkinter as tk
from Utils import timestamped_print

root = tk.Tk()
label = tk.Label(root, text="Hello, Tkinter!")
label.pack()

print("Test message")

timestamped_print("sequel")

root.mainloop()
