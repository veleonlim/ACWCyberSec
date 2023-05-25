import numpy as np
import base64
import os.path

cover_source = "coverfile.docx"
payload_source = "password.txt"
numOfBits = 1

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

def encodeDocument(cover_source,payload_source,numOfBits):

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

    # Converts encoded payload into a string, include Payload's extension and adds delimeter 
    # Delimeter is for decoder to identify end of payload (Stop stegnograph decoding)
    payloadEncode = str(payload_64) + payload_ext + "%$&@"

    # Converting BYTES into BITS
    #cover_BITS = convertBITS(cover_BYTES)
    payload_BITS = convertBITS(payloadEncode)
    
    # Outputs information of Cover Byte length and binary/bits length of payload
    print("Byte Length (Cover):", len(cover_BYTES))
    print("Binary Length (Payload)", len(payload_BITS))

    # Throws error if payload length is lesser than cover length (Insufficient bytes to stegnograph the payload into cover)
    if len(payload_BITS) / numOfBits > len(cover_BYTES):
        raise ValueError("[!] Insufficient bytes, need bigger cover document")
    
    # CoverBytesList stores a series of bits (8 bits) at each index e.g. [10101010, 00001111, 11110101]
    coverByteList = []
    for i in range(0, len(cover_BYTES)):
        coverByteList.append(convertBITS(cover_BYTES[i]))
    
    payloadBITS_len = len(payload_BITS)

    # "Pointer" to keep track of which bits of payload has already been completed.
    dataIndex = 0

    for i, byte_in_BITS in enumerate(coverByteList):
        # If there is still more data to store
        if dataIndex < payloadBITS_len:
            tempBin = ''
            # Remove the last few digits of the byte based on the number of LSB used
            byte_in_BITS = byte_in_BITS[:-numOfBits]
            # Loop and store the data to hide into a temp variable
            for x in range(numOfBits):
                tempBin += payload_BITS[dataIndex]
                dataIndex += 1
                # Break the loop if all the data have been hidden
                if dataIndex == payloadBITS_len:
                    break
            # Pad 0 to the front of the temp binary if the length of the temp binary is less than the number of LSB used
            if len(tempBin) < numOfBits:
                tempBin = tempBin.ljust(numOfBits, '0')
            # Adds the temp binary to the byte and change it into an integer and assign it to the back to the array of bytes
            coverByteList[i] = byte_in_BITS + tempBin

    # Converting the encoded Text from BITS into human readable CHAR
    encodedText = convertCHAR(coverByteList)

    print("\nEncoded Text(Stego):", encodedText)
    print("Encoded Text Length:", len(encodedText), "\n")
    print("########### Encoding Successful ###########\n")

    stegoObjName = input("Filename to save as (Without file extension): ")
    with open(stegoObjName + cover_ext, "wb") as outFile:
        outFile.write(encodedText.encode('utf-8'))

encodeDocument(cover_source,payload_source,numOfBits)



