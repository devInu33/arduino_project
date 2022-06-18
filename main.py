import io
import os
import socket
import struct
import time

from PIL import Image
import numpy as np
import cv2
from test import test

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# address '0.0.0.0' or '' work to allow connections from other machines.  'localhost' disallows external connections.
# see https://www.raspberrypi.org/forums/viewtopic.php?t=62108
serv.bind(('0.0.0.0', 8090))
serv.listen(5)
print("Ready to accept 0 connections")
file_name = "test.jpg"

def create_image_from_bytes(image_bytes) -> Image.Image:
    stream = io.BytesIO(image_bytes)
    return Image.open(stream)



while True:
    conn, addr = serv.accept()
    array_from_client =bytearray()
    shape = None
    chunks_received = 0
    start = time.time()
    shape_string = ''
    received = False
    width=0
    height=0
    while True:
        print('waiting for data')
        # Try 4096 if unsure what buffer size to use. Large transfer chunk sizes (which require large buffers) can cause corrupted results
        data = conn.recv(1024)

        if not data:
            break
        # elif data.decode("utf-8")=="Not Available":
        #     continue
        elif shape is None:
            shape_string += data.decode("utf-8")
            # Find the end of the line.  An index other than -1 will be returned if the end has been found because
            # it has been received
            if shape_string.find('\r\n') != -1:
                width_index = shape_string.find('width:')
                height_index = shape_string.find('height:')
                width = int(shape_string[width_index + len('width:'): height_index])
                height = int(shape_string[height_index + len('height:'):])
                shape = (width, height)
            print("shape is {}".format(shape))
        received=True
        chunks_received += 1
        array_from_client.extend(data)
        # print(array_from_client)
        # conn.sendall(b'ack')
    if not received: continue
    print("chunks_received {}. Number of bytes {}".format(chunks_received, len(array_from_client)))
    # image = Image.open(io.BytesIO(array_from_client))
    # image.show()
    try:
        # img = Image.frombuffer('RGB', (width, height), bytes(array_from_client))
        bytes = io.BytesIO(array_from_client)
        img = Image.open(bytes)
        val = test(img)

    except Exception as e:
        print(e)
        conn.close()
        print('failed to open image. client disconnected')
        continue
    array_start_time = time.time()
    conn.close()
    print('succeded to open image. client disconnected')