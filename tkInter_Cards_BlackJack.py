#For BlackJack
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk

def load_card_image(filename, width=120, height=160):
    image = Image.open(f"images/{filename}")
    image = image.resize((width, height), Image.ANTIALIAS)
    return ImageTk.PhotoImage(image)


root = tk.Tk()
root.title("Card Display")
root.configure(bg="green")  


card_width = 120
card_height = 160


clubs_img = load_card_image("images/10_of_clubs.png", card_width, card_height)
diamonds_img = load_card_image("images/10_of_diamonds.png", card_width, card_height)


main_frame = tk.Frame(root, bg="green")
main_frame.pack(fill='both', expand=True)


frame1 = tk.Frame(main_frame, padx=50, pady=30, bg="grey")
frame1.pack(pady=10, fill='both', expand=True)

frame2 = tk.Frame(main_frame, padx=50, pady=30, bg="grey")
frame2.pack(pady=10, fill='both', expand=True)


dealer_label = tk.Label(frame1, text="Dealer", font=("Arial", 16), bg="grey")
dealer_label.pack()

player_label = tk.Label(frame2, text="Player", font=("Arial", 16), bg="grey")
player_label.pack()


card1_frame = tk.Frame(frame1, width=card_width, height=card_height, bg="grey")
card1_frame.pack(pady=10)
card2_frame = tk.Frame(frame2, width=card_width, height=card_height, bg="grey")
card2_frame.pack(pady=10)


card1_label = Label(card1_frame, image=clubs_img, bg="grey")
card1_label.pack()
card2_label = Label(card2_frame, image=diamonds_img, bg="grey")
card2_label.pack()


button_frame = tk.Frame(root, bg="green")
button_frame.pack(pady=20)

hit_button = tk.Button(button_frame, text="HIT", font=("Arial", 14), bg="lightgrey")
hit_button.pack(side="left", padx=20)

stand_button = tk.Button(button_frame, text="STAND", font=("Arial", 14), bg="lightgrey")
stand_button.pack(side="left", padx=20)


root.update_idletasks()  
root.geometry(f'{root.winfo_width()}x{root.winfo_height()}')  
root.mainloop()
