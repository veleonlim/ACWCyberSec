import math
from os import path
import base64
import os
import shutil
import cv2
import numpy as np
from subprocess import call,STDOUT

# Embed secret in the n least significant bit.
# Lower n make picture less loss but lesser storage capacity.




def insert(img_path, msg,BITS):
    HIGH_BITS = 256 - (1 << BITS)
    LOW_BITS = (1 << BITS) - 1
    BYTES_PER_BYTE = math.ceil(8 / BITS)
    FLAG = '%'
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
        encode(data[idx * BYTES_PER_BYTE: (idx + 1) * BYTES_PER_BYTE], val,HIGH_BITS,LOW_BITS,BITS)

    img = np.reshape(data, ori_shape)
    filename, _ = path.splitext(img_path)
    filename += '_lsb_embeded' + ".png"
    cv2.imwrite(filename, img)
    return filename


def encode(block, data,HIGH_BITS,LOW_BITS,BITS):
    # returns the Unicode code from a given character
    data = ord(data)
    for idx in range(len(block)):
        block[idx] &= HIGH_BITS
        block[idx] |= (data >> (BITS * idx)) & LOW_BITS


import cv2
import math
import numpy as np

def decode(block, LOW_BITS, BITS):
    val = 0
    for idx in range(len(block)):
        val |= (block[idx] & LOW_BITS) << (idx * BITS)
    return chr(val)


def extract(path, BITS):
    HIGH_BITS = 256 - (1 << BITS)
    LOW_BITS = (1 << BITS) - 1
    BYTES_PER_BYTE = math.ceil(8 / BITS)
    FLAG = '%'
    img = cv2.imread(path, cv2.IMREAD_ANYCOLOR)
    data = np.reshape(img, -1)
    total = data.shape[0]
    res = ''
    idx = 0

    try:
        # Decode message length
        while idx < total // BYTES_PER_BYTE:
            ch = decode(data[idx * BYTES_PER_BYTE: (idx + 1) * BYTES_PER_BYTE], LOW_BITS, BITS)
            idx += 1
            if ch == FLAG:
                break
            res += ch
        end = int(res) + idx
        assert end <= total // BYTES_PER_BYTE, "Input image isn't correct."

        secret = ''
        while idx < end:
            secret += decode(data[idx * BYTES_PER_BYTE: (idx + 1) * BYTES_PER_BYTE], LOW_BITS, BITS)
            idx += 1

        return secret

    except ValueError:
        print("Invalid LSB. Failed to extract secret message.")
        return "Invalid LSB. Failed to extract secret message."






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

#Encoding video

 # # checking if the image exists on given path
    # def is_image_path_valid(self):
    #     if os.path.exists(self.image_path):
    #         return True
    #     return False

    # Method to convert data into binary format
    
def dataToBinary(data):
        if type(data) == str:
            return ''.join([format(ord(i), "08b") for i in data])
        elif type(data) == bytes or type(data) == np.ndarray:
            return [format(i, "08b") for i in data]
        elif type(data) == int or type(data) == np.uint8:
            return format(data, "08b")
        else:
            # Input type not able to be changed to binary
            raise TypeError("Input type not supported")

def frameExtraction(videoPath):
        # Create a temp folder if it does not exist
        if not os.path.exists("./tmp"):
            os.makedirs("tmp")
        tempFolder="./tmp"

        # Opens the video file using OpenCV library
        vidcap = cv2.VideoCapture(videoPath)
        count = 0
        fps = vidcap.get(cv2.CAP_PROP_FPS)
        imgResolution = 0
        imgChannel = 0
        while True:
            # Read each frame from the video
            success, image = vidcap.read()
            if not success:
                # Return after all frames have been read
                return [count, imgResolution, imgChannel, fps]
            # Save each frame from the video into a temp folder
            cv2.imwrite(os.path.join(tempFolder, "{:d}.png".format(count)), image)
            count += 1
            imgResolution = image.shape[0] * image.shape[1]
            imgChannel = image.shape[2]

    # Method to hide/encode the encrypted binary data into the cover object
