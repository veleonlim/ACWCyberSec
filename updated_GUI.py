# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


import os
from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
import winsound
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, filedialog, messagebox, simpledialog
from tkinter import *
from combinedENDE import decodedocx, encodedocx, insert, extract,encodeDocument,decodeDocuments,hideData, showData
from audio_encode import *
from audio_decode import *
from PIL import ImageTk,Image
import tkinter as tk
from tkVideoPlayer import TkinterVideo
from tkinter import ttk
import tkinterDnD 



# Replace `Canvas(root, ...)` with `Canvas(root, dnd_enabled=True, ...)`


input_file = ''
payload_file = ''
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/Users/veleonlim/Downloads/build/assets/frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def upload_file():
   
    file_path = filedialog.askopenfilename()
    print('path is this '+file_path)
    if file_path:
        file_extension = Path(file_path).suffix.lower()
        print("File extension:", file_extension)

        if file_extension == ".mp4":
            play_button.place_forget()
            stop_button.place_forget()

            videoplayer.load(file_path)
            videoplayer.play()
            videoplayer_frame.place(x=39, y=118, width=160, height=160)
        elif file_extension == ".png" or file_extension == ".tiff":
            videoplayer.stop()
            videoplayer_frame.place_forget()

            play_button.place_forget()
            stop_button.place_forget()
            
            image = Image.open(file_path)
            image.thumbnail((160, 160))
            photo = ImageTk.PhotoImage(image)

            label = tk.Label(canvas, image=photo)
            label.image = photo
            label.place(x=39, y=118)
        elif file_extension == ".txt" or file_extension == ".docx":
            videoplayer.stop()
            videoplayer_frame.place_forget()

            play_button.place_forget()
            stop_button.place_forget()
            
            filename = os.path.basename(file_path)
            label = tk.Label(canvas, text=filename, wraplength=160)
            label.place(x=38, y=118, width=160, height=160)
        elif file_extension == ".wav":
            videoplayer.stop()
            videoplayer_frame.place_forget()
            
            filename = os.path.basename(file_path)
            label = tk.Label(canvas, text=filename, wraplength=160)
            label.place(x=38, y=118, width=160, height=160)

            play_button.place(x=39, y=360, width=80, height=35)
            stop_button.place(x=120, y=360, width=80, height=35)
        else:
            print("Unsupported file format")

    global input_file
    # file_path = filedialog.askopenfilename()
    input_file = str(file_path)
    print(input_file)

# -- plays audio file --
def play():
    winsound.PlaySound(input_file,winsound.SND_ASYNC+winsound.SND_LOOP)

def output_play():
    winsound.PlaySound(input_file,winsound.SND_ASYNC+winsound.SND_LOOP)

def stop_play():
    winsound.PlaySound(None,0)

# --        END        --

def dragupload_file(path):
    file_path = path.strip("{}")
    
    if file_path:
        file_extension = Path(file_path).suffix.lower()
        print("File extension:", file_extension)

        if file_extension == ".mp4":
            play_button.place_forget()
            stop_button.place_forget()
            
            videoplayer.load(file_path)
            videoplayer.play()
            videoplayer_frame.place(x=39, y=118, width=160, height=160)
          
        elif file_extension == ".png" or file_extension == ".tiff":
            videoplayer.stop()
            videoplayer_frame.place_forget()

            play_button.place_forget()
            stop_button.place_forget()

            image = Image.open(file_path)
            image.thumbnail((160, 160))
            photo = ImageTk.PhotoImage(image)

            label = tk.Label(canvas, image=photo)
            label.image = photo
            label.place(x=39, y=118)
        elif file_extension == ".txt" or file_extension == ".docx":
            videoplayer.stop()
            videoplayer_frame.place_forget()

            play_button.place_forget()
            stop_button.place_forget()
            
            filename = os.path.basename(file_path)
            label = tk.Label(canvas, text=filename, wraplength=160)
            label.place(x=38, y=118, width=160, height=160)
        elif file_extension == ".wav":
            videoplayer.stop()
            videoplayer_frame.place_forget()
            
            filename = os.path.basename(file_path)
            label = tk.Label(canvas, text=filename, wraplength=160)
            label.place(x=38, y=118, width=160, height=160)

            play_button.place(x=39, y=360, width=80, height=35)
            stop_button.place(x=120, y=360, width=80, height=35)
        else:
            print("Unsupported file format")

    global input_file
    # file_path = filedialog.askopenfilename()
    input_file = str(file_path)
    print(input_file)


