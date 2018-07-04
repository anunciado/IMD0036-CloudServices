# coding: utf-8
# author: cruxiu

import cv2 # filter2D, imread, threshold, multiply, add
import zmq # socket, bind, recv_string, recv, send_string, send
import pickle # loads, dumps
import sys # argv
import getopt # getopt
import signal # signal
import os # kill, getpid
from functools import partial  # partial
import numpy as np #array

def signal_handler(port, socket, context, signal, frame):
    print("</Ending process image server at " + port + ">")
    socket.unbind("tcp://*:" + port)
    socket.close()
    context.destroy()
    os.kill(os.getpid(), signal.SIGKILL)

def process(image, alpha_file, process_type):
    # Deserialization
    image_client = deserialization(image_client_pickle)
    if (process_type == "alpha"):
        # Alfa Blending
        src = cv2.imread(alpha_file)
        filtered = alphaTransform(image_client, src)
    elif (process_type == "horizontal"):
        # horizontal edge detector
        kernel = np.array([[1, 0, -1],
                           [1, 0, -1],
                           [1, 0, -1]])
        filtered = filterTransform(image_client, kernel)
    elif (process_type == "vertical"):
        # vertical edge detector
        kernel = np.array([[1,  1,  1],
                           [0,  0,  0],
                           [-1, -1, -1]])
        filtered = filterTransform(image_client, kernel)
    elif (process_type == "blurring"):
        # blurring ("box blur", because it's a box of ones)
        kernel = np.array([[1, 1, 1],
                           [1, 1, 1],
                           [1, 1, 1]]) / 9.0
        filtered = filterTransform(image_client, kernel)
    elif (process_type == "sharpening"):
        # sharpening
        kernel = (np.array([[-1, -1, -1],
                            [-1,  9, -1],
                            [-1, -1, -1]]))
        filtered = filterTransform(image_client, kernel)
    else:
        print("</Process image unknown>")
        filtered = image
    # Serialization
    image_server_pickle = serialization(filtered)
    return image_server_pickle

def alphaTransform(dest, src):
    foreground = dest
    background = src
    ret, alpha = cv2.threshold(foreground, 127,255, cv2.THRESH_BINARY_INV)
    # Convert uint8 to float
    foreground = foreground.astype(float)
    background = background.astype(float)

    # Normalize the alpha mask to keep intensity between 0 and 1
    alpha = alpha.astype(float)/255

    # Multiply the foreground with the alpha matte
    foreground = cv2.multiply(alpha, foreground)

    # Multiply the background with ( 1 - alpha )
    background = cv2.multiply(1.0 - alpha, background)

    # Add the masked foreground and background.
    image_alpha = cv2.add(foreground, background)

    return image_alpha

def filterTransform(dest, kernel):
    filtered = cv2.filter2D(src=dest, kernel=kernel, ddepth=-1)
    return filtered

def serialization(image):
    image_pickle = pickle.dumps(image)
    return image_pickle

def deserialization(image):
    image_pickle = pickle.loads(image)
    return image_pickle

# Read commandline arguments, except first
argumentList = sys.argv[1:]

# Arguments needed
unixOptions = "a:p:h"
gnuOptions = ["alpha=", "port=", "help"]

try:
    arguments, values = getopt.getopt(argumentList, unixOptions, gnuOptions)
except getopt.error as err:
    # Output error, and return with an error code
    print (str(err))
    sys.exit(2)

# Evaluate given options
for currentArgument, currentValue in arguments:
    if currentArgument in ("-a", "--alpha"):
        alpha_file = currentValue
    elif currentArgument in ("-p", "--port"):
        port = currentValue
    elif currentArgument in ("-h", "--help"):
        print 'server.py -a <alphafile> -p <port>'
        sys.exit(0)

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:" + port)
print("</Starting process image server at " + port + ">")

while True:
    # Receive signal to kill the server
    signal.signal(signal.SIGINT, partial(signal_handler, port, socket, context))
    # Receive process type
    process_type = socket.recv_string()
    #print (socket.poll())
    # Send reply back to client
    socket.send_string("</Receive process type>")
    # Wait for next request from client
    image_client_pickle = socket.recv()
    # Process image
    print("</Processing input image>")
    image_server_pickle = process(image_client_pickle, alpha_file, process_type)
    # Send reply back to client
    print("</Send output image>")
    socket.send(image_server_pickle)
