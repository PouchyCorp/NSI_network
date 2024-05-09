import os
import tkinter as tk
import subprocess
from random import randint
import tkinter as tk

def launch():
    ip = e1.get()
    port = e2.get()
    playername = e3.get()
    #subprocess.Popen("python client.py "+ip+" "+port)
    subprocess.Popen("client.py "+str(ip)+" "+str(port)+" "+str(playername))

master = tk.Tk()
tk.Label(master, 
         text="IP").grid(row=0)
tk.Label(master,
         text="PORT").grid(row=1)
tk.Label(master,
         text="Enter your nickname").grid(row=2)

e1 = tk.Entry(master)
e2 = tk.Entry(master)
e3 = tk.Entry(master)

e1.insert(10, '127.0.0.1')
e2.insert(10, '12345')
e3.insert(10, 'player'+str(randint(0,1000)))

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)

tk.Button(master, text='Quit', command=master.quit).grid(row=3, column=0, sticky=tk.W, pady=4)
tk.Button(master, text='Run', command=launch).grid(row=3, column=1, sticky=tk.W, pady=4)

tk.mainloop()