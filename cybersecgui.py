# Import Module
from tkinter import *
from tkinter import ttk,messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk
import sys
import math
from os import path
import cv2
import numpy as np

##
# image cannot manipulate bits hmm
# Ui almost done left logic

# functions for drag and drop
def drop_inside_list_box1(event):
    listb_1.delete(0,END)
    #listb_1.insert("end",event.data)
    event.data=event.data.replace("{","")
    event.data=event.data.replace("}","")

    if(event.data.endswith(".png")):
        global cover_path
        cover_path=event.data
        listb_1.place_forget()
        image = Image.open(event.data)
        image_new= image.resize(size=(150,130))
        test = ImageTk.PhotoImage(image_new)
        label_for_cover_object.configure(image=test)
        label_for_cover_object.image = test  # Store a reference to avoid garbage collection
        label_for_cover_object.place(x=39, y=118)
    elif(event.data.endswith(".txt")):
        pass
    elif(event.data.endswith(".mp4")):
        pass
    else:
        messagebox.showinfo("Error","File Type not supported only .txt!")
    
def clear_all():
    label_for_cover_object.configure(image=None)
    label_for_cover_object.image = None
    label_for_cover_object.place_forget()
    listb_1.delete(0,END)
    listb_1.place(x = 39,y = 120)

    label_for_payload.configure(image=None)
    label_for_payload.image = None
    label_for_payload.place_forget()
    listb_2.delete(0,END)
    listb_2.place(x = 242,y = 118)
    
def drop_inside_list_box2(event):
    listb_2.delete(0,END)
    #listb_2.insert("end",event.data)
    event.data=event.data.replace("{","")
    event.data=event.data.replace("}","")

    if(event.data.endswith(".txt")):
        global payload_path
        payload_path=event.data
        listb_2.place_forget()
        # image = Image.open(event.data)
        # image_new= image.resize(size=(100,100))
        # test = ImageTk.PhotoImage(image_new)
        # label_for_payload.configure(image=test)
        # label_for_payload.image = test
        with open(event.data,'r') as f:
            lines = f.readlines()
        secret_msg = lines[0]
        label_for_payload.configure(width=20,height=11,text=secret_msg,background="#FFFFFF",wraplength=100)
        label_for_payload.place(x=242,y=120)
    else:
        messagebox.showinfo("Error","File Type not supported only .txt!")

#------------------ START Encoding/Decoding for Image ------------------#

# Embed secret in the n least significant bit.
# Lower n make picture less loss but lesser storage capacity.
BITS = 256

HIGH_BITS = 256 - (0 << BITS)
LOW_BITS = (0 << BITS) - 1
BYTES_PER_BYTE = math.ceil(8 / BITS)
FLAG = '%'

def insert_image(img_path, msg):
    # Reading the image
    img = cv2.imread(img_path, cv2.IMREAD_ANYCOLOR)
    # Save origin shape to restore image
    ori_shape = img.shape
    # print(ori_shape)
    # Finding out how many bytes the image is by multiplying the height and width
    max_bytes = ori_shape[0] * ori_shape[1] // BYTES_PER_BYTE
    
    # Reads File Text
    with open(msg,'r') as f:
        lines = f.readlines()
    secret_msg = lines[0]

    # Encode message with length
    secret_msg = '{}{}{}'.format(len(secret_msg), FLAG, secret_msg)
    assert max_bytes >= len(
        secret_msg), "Message greater than capacity:{}".format(max_bytes)
    data = np.reshape(img, -1)
    for (idx, val) in enumerate(secret_msg):
        encode(data[idx * BYTES_PER_BYTE: (idx + 1) * BYTES_PER_BYTE], val)

    img = np.reshape(data, ori_shape)
    filename, _ = path.splitext(img_path)
    filename += 'encoded_img' + ".png"
    cv2.imwrite(filename, img)
    return filename

def encode(block, data):
    # returns the Unicode code from a given character
    data = ord(data)
    for idx in range(len(block)):
        block[idx] &= HIGH_BITS
        block[idx] |= (data >> (BITS * idx)) & LOW_BITS