def payload_file_find():
    global payload_file
    file_path = filedialog.askopenfilename()
    payload_file = str(file_path)
    print(payload_file)

    if file_path:
        file_extension = Path(file_path).suffix.lower()
        print("File extension:", file_extension)

        if file_extension == ".txt" or file_extension == ".docx":
        

            label = tk.Label(canvas, text=os.path.basename(file_path), wraplength=160)
            label.place(x=242, y=119, width=170, height=160)
        else:
            print("Unsupported file format")

def dragpayload_file(path):
    global payload_file
    file_path = path.strip("{}")
    payload_file = str(file_path)
    print(payload_file)

    if file_path:
        file_extension = Path(file_path).suffix.lower()
        print("File extension:", file_extension)

        if file_extension == ".txt" or file_extension == ".docx":
            videoplayer.stop()
            videoplayer_frame.place_forget()

            label = tk.Label(canvas, text=os.path.basename(file_path), wraplength=160)
            label.place(x=242, y=119, width=170, height=160)
        else:
            print("Unsupported file format")

def run_extraction(path,bits):
    print("file:", path)
    extract_path = path
    msg = extract(extract_path,bits)
    # Do something with the extracted message (e.g., display it in the GUI)
    print("???", msg)  # Example: printing the extracted message
    canvas.itemconfigure(text_item, text=msg)  # Update the text item in the canvas

window = tkinterDnD.Tk(className=" Steganography Program")

stringvar = tk.StringVar()
stringvar.set('Drop here or drag from here!')
stringvar2 = tk.StringVar()
stringvar2.set('Drop here or drag from here!')
window.geometry("1000x1000")
window.configure(bg="#E6F2FF")


def drop(event):
    # This function is called, when stuff is dropped into a widget
    dragupload_file(event.data)
    stringvar.set(event.data)

def drag_command(event):
    # This function is called at the start of the drag,
    # it returns the drag type, the content type, and the actual content
    return (tkinterDnD.COPY, "DND_Text", "Some nice dropped text!")
def droppayload(event):
    # This function is called, when stuff is dropped into a widget
    dragpayload_file(event.data)
    stringvar2.set(event.data)

canvas = Canvas(
    window,
    bg="#E6F2FF",
    height=1000,
    width=1000,
    bd=0,
    highlightthickness=0,
    relief="ridge",
   
)

canvas.place(x=0, y=0)

# Video
videoplayer_frame = tk.Frame(canvas, bg="#D9D9D9")
videoplayer_frame.place(x=39, y=118, width=160, height=160)

videoplayer = TkinterVideo(master=videoplayer_frame, scaled=True)

videoplayer.pack(expand=True, fill="both")

# Audio
play_button = Button(canvas, text="Play Sound", font=("Helvetica", 10),
                     relief=GROOVE, command=play)

stop_button = Button(canvas, text="Stop Sound", font=("Helvetica", 10),
                     relief=GROOVE, command=stop_play)

# Drag and Drops
label_1 = tk.Label(window, textvar=stringvar, relief='solid', borderwidth=1)

label_1.place(x= 39, y=325, width=160, height=35)

label_1.register_drop_target("*")
label_1.bind("<<Drop>>", drop)

label_1.register_drag_source("*")
label_1.bind("<<DragInitCmd>>", drag_command)


