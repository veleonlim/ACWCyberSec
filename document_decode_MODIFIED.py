import numpy as np
import base64
import os.path

encodedStegoFile = "test123.docx" #Change to user Input
numOfBits = 1 #Change to user Input

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

def decode(encodedStegoFile, numOfBits):

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
        payload_BIN += byte[-numOfBits:]

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

decode(encodedStegoFile, numOfBits)