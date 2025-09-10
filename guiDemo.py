import tkinter as tk

root = tk.Tk()
root.title("SOS Game")

# simple label
label = tk.Label(root, text="sos demo")
label.pack()

# checkbox
autoplay = tk.BooleanVar()
chk = tk.Checkbutton(root, text="AutoPlay", variable=autoplay)
chk.pack()

# radio buttons
piece = tk.StringVar(value="S")
r1 = tk.Radiobutton(root, text="choose S", variable=piece, value="S")
r2 = tk.Radiobutton(root, text="choose O", variable=piece, value="O")
r1.pack()
r2.pack()

# canvas with grid lines and some text
canvas = tk.Canvas(root, width=300, height=300, bg="white")
canvas.pack()
for i in range(1, 3):
    canvas.create_line(i * 100, 0, i * 100, 300)
    canvas.create_line(0, i * 100, 300, i * 100)

canvas.create_text(150, 150, text="S O S")

root.mainloop()