# With DnD hook you just pass the command to the proper argument,
# and tkinterDnD will take care of the rest
# NOTE: You need a ttk widget to use these arguments
label_2 = ttk.Label(window,textvar=stringvar2, relief="solid", borderwidth=1)
label_2.place(x=242, y=325, width=160, height=35)

label_2.register_drop_target("*")
label_2.bind("<<Drop>>", droppayload)
label_2.register_drag_source("*")
label_2.bind("<<DragInitCmd>>", drag_command)

canvas.create_rectangle(
    39.0,
    118.0,
    199.0,
    278.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    242.0,
    119.0,
    402.0,
    279.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    131.0,
    410.0,
    672.0,
    816.0,
    fill="#D9D9D9",
    outline="")


text_item = canvas.create_text(
    131.0,
    410.0,
    width=500, # Wrap Text
    anchor="nw",
    text="",
    fill="#000000",
         font=("Inter 12"),
    )

canvas.create_text(
    39.0,
    92.0,
    anchor="nw",
    text="Cover Object / Stego",
fill="#000000",
           font=("Inter 14 bold")
)

canvas.create_text(
    39.0,
    36.0,
    anchor="nw",
    text="Step 1: Upload File",
    fill="#055DEC",
    font=("Helvetica 16 bold")
)

canvas.create_text(
    242.0,
    35.0,
    anchor="nw",
    text="Step 2: Upload Payload",
    fill="#055DEC",
    font=("Helvetica 16 bold")
)

canvas.create_text(
    490.0,
    34.0,
    anchor="nw",
    text="Step 3: Select Number of LSB",
    fill="#055DEC",
    font=("Helvetica 16 bold")
)

canvas.create_text(
    470.0,
    170.0,
    anchor="nw",
    text="Step 4: Encode or Decode",
   fill="#055DEC",
    font=("Helvetica 16 bold")
)

canvas.create_text(
    242.0,
    92.0,
    anchor="nw",
    text="Payload",
    fill="#000000",
    font=("Inter 14 bold")
)

canvas.create_text(
    319.0,
    374.0,
    anchor="nw",
    text="Output",
    fill="#000000",
      font=("Inter 14 bold")
)

canvas.create_text(
    474.0,
    92.0,
    anchor="nw",
    text="Number of LSB (0-5)",
    fill="#000000",
      font=("Inter 14 bold")
)

# Define a global variable to store the selected number of LSB
selected_lsb = StringVar()
selected_lsb.set("0")  # Default value

# Create the OptionMenu widget
lsb_option_menu = OptionMenu(canvas, selected_lsb, "0", "1", "2", "3", "4", "5")
lsb_option_menu.configure(width=10)
lsb_option_menu.place(x=472.0, y=115.0, width=152.0, height=26.0)

# button_image_1 = PhotoImage(
#     file=relative_to_assets("button_1.png"))
button_1 = Button(
    # image=button_image_1,
    text="Upload",
    borderwidth=0,
    highlightthickness=0,
    command=lambda: (upload_file(), print("button_1 clicked" )),
    relief="flat"
)

button_1.place(
    x=39.0,
    y=285.0,
    width=160,
    height=35.0
)

# button_image_2 = PhotoImage(
#     file=relative_to_assets("button_2.png"))
button_2 = Button(
    # image=button_image_2,
    text="Upload",
    borderwidth=0,
    highlightthickness=0,
    command=lambda: (payload_file_find(), print("button_2 clicked" )),
    relief="flat"
)
button_2.place(
    x=242.0,
    y=285.0,
    width=160.0,
    height=35.0
)

# button_image_3 = PhotoImage(
#     file=relative_to_assets("button_3.png"))
button_3 = Button(
    text="Encode",
    borderwidth=0,
    highlightthickness=0,
    relief="flat"
)

