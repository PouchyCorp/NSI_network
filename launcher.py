import os
import tkinter as tk
import subprocess

import tkinter as tk

def launch():
    ip = e1.get()
    port = e2.get()
    subprocess.Popen("python client.py "+ip+" "+port)

master = tk.Tk()
tk.Label(master, 
         text="IP").grid(row=0)
tk.Label(master, 
         text="PORT").grid(row=1)

e1 = tk.Entry(master)
e2 = tk.Entry(master)
e1.insert(10, '127.0.0.1')
e2.insert(10, '12345')

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)

tk.Button(master, text='Quit', command=master.quit).grid(row=3, column=0, sticky=tk.W, pady=4)
tk.Button(master, text='Run', command=launch).grid(row=3, column=1, sticky=tk.W, pady=4)

tk.mainloop()