import tkinter as tk
from tkinter import font
def center_window(window, width = 600, height = 600): 
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

w = tk.Tk()
window_width = 800
window_height = 600
w.geometry(f"{window_width}x{window_height}")
w.configure(bg='green')
fontStyle = font.Font(family="Arial", size=60)
name = tk.Label(
    w,
    text='Casino Royale',
    foreground = 'yellow',
    background= 'green',  
    font = fontStyle
)
name.pack(pady=50)
settingsbutton = tk.Button(
    w,
    text='Baccarat',
    width=15 ,
    height=3,
    bg='red',
    fg='black',
    relief='flat',
    highlightbackground='red' 
)
playbutton = tk.Button(
    w,
    text='BlackJack',
    width=15,
    height=3,
    bg='red',
    fg='black',
    relief='flat',
    highlightbackground='red'
)
Exitbutton = tk.Button(
    w,
    text='Exit',
    width=15,
    height=3,
    bg='red',
    fg='black',
    relief='flat',
    highlightbackground='red'
)
playbutton.place(relx=0.5, rely = 0.4, anchor="center")
settingsbutton.place(relx=0.5, rely=0.55, anchor="center")
Exitbutton.place(relx=0.5, rely=0.7, anchor='center')
center_window(w, window_width, window_height)
w.mainloop()
