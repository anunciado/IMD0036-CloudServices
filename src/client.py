# coding: utf-8
# author: cruxiu

import cv2 # imread, threshold, cvtColor
import zmq # socket, connect, recv_string, recv, send_string, send
import pickle # loads, dumps
import sys # argv
import getopt # getopt
import numpy as np #array

def process(image, port, process_type):
    context = zmq.Context()
    #  Socket to talk to server
    print("</Connecting to server " + str(port) + " to process input image>")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:" + str(port))
    # Send process type
    socket.send_string(process_type)
    #  Get the reply.
    process_type_answer = socket.recv()
    # Serialization
    image_client_pickle = serialization(imgYCC)
    # Send bytes object to server
    socket.send(image_client_pickle)
    #  Get the reply.
    image_server_pickle = socket.recv()
    # Deserialization
    image_server = deserialization(image_server_pickle)
    # Disconnect from the socket and destroy context
    print("</Disconnecting from the server " + str(port) + " that send output image>")
    socket.disconnect("tcp://localhost:" + str(port))
    context.destroy()
    return image_server

def limiarization(image, thresh):
    ret, thresh = cv2.threshold(image_client, thresh, 255, cv2.THRESH_BINARY)
    return thresh

def transform(image, type_input , type_output):
    if (type_input == 1 and type_output == 2):
        imgYCC = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)
        return imgYCC
    elif (type_input == 2 and type_output == 1):
        imgRGB = cv2.cvtColor(image, cv2.COLOR_YCrCb2BGR)
        return imgRGB
    else:
        return image

def serialization(image):
    image_pickle = pickle.dumps(image)
    return image_pickle

def deserialization(image):
    image_pickle = pickle.loads(image)
    return image_pickle

# Read commandline arguments, except first
argumentList = sys.argv[1:]

# Arguments needed
unixOptions = "i:o:p:t:h"
gnuOptions = ["input=", "output=", "port=", "technique=", "help"]

try:
    arguments, values = getopt.getopt(argumentList, unixOptions, gnuOptions)
except getopt.error as err:
    # Output error, and return with an error code
    print (str(err))
    sys.exit(2)

# Evaluate given options
for currentArgument, currentValue in arguments:
    if currentArgument in ("-i", "--input"):
        input_file = currentValue
    elif currentArgument in ("-o", "--output"):
        output_file = currentValue
    elif currentArgument in ("-p", "--port"):
        port = currentValue
    elif currentArgument in ("-t", "--technique"):
        process_type = currentValue
    elif currentArgument in ("-h", "--help"):
        print 'client.py -i <inputfile> -o <outputfile> -p <port> -t <technique>'
        sys.exit(0)

print("</Reading input image>")
# Read file
image_client = cv2.imread(input_file)
# Thresholding
thresh = limiarization(image_client, 127)
# Convert RGB into YCbCr
imgYCC = transform(thresh, 1 , 2)
print("</Processing input image>")
# Process image
image_server = process(imgYCC, port, process_type)
print("</Output image saved at " + output_file + ">")
# Save file
cv2.imwrite(output_file, image_server)
