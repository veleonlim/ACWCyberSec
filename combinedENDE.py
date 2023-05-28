import math
from os import path
import base64
import os
import cv2
import numpy as np

# Embed secret in the n least significant bit.
# Lower n make picture less loss but lesser storage capacity.
BITS = 20

HIGH_BITS = 256 - (1 << BITS)
LOW_BITS = (1 << BITS) - 1
BYTES_PER_BYTE = math.ceil(8 / BITS)
FLAG = '%'


def insert(img_path, msg):
    # Reading the image
    img = cv2.imread(img_path, cv2.IMREAD_ANYCOLOR)
    # Save origin shape to restore image
    ori_shape = img.shape
    print(ori_shape)
    # Finding out how many bytes the image is by multiplying the height and width
    max_bytes = ori_shape[0] * ori_shape[1] // BYTES_PER_BYTE
    # Encode message with length
    with open(msg, 'r') as file:
        msg = file.read()
    msg = '{}{}{}'.format(len(msg), FLAG, msg)
    assert max_bytes >= len(
        msg), "Message greater than capacity:{}".format(max_bytes)
    data = np.reshape(img, -1)
    for (idx, val) in enumerate(msg):
        encode(data[idx * BYTES_PER_BYTE: (idx + 1) * BYTES_PER_BYTE], val)

    img = np.reshape(data, ori_shape)
    filename, _ = path.splitext(img_path)
    filename += '_lsb_embeded' + ".png"
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
        # print(secret)
    return secret


def decode(block):
    val = 0
    for idx in range(len(block)):
        val |= (block[idx] & LOW_BITS) << (idx * BITS)
    return chr(val)


if __name__ == '__main__':

    ch = int(input('What do you want to do?\n\n1.Encrypt\n2.Decrypt\n\nInput(1/2): '))
    if ch == 1:
        img_path = input('\nEnter cover image name(path)(with extension): ')
        msg = input('Enter secret data: ')
        res_path = insert(img_path, msg)
        print("success")
    elif ch == 2:
        img_path = input('\nEnter cover image name(path)(with extension): ')
        msg = extract(img_path)
        print(msg)


#Encoding Documents

def convertBYTES(file_path):
    with open(file_path,'rb') as file:
        file_bytes = file.read()
    return file_bytes

def encodeBASE64(file_path):
    with open(file_path, "rb") as file:
        file_64 = base64.b64encode(file.read())
    return file_64

def convertBITS(data):
    if type(data) == str:
        return ''.join([format(ord(i), "08b") for i in data])
    elif type(data) == bytes or type(data) == np.ndarray:
        return [format(i, "08b") for i in data]
    elif type(data) == int or type(data) == np.uint8:
        return format(data, "08b")
    else:
        # Input type not able to be changed to binary
        raise TypeError("Input type not supported")

def convertCHAR(data):
    encodedText = ""
    for byte_in_BITS in data:
        encodedText += chr(int(byte_in_BITS, 2))
    return encodedText

import os