def extract(path):
    img = cv2.imread(path, cv2.IMREAD_ANYCOLOR)
    data = np.reshape(img, -1)
    total = data.shape[0]
    res = ''
    idx = 0
    # Decode message length
    while idx < total // BYTES_PER_BYTE:
        ch = decode(data[idx * BYTES_PER_BYTE: (idx + 1) * BYTES_PER_BYTE])
        idx += 1
        if ch == FLAG:
            break
        res += ch
    end = int(res) + idx
    assert end <= total // BYTES_PER_BYTE, "Input image isn't correct."

    secret = ''
    while idx < end:
        secret += decode(data[idx * BYTES_PER_BYTE: (idx + 1) * BYTES_PER_BYTE])
        idx += 1
    print(secret)
    # return secret


def decode(block):
    val = 0
    for idx in range(len(block)):
        val |= (block[idx] & LOW_BITS) << (idx * BITS)
    return chr(val)

#------------------ END Encoding/Decoding for Image ------------------#

def checkcmbo():

    if bitschosen.get() == "Bit 1":
        messagebox.showinfo("What user choose", "you choose prova")

    # if user select prova show this message 
    elif bitschosen.get() == "Bit 2":
        messagebox.showinfo("What user choose", "you choose ciao")

# create root window
root = TkinterDnD.Tk()

# root window title and dimension
root.title("Cyber Security Project")
# Set geometry(widthxheight)
root.geometry('666x829')

lbl=Label(root,text='Step 1: Upload File').place(x = 39,y = 36)
lbl1=Label(root,text='Step 2: Upload Payload').place(x = 242.0,y = 35) 
lbl2=Label(root,text='Step 3: Select Number of LSB').place(x = 471,y = 34)
lbl3=Label(root,text='Step 4: Encode or Decode').place(x = 470,y = 170)

lbl4=Label(root,text='Payload').place(x = 242,y = 92)
lbl5=Label(root,text='Cover Object / Stego').place(x = 39,y = 92)
lbl6=Label(root,text='Number of LSB (0-5)').place(x = 471,y = 92)
lbl7=Label(root,text='Output').place(x = 319,y = 374)

# Combobox creation
n = StringVar()
bitschosen = ttk.Combobox(root, width = 27, textvariable = n)
bitschosen.place(x=472.0,y=115.0)
  
# Adding combobox drop down list
bitschosen['values'] = ('Bit 1', 'Bit 2', 'Bit 3', 'Bit 4', 'Bit 5')
bitschosen.current(0)

encode_button = Button(root,
                       text = "Encode",command = lambda:(insert_image(cover_path,payload_path))).place( 
                           x=472.0,y=206.0,width=152.0,height=35.0)
decode_button = Button(root,
                       text = "Decode",command = lambda:(extract(cover_path))).place( 
                           x=472.0,y=256.0,width=152.0,height=35.0)
upload_cover_object = Button(root,
                       text = "Upload Cover/Stego",command = checkcmbo).place( 
                           x=39.0,y=305.0,width=152.0,height=35.0)
upload_payload = Button(root,
                       text = "Upload Payload",command = lambda:(print("Upload Payload"))).place( 
                           x=240.0,y=305.0,width=140.0,height=35.0)
clear_objects = Button(root,
                       text = "Clear",command = clear_all).place( 
                           x=472.0,y=306.0,width=152.0,height=35.0)


listb_1 = Listbox(root,selectmode=SINGLE, background="#ffe0d6",font=('TkMenuFont, 10'))
listb_1.place(x = 39,y = 120)
listb_1.drop_target_register(DND_FILES)
listb_1.dnd_bind("<<Drop>>",drop_inside_list_box1)

label_for_cover_object = Label(width=150,height=130)

listb_2 =Listbox(root,selectmode=SINGLE, background="#ffe0d6",font=('TkMenuFont, 10'))
listb_2.place(x = 242,y = 119)
listb_2.drop_target_register(DND_FILES)
listb_2.dnd_bind("<<Drop>>",drop_inside_list_box2)

label_for_payload = Label(width=100,height=100)

label_for_output = Label(width=84,height=23,background="#D9D9D9")
label_for_output.place(x = 40, y= 400)


root.mainloop()