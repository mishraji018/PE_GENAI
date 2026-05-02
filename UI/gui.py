
import tkinter as tk

#Create window
root = tk.Tk()

#Set title
root.title("Empty Window")

#set size
root.geometry("400x300")

# def add():
#     a=10
#     b=20
#     lbl.config(text=a+b)

def Counterdata():
    old_count=lbl.cget("text")
    lbl.config(text=old_count+1)
    lbl.config(text="")

btn=tk.Button(root, text="Click Me", command=add)
btn.pack()

lbl=tk.Label(text="Hello, World!")
lbl.pack()

clr=tk.Button(root, text="Clear", command=Counterdata)
clr.pack()

#run window
root.mainloop()
