import tkinter as tk
from PIL import ImageTk

root = tk.Tk()
def make_button():
    b = tk.Button(root)
    image = ImageTk.PhotoImage(file="contactos.png")
    b.config(image=image)
    b.image = image
    b.pack()
make_button()
root.mainloop()
