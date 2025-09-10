import tkinter as tk
from tkinter import ttk

def build_gui():
    root = tk.Tk()
    root.title("SOS GUI Demo")

    # Top text label
    title = ttk.Label(root, text="SOS GUI Demo — Sprint #0", font=("Segoe UI", 14, "bold"))
    title.pack(padx=12, pady=8, anchor="w")

    # Options frame with checkbox and radio buttons
    opts = ttk.LabelFrame(root, text="Options")
    opts.pack(padx=12, pady=6, fill="x")

    autoplay_var = tk.BooleanVar(value=False)
    chk = ttk.Checkbutton(opts, text="Enable autoplay", variable=autoplay_var)
    chk.grid(row=0, column=0, padx=8, pady=6, sticky="w")

    piece_var = tk.StringVar(value="S")
    r1 = ttk.Radiobutton(opts, text="Place S", value="S", variable=piece_var)
    r2 = ttk.Radiobutton(opts, text="Place O", value="O", variable=piece_var)
    r1.grid(row=0, column=1, padx=8, pady=6)
    r2.grid(row=0, column=2, padx=8, pady=6)

    # Canvas with grid LINES
    canvas = tk.Canvas(root, width=300, height=300, bg="white")
    canvas.pack(padx=12, pady=8)
    # draw a 3x3 grid
    for i in range(1, 3):
        # vertical lines
        canvas.create_line(i * 100, 0, i * 100, 300)
        # horizontal lines
        canvas.create_line(0, i * 100, 300, i * 100)

    # Put some TEXT
    canvas.create_text(150, 150, text="S O S", font=("Segoe UI", 20))

    # Footer
    footer = ttk.Label(root, text="Include this window in your screenshot.", foreground="#555")
    footer.pack(padx=12, pady=8)

    return root

if __name__ == "__main__":
    app = build_gui()
    app.mainloop()