def hideData(coverVidPath,payloadType,numOfBits,isPath):
        # Find extension of cover video
        coverName = os.path.splitext(os.path.basename(coverVidPath))[0]
        coverExt = os.path.splitext(os.path.basename(coverVidPath))[1]
   
        # Check if payload is a file
        if isPath:
            payloadPath = os.path.join(os.getcwd(), payloadType)

            # Opens the payload object and encodes it into a Base64 format
            payloadB64 = ''
            with open(payloadPath, "rb") as payload:
                payloadB64 = base64.b64encode(payload.read())

            # Find extension of payload object
            payloadExt = os.path.splitext(payloadPath)[1]

            # Add padding to file extention untill there is 10 characters
            while len(payloadExt) < 10:
                payloadExt += '@'

            # Converts the encoded Base64 payload into a string and adds the file extention and the delimeter to indicate the end of the file
            payloadEncode = str(payloadB64) + payloadExt + '#####'
        # If payload is a string
        else:
            payloadString = payloadType
            # Encodes the payload into a Base64 format
            payloadB64 = base64.b64encode(payloadString.encode('utf-8'))
            # Converts the encoded Base64 payload into a string and adds the delimeter to indicate the end of the file
            payloadEncode = str(payloadB64) + '$' + '#####'


        # Extract the frames from the cover video
        frameExtracted = frameExtraction(coverVidPath)

        # Get the number of total frames, each frame's resolution, the channel for the frames (3 for RGB and 4 for RGBA) and the fps of the video
        numOfFrames = frameExtracted[0]
        imgResolution = frameExtracted[1]
        imgChannels = frameExtracted[2]
        fps = frameExtracted[3]

        # Extract the audio from the cover video
        call(["ffmpeg", "-i",coverVidPath, "-q:a", "0", "-map", "a", "tmp/audio.mp3", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)

        # Calculate the maximum bytes that can be encoded for the cover video
        maxBytes = numOfFrames * ((imgResolution * numOfBits * 3) // 8)
        print("Maximum bytes to encode:", maxBytes)

        # Check if the number of bytes of the payload object to encode is less than the maximum bytes in the cover video
        print('Payload size: ', len(payloadEncode))
        if len(payloadEncode) > maxBytes:
            raise ValueError("Error encountered insufficient bytes, need bigger video or less data !!")

        # Converts the encoded payload string to binary format
        dataToHideBin = dataToBinary(payloadEncode)

        # Get the length of the encoded payload binary
        dataLen = len(dataToHideBin)

        # setting a local variable to point to the binary value to encode in each iteration
        dataIndex = 0

        # Loop through frame of the cover video
        for frame in range(numOfFrames):
            # Break the loop if all the data have been hidden
            if (dataIndex >= dataLen):
                break
            
            # Opens the current frame image using OpenCV library
            imgPath = os.path.abspath("./tmp/{:d}.png".format(frame))
            image = cv2.imread(imgPath)

            print('Hiding in frame: ', frame+1)
            # Loop through each pixel in the current frame
            for values in image:
                # Break the loop if all the data have been hidden
                if (dataIndex >= dataLen):
                    break
                for pixel in values:
                    r = 0
                    g = 0
                    b = 0
                    a = 0
                    
                    if imgChannels == 3:
                        # convert RGB values to binary format
                        r, g, b = dataToBinary(pixel)
                    elif imgChannels == 4:
                        # convert RGBA values to binary format
                        r, g, b, a = dataToBinary(pixel)

                    # modify the least significant bit only if there is still data to store
                    if dataIndex < dataLen:
                        tempBin = ''
                        # Remove the last few digits of the red pixel binary based on the number of LSB used
                        r = r[:-numOfBits]
                        # Loop and store the data to hide into a temp variable
                        for x in range(numOfBits):
                            tempBin += dataToHideBin[dataIndex]
                            dataIndex += 1
                            # Break the loop if all the data have been hidden
                            if dataIndex == dataLen:
                                break
                        # Pad 0 to the front of the temp binary if the length of the temp binary is less than the number of LSB used
                        if len(tempBin) < numOfBits:
                            tempBin = tempBin.ljust(numOfBits, '0')
                        # Adds the temp binary to the pixel binary and change it into an integer and assign it to the pixel array
                        pixel[0] = int(r + tempBin, 2)
                    if dataIndex < dataLen:
                        tempBin = ''
                        # Remove the last few digits of the green pixel binary based on the number of LSB used
                        g = g[:-numOfBits]
                        # Loop and store the data to hide into a temp variable
                        for x in range(numOfBits):
                            tempBin += dataToHideBin[dataIndex]
                            dataIndex += 1
                            # Break the loop if all the data have been hidden
                            if dataIndex == dataLen:
                                break
                        # Pad 0 to the front of the temp binary if the length of the temp binary is less than the number of LSB used
                        if len(tempBin) < numOfBits:
                            tempBin = tempBin.ljust(numOfBits, '0')
                        # Adds the temp binary to the pixel binary and change it into an integer and assign it to the pixel array
                        pixel[1] = int(g + tempBin, 2)
                    if dataIndex < dataLen:
                        tempBin = ''
                        # Remove the last few digits of the blue pixel binary based on the number of LSB used
                        b = b[:-numOfBits]
                        # Loop and store the data to hide into a temp variable
                        for x in range(numOfBits):
                            tempBin += dataToHideBin[dataIndex]
                            dataIndex += 1
                            # Break the loop if all the data have been hidden
                            if dataIndex == dataLen:
                                break
                        # Pad 0 to the front of the temp binary if the length of the temp binary is less than the number of LSB used
                        if len(tempBin) < numOfBits:
                            tempBin = tempBin.ljust(numOfBits, '0')
                        # Adds the temp binary to the pixel binary and change it into an integer and assign it to the pixel array
                        pixel[2] = int(b + tempBin, 2)
                    if (dataIndex < dataLen) and (imgChannels == 4): # If channel is 4 (RGBA image)
                        tempBin = ''
                        # Remove the last few digits of the black pixel binary based on the number of LSB used
                        a = a[:-numOfBits]
                        # Loop and store the data to hide into a temp variable
                        for x in range(numOfBits):
                            tempBin += dataToHideBin[dataIndex]
                            dataIndex += 1
                            # Break the loop if all the data have been hidden
                            if dataIndex == dataLen:
                                break
                        # Pad 0 to the front of the temp binary if the length of the temp binary is less than the number of LSB used
                        if len(tempBin) < numOfBits:
                            tempBin = tempBin.ljust(numOfBits, '0')
                        # Adds the temp binary to the pixel binary and change it into an integer and assign it to the pixel array
                        pixel[3] = int(a + tempBin, 2)

                    # Break the loop if all the data have been hidden
                    if dataIndex >= dataLen:
                        break

            # Save the edited frame
            cv2.imwrite(os.path.join(os.getcwd(), "tmp/{:d}.png".format(frame)), image)

        # Write the output stego object to a temp video file 
        call(["ffmpeg", "-framerate", str(fps), "-i", "tmp/%d.png", "-vcodec", "png", "tmp/temp.avi", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)
        
        # Puts the audio back to the temp video file
        call(["ffmpeg", "-i", "tmp/temp.avi", "-i", "tmp/audio.mp3", "-codec", "copy", "tmp/outputVid.avi", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)

        # Change the temp video file into a format that can be played
        call(["ffmpeg", "-i", "tmp/outputVid.avi", "-f", "avi", "-c:v", "rawvideo", "-pix_fmt", "rgb32", coverName+"_encoded"+coverExt, "-y"], stdout=open(os.devnull, "w"), stderr=STDOUT)

        # Clears the temp folder
        if os.path.exists("./tmp"):
            shutil.rmtree("./tmp")
        return coverName+"_encoded"+coverExt


#decode Video
# Method to convert data into binary format


def frameExtraction(videoPath):
        # Create a temp folder if it does not exist
        if not os.path.exists("./tmp"):
            os.makedirs("tmp")
        tempFolder="./tmp"

        # Opens the video file using OpenCV library
        vidcap = cv2.VideoCapture(videoPath)
        count = 0
        fps = vidcap.get(cv2.CAP_PROP_FPS)
        imgResolution = 0
        imgChannel = 0
        while True:
            # Read each frame from the video
            success, image = vidcap.read()
            if not success:
                # Return after all frames have been read
                return [count, imgResolution, imgChannel, fps]
            # Save each frame from the video into a temp folder
            cv2.imwrite(os.path.join(tempFolder, "{:d}.png".format(count)), image)
            count += 1
            imgResolution = image.shape[0] * image.shape[1]
            imgChannel = image.shape[2]

    # Method to show/decode the data hidden in the video
def showData(stegoObjPath,numOfBits):
        # Extract the frames from the stego video and get the number of total frames, each frame's resolution and the channel for the frames (3 for RGB and 4 for RGBA)
        frameExtracted = frameExtraction(stegoObjPath)
        numOfFrames = frameExtracted[0]
        imgChannels = frameExtracted[2]

        # Find name of stego video
        stegoName = os.path.splitext(stegoObjPath)[0]

        decodedData = ""
        # Loop through each frame of the stego video
        for frame in range(numOfFrames):
            # Empty variable to store the binary data extracted from the image
            binaryData = ''

            
            # Stop decoding after we have reached the delimeter which is "#####"
            if decodedData[-5:] == "#####":
                    break

            print('Processing frame: ', frame+1)

            # Opens the current frame image using OpenCV library
            imgPath = os.path.abspath("./tmp/{:d}.png".format(frame))
            image = cv2.imread(imgPath)

            # Loop through each pixel in the current frame
            for values in image:
                for pixel in values:

                    if imgChannels == 3:
                        # convert RGB values to binary format
                        r, g, b = dataToBinary(pixel)
                        binaryData += r[-numOfBits:] #extracting data from the LSB of red pixel based on bits specified by user
                        binaryData += g[-numOfBits:] #extracting data from the LSB of green pixel based on bits specified by user
                        binaryData += b[-numOfBits:] #extracting data from the LSB of blue pixel based on bits specified by user
                    elif imgChannels == 4:
                        # convert RGBA values to binary format
                        r, g, b, a = dataToBinary(pixel)
                        binaryData += r[-numOfBits:] #extracting data from the LSB of red pixel based on bits specified by user
                        binaryData += g[-numOfBits:] #extracting data from the LSB of green pixel based on bits specified by user
                        binaryData += b[-numOfBits:] #extracting data from the LSB of blue pixel based on bits specified by user
                        binaryData += a[-numOfBits:] #extracting data from the LSB of black pixel based on bits specified by user
            
            # split the binary data to groups of 8
            allBytes = [binaryData[i: i+8] for i in range(0, len(binaryData), 8)]
            
            # convert from bits to characters
            tempList = ''
            for byte in allBytes:
                tempList += chr(int(byte, 2))
                # Stop decoding after we have reached the delimeter which is "#####"
                if tempList[-5:] == "#####":
                    break

            decodedData += tempList
                
        # Removes delimeter
        decodedData = decodedData[:-5]
        # Check if payload is a file or text
        if decodedData[-1:] == '$':
            # Remove '$' from decoded data
            decodedData = decodedData[:-1]
            # Converts the hidden data back to text from a Base64 format
            decodedData = base64.b64decode(eval(decodedData))
            fileExt = ".txt"
            # Write the decoded data back to a .txt file and saves it
            with open(stegoName + "_decoded.txt", "wb") as outFile:
                outFile.write(decodedData)

        else:
            # Get the file extension and removes it
            fileExt = decodedData[-10:]
            decodedData = decodedData[:-10]
            # Remove padding from file extention
            fileExt = fileExt.replace("@", "")

            # Converts the hidden data back to a file from a Base64 format
            decodedData = base64.b64decode(eval(decodedData))

            # Write the decoded data back to a file and saves it
            with open(stegoName + "_decoded" + fileExt, "wb") as outFile:
                outFile.write(decodedData)
            
        decodedData = decodedData.decode("utf-8").strip("b'")
        print(decodedData)
        # Clears the temp folder
        if os.path.exists("./tmp"):
            shutil.rmtree("./tmp")

        return decodedData