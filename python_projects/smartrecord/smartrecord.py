from tkinter import *
from PIL import Image, ImageTk
import time, sys, threading

screen = Tk()
screen.iconbitmap("stopwatch.ico")
screen.geometry("700x400")
screen.attributes("-fullscreen", True)

screen.bind("<Escape>", lambda event: screen.attributes("-fullscreen", False))
screen.bind("<space>", lambda event: keypressed())
screen.bind("<Control-r>", lambda event: reset_timer())

background = Image.open("backgroundtime.jpg")
background = background.resize((screen.winfo_screenwidth(), screen.winfo_screenheight()), Image.LANCZOS)
backgroundphoto = ImageTk.PhotoImage(background)

canvas = Canvas(screen, width=screen.winfo_screenwidth(), height=screen.winfo_screenheight())
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=backgroundphoto, anchor="nw")
canvas.backgroundphoto = backgroundphoto

second = minute = milli_second = hour = 0
start_time = elapsed_time = 0
play = False

def reset_timer():
    global second, minute, milli_second, start_time, elapsed_time, play, hour
    second = minute = milli_second = hour = 0
    start_time = elapsed_time = 0
    lsecond.config(text=f"{hour:02d}:{minute:02d}:{second:02d}:{milli_second:03d}")
    stop_button.config(image=icons["play"])
    play = False

def keypressed():
    global play, start_time, elapsed_time
    if play:
        play = False
        elapsed_time += time.time() - start_time
        stop_button.config(image=icons["play"])
    else:
        play = True
        start_time = time.time()
        stop_button.config(image=icons["pause"])
        update_second()

def update_second():
    global start_time, elapsed_time
    if play:
        current_time = time.time()
        elapsed = current_time - start_time + elapsed_time
        hour = int(elapsed // 3600)
        minute = int((elapsed % 3600) // 60)
        second = int(elapsed % 60)
        milli_second = int((elapsed * 1000) % 1000)
        lsecond.config(text=f"{hour:02d}:{minute:02d}:{second:02d}:{milli_second:03d}")
        screen.after(1, update_second)

lsecond = Label(screen, text=f"{hour:02d}:{minute:02d}:{second:02d}:{milli_second:03d}", bg="black", fg="white", font=("Arial", '80'))
lsecond.place(relx=0.5, rely=0.3, anchor='center')

def endcon():
    confirm.destroy()
    screen.destroy()

def end():
    global confirm
    confirm = Toplevel(screen)
    confirm.geometry("450x150")
    confirm.title("Exit")
    Label(confirm, text="Do you want to close it?", font=("Arial", "20")).pack(pady=10)
    Button(confirm, text="OK", command=endcon, bg="red", fg="white").pack(pady=10)

endbutton = Button(text="X", bg='red', fg='white', command=end)
endbutton.place(x=screen.winfo_screenwidth() - 40, y=0)

def load_icon(icon_name, size=(50, 50)):
    img = Image.open(icon_name)
    img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

icons = {
    "play": load_icon("play.png"),
    "pause": load_icon("pause.png"),
    "restart": load_icon("restart.png")
}

stop_button = Button(screen, image=icons["play"], command=keypressed)
stop_button.place(relx=0.4, rely=0.6, anchor='center')

reset_btn = Button(screen, image=icons["restart"], command=reset_timer)
reset_btn.place(relx=0.6, rely=0.6, anchor='center')

screen.after(100, update_second)
screen.mainloop()