def encodeDocument(cover_source, payload_source, BITS):
    # Using os.path to retrieve file path & file extensions 
    cover_path = os.path.join(os.getcwd(), cover_source)
    payload_path = os.path.join(os.getcwd(), payload_source)
    cover_ext = os.path.splitext(cover_path)[1]
    payload_ext = os.path.splitext(payload_path)[1]

    # Converting cover file into BYTES (Readable texts)
    cover_BYTES = convertBYTES(cover_path)
    #payload_BYTES = convertBYTES(payload_path)

    # Encoding Payload Bytes into Base64
    payload_64 = encodeBASE64(payload_path)

    # Adding Paddings into extension
    while len(payload_ext) < 10:
        payload_ext += '@'

    # Converts encoded payload into a string, include Payload's extension and adds delimiter 
    # Delimiter is for decoder to identify the end of payload (Stop steganography decoding)
    payloadEncode = str(payload_64) + payload_ext + "%$&@"

    # Converting BYTES into BITS
    #cover_BITS = convertBITS(cover_BYTES)
    payload_BITS = convertBITS(payloadEncode)
    
    # Outputs information of Cover Byte length and binary/bits length of payload
    print("Byte Length (Cover):", len(cover_BYTES))
    print("Binary Length (Payload)", len(payload_BITS))

    # Throws an error if the payload length is lesser than the cover length 
    # (Insufficient bytes to steganograph the payload into the cover)
    if len(payload_BITS) / BITS > len(cover_BYTES):
        raise ValueError("[!] Insufficient bytes, need bigger cover document")
    
    # CoverBytesList stores a series of bits (8 bits) at each index e.g. [10101010, 00001111, 11110101]
    coverByteList = []
    for i in range(0, len(cover_BYTES)):
        coverByteList.append(convertBITS(cover_BYTES[i]))
    
    payloadBITS_len = len(payload_BITS)

    # "Pointer" to keep track of which bits of payload have already been completed.
    dataIndex = 0

    for i, byte_in_BITS in enumerate(coverByteList):
        # If there is still more data to store
        if dataIndex < payloadBITS_len:
            tempBin = ''
            # Remove the last few digits of the byte based on the number of LSB used
            byte_in_BITS = byte_in_BITS[:-BITS]
            # Loop and store the data to hide into a temp variable
            for x in range(BITS):
                tempBin += payload_BITS[dataIndex]
                dataIndex += 1
                # Break the loop if all the data have been hidden
                if dataIndex == payloadBITS_len:
                    break
            # Pad 0 to the front of the temp binary if the length of the temp binary is less than the number of LSB used
            if len(tempBin) < BITS:
                tempBin = tempBin.ljust(BITS, '0')
            # Adds the temp binary to the byte and change it into an integer and assign it to the back to the array of bytes
            coverByteList[i] = byte_in_BITS + tempBin

    # Converting the encoded Text from BITS into human-readable CHAR
    encodedText = convertCHAR(coverByteList)

    print("\nEncoded Text(Stego):", encodedText)
    print("Encoded Text Length:", len(encodedText), "\n")
    print("########### Encoding Successful ###########\n")

    stegoObjName = os.path.splitext(cover_source)[0] + "_embedded"
    output_file_name = stegoObjName + cover_ext

    with open(output_file_name, "wb") as outFile:
        outFile.write(encodedText.encode('utf-8'))








#Decoding Documents
encodedStegoFile = "test123.docx" #Change to user Input

def convertBYTES(file_path):
    with open(file_path,'rb') as file:
        file_bytes = file.read()
    return file_bytes

def convertBITS(data):
    if type(data) == str:
        return ''.join([format(ord(i), "08b") for i in data])
    elif type(data) == bytes or type(data) == np.ndarray:
        return [format(i, "08b") for i in data]
    elif type(data) == int or type(data) == np.uint8:
        return format(data, "08b")
    else:
        # Input type not able to be changed to binary
        raise TypeError("Input type not supported")

def convertCHAR(payload_BYTES):        
    decoded_data = ""
    for bytes in payload_BYTES:
        decoded_data += chr(int(bytes, 2))

        # Identify End of Payload when hit Preset Delimeter
        if decoded_data[-4:] == "%$&@":
            break
    return decoded_data

def decodeDocuments(encodedStegoFile, BITS):

    # Using os.path to retrieve path of encoded file 
    encodedStego_path = os.path.join(os.getcwd(), encodedStegoFile)
    stego_BYTES = convertBYTES(encodedStego_path).decode('utf-8')
    
    # Creates an array (stegoByteList) to store BITS in "byte" structure
    # Similar to encode [11110000, 00011000, 00111100]
    stegoByteList = []
    for i in range(0, len(stego_BYTES)):
        stegoByteList.append(convertBITS(stego_BYTES[i]))

    # Extract the LSB(Contains Payload) based on numOfBits & store into payload_BIN Array
    payload_BIN = ''
    for i, byte in enumerate(stegoByteList):
        payload_BIN += byte[-BITS:]

    # Converge 8 payload bits into 1 byte [xxxxxxxx,xxxxxxxx,xxxxxxxx]
    payload_BYTES = [payload_BIN[i: i + 8] for i in range(0, len(payload_BIN), 8)]

    # decoded_data contains payload in CHAR
    decoded_data = convertCHAR(payload_BYTES)

    # Removing the Preset Delimeter ("%$&@") Found at last 4 index.
    decoded_data = decoded_data[:-4]

    # Retrieves Padded File Extension(E.g. .txt@@@@@@)
    file_ext = decoded_data[-10:]
    decoded_data = decoded_data[:-10]

    # Removal of Paddings to idenfity file extension (Can reuse for image code to allow generate new img etc)
    file_ext = file_ext.replace("@", "")

     # Converting Base64 Payload Text back into a STRING
    decoded_data_STR = base64.b64decode(eval(decoded_data)).decode("utf-8")
    print("Decoded Text: ", decoded_data_STR)
    return decoded_data_STR