def encode_button_click():
    print("file extension is this " +input_file)
    file_extension = Path(input_file).suffix.lower()
    print("file extension is this " +file_extension)
    try:
        if file_extension == ".txt" :
            # Call your encodedocument function here
            encodeDocument(input_file, payload_file,int(selected_lsb.get()))
        elif  file_extension == ".docx":
            encodedocx(input_file, payload_file,int(selected_lsb.get()))
        elif file_extension == ".png" or file_extension == ".tiff":
            # Call the insert function here
            insert(input_file, payload_file,int(selected_lsb.get()))
        elif file_extension == ".mp4" or file_extension == ".mp3":
            coverfile = os.path.join(os.getcwd(), input_file)
            encodedvid = hideData(coverfile, payload_file, int(selected_lsb.get()), True)
            print(encodedvid)
            videoplayer.load(encodedvid)
            videoplayer.play()
            videoplayer_frame.place(x=131, y=410, width=472, height=416)
        elif file_extension==".wav":
            if(int(selected_lsb.get()) in [3,4,5]):
                messagebox.showinfo("Error","Only LSB 0, 1 and 2 is supported!")
            else:
                #coverfile = os.path.join(os.getcwd(), input_file)
                cover = wave.open(input_file, "r")
                with open(payload_file,'r') as file:
                    secret = file.read()
                messagebox.showinfo("Info","Length of message in bits: " + str(len(secret)))

                msg = convertMsgToBin(secret)

                nlsb = int(selected_lsb.get())
                if nlsb==0:
                    nlsb=1
                if nlsb==1:
                    nlsb=2
                if nlsb==2:
                    nlsb=3
                audio_stego(cover, msg, nlsb)
                cover.close()
        else:
            print("Unsupported file format")
    except:
        messagebox.showinfo("Error","No Payload Uploaded!")


button_3.configure(command=encode_button_click)


button_3.place(
    x=472.0,
    y=206.0,
    width=152.0,
    height=35.0
)

# button_image_4 = PhotoImage(
#     file=relative_to_assets("button_4.png"))
def Decode_button_click():
    file_extension = Path(input_file).suffix.lower()
    if file_extension == ".txt":
        # Call your encodedocument function here
        msg = decodeDocuments(input_file,int(selected_lsb.get()))
        canvas.itemconfigure(text_item, text=msg)  # Update the text item in the canvas
    elif file_extension == ".docx":
        msg = decodedocx(input_file,int(selected_lsb.get()))
        canvas.itemconfigure(text_item, text=msg)  # Update the text item in the canvas
    elif file_extension == ".png" or file_extension == ".tiff":
        # Call the insert function here
        run_extraction(input_file,int(selected_lsb.get()))
    elif file_extension == ".mp4" or file_extension == ".mp3":
        msg = showData(input_file,int(selected_lsb.get()))
        print("???", msg)  # Example: printing the extracted message
        canvas.itemconfigure(text_item, text=msg)  # Update the text item in the canvas
    elif file_extension == ".wav":
        if(int(selected_lsb.get()) in [3,4,5]):
            messagebox.showinfo("Error","Only LSB 0, 1 and 2 is supported!")
        else:
            stego = wave.open(input_file, "r")
            nlsb = int(selected_lsb.get())
            if nlsb==0:
                nlsb=1
            if nlsb==1:
                nlsb=2
            if nlsb==2:
                nlsb=3
            size = simpledialog.askstring(title="Audio Stego",
                                    prompt="Enter Secret Message Size")
            msg = audio_extract(stego, nlsb, int(size))
            canvas.itemconfigure(text_item, text=msg)  # Update the text item in the canvas
    else:
        print("Unsupported file format")


# Create the decode button
button_4 = Button(
    text="Decode",
    borderwidth=0,
    highlightthickness=0,
    command=Decode_button_click,
    relief="flat"
)
button_4.place(
    x=472.0,
    y=258.0,
    width=152.0,
    height=34.0
)

canvas.create_rectangle(
    472.0,
    115.0,
    624.0,
    141.0,
    fill="#D9D9D9",
    outline="")

window.resizable(False, False)
window.mainloop()
