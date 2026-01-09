from datetime import datetime
from tkinter import Tk, ttk, filedialog

from PIL import ImageTk, Image


def open_image():
    global image
    global image_file

    filename = choose_file()
    if filename:
        clear_frame()

        image_file = Image.open(filename).resize((960, 480))

        image = ImageTk.PhotoImage(image_file)

        image_label = ttk.Label(frame, image=image)
        image_label.pack()


def reset_frame():
    global image_file
    global image
    global watermarked_image_file

    clear_frame()

    image_file = Image.open("img/image.png").resize((960, 480))
    image = ImageTk.PhotoImage(image_file)
    watermarked_image_file = image_file.copy()


def clear_frame():
    for widget in frame.winfo_children():
        widget.destroy()


def display_image():
    image_label = ttk.Label(frame, image=image)
    image_label.pack()


def choose_file():
    filetypes = [("Image Files", ["*.jpg", "*.png"]), ("All Files", "*.*")]
    filename = filedialog.askopenfilename(initialdir="/", title="Select Image",
                                          filetypes=filetypes)

    return filename


def add_watermark():
    global image
    global image_file
    global watermarked_image_file

    watermarked_image_file = image_file.copy()

    watermark_image = Image.open("watermark/image.png").resize((960, 480))

    watermarked_image_file = Image.blend(watermarked_image_file, watermark_image, 0.2)

    image = ImageTk.PhotoImage(watermarked_image_file)

    clear_frame()
    image_label = ttk.Label(frame, image=image)
    image_label.pack()


def save_image():
    global watermarked_image_file

    watermarked_image_file.save(f"image - {int(datetime.now().strftime('%Y%m%d%H%M%S%f'))}.png")

    clear_frame()
    reset_frame()
    display_image()


root = Tk()
root.title("Image Watermarking")
root.geometry("1024x720")

frame = ttk.Frame(root, style="new.TFrame")
frame.config(width=960, height=480)
frame.place(x=32, y=16)

image_file = None
image = None
watermarked_image_file = None

reset_frame()
display_image()

style = ttk.Style()
style.configure("new.TFrame", background="white")
style.configure("new.TButton", font=('Arial', 10), background="white", foreground="black", width=14, borderwidth=1,
                focusthickness=5, focuscolor='blue')
style.configure("new.TEntry", font=('Arial', 8), background="white", foreground="black", width=14, borderwidth=1,
                focusthickness=5, focuscolor='blue')
style.configure("new.TLabel", font=('Arial', 11), foreground="black", borderwidth=10)

button_choose = ttk.Button(root, text="Open File", command=open_image, style="new.TButton")
button_choose.place(x=780, y=550)

button_add_watermark = ttk.Button(root, text="Add Watermark", command=add_watermark, style="new.TButton")
button_add_watermark.place(x=530, y=640)

button_save_image = ttk.Button(root, text="Save Image", command=save_image, style="new.TButton")
button_save_image.place(x=780, y=640)

root.mainloop()
