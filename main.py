import io
import socket
import struct
import time

import numpy as np
from PIL import Image
import cv2
from test import test


serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# address '0.0.0.0' or '' work to allow connections from other machines.  'localhost' disallows external connections.
# see https://www.raspberrypi.org/forums/viewtopic.php?t=62108
serv.bind(('0.0.0.0', 20))
serv.listen(0)
print("Ready to accept 5 connections")


def create_image_from_bytes(image_bytes) -> Image.Image:
    stream = io.BytesIO(image_bytes)
    return Image.open(stream)


while True:
    conn, addr = serv.accept()
    array_from_client = bytearray()
    shape = None
    chunks_received = 0
    start = time.time()
    shape_string = ''
    while True:
        # print('waiting for data')
        # Try 4096 if unsure what buffer size to use. Large transfer chunk sizes (which require large buffers) can cause corrupted results
        data = conn.recv(4096)
        if not data or data == b'tx_complete':
            break
        chunks_received += 1
        array_from_client.extend(data)
        # print(array_from_client)
        # conn.sendall(b'ack')
    #     TODO: need to check if sending acknowledgement of the number of chunks and the total length of the array is a good idea
    print("chunks_received {}. Number of bytes {}".format(chunks_received, len(array_from_client)))
    img: Image.Image = create_image_from_bytes(array_from_client)
    val = struct.pack("!i", test(img))
    conn.send(val)
    array_start_time = time.time()
    print('array conversion took {} s'.format(time.time() - array_start_time))
    conn.close()
    print('client disconnected')