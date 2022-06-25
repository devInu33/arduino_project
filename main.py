# import io
# import os
# import socket
# import struct
# import time
#
# from PIL import Image
# import numpy as np
# import cv2
# import urllib
# from test import test
#
# serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # address '0.0.0.0' or '' work to allow connections from other machines.  'localhost' disallows external connections.
# # see https://www.raspberrypi.org/forums/viewtopic.php?t=62108
# serv.bind(('0.0.0.0', 8090))
# serv.listen(5)
# print("Ready to accept 0 connections")
# file_name = "test.jpg"
#
# def create_image_from_bytes(image_bytes) -> Image.Image:
#     stream = io.BytesIO(image_bytes)
#     return Image.open(stream)
#
#
#
# while True:
#     conn, addr = serv.accept()
#     array_from_client =bytearray()
#     shape = None
#     chunks_received = 0
#     start = time.time()
#     shape_string = ''
#     received = False
#     width=0
#     height=0
#     while True:
#         print('waiting for data')
#         # Try 4096 if unsure what buffer size to use. Large transfer chunk sizes (which require large buffers) can cause corrupted results
#         data = conn.recv(1024)
#
#         if not data:
#             break
#         # elif data.decode("utf-8")=="Not Available":
#         #     continue
#         elif shape is None:
#             shape_string += data.decode("utf-8")
#             # Find the end of the line.  An index other than -1 will be returned if the end has been found because
#             # it has been received
#             if shape_string.find('\r\n') != -1:
#                 width_index = shape_string.find('width:')
#                 height_index = shape_string.find('height:')
#                 width = int(shape_string[width_index + len('width:'): height_index])
#                 height = int(shape_string[height_index + len('height:'):])
#                 shape = (width, height)
#             print("shape is {}".format(shape))
#         received=True
#         chunks_received += 1
#         array_from_client.extend(data)
#         # print(array_from_client)
#         # conn.sendall(b'ack')
#     if not received: continue
#     print("chunks_received {}. Number of bytes {}".format(chunks_received, len(array_from_client)))
#
#     # image = Image.open(io.BytesIO(array_from_client))
#     # image.show()
#     try:
#
#         f= open(file_name, "wb")
#         f.write(array_from_client)
#         f.close()
#         array_start_time = time.time()
#
#         # img = Image.open(io.BytesIO(array_from_client))
#
#         val = test(file_name)
#
#     except Exception as e:
#         print(e)
#         conn.close()
#         print('failed to open image. client disconnected')
#         continue
#     array_start_time = time.time()
#     conn.close()
#     print('succeded to open image. client disconnected')

import io
import os
import socket
import struct
import time
import cv2
import urllib.request
import numpy as np
import time
from test import test

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)







url = 'http://192.168.0.18/capture'
# values = {"query":"python"}
# data = urllib.parse.urlencode(values).encode('utf-8')
# headers = {'Content-Type': 'text/plain'}
# req = urllib.request.Request(url, data, headers)
while True:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('192.168.0.18', 80))
        imgResp = urllib.request.urlopen(url)
        imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
        img = cv2.imdecode(imgNp, -1)
        cv2.imshow("img",img)
        res = 1 if test(img) else 0
        ans = struct.pack('!i', res)
        sock.send(ans)
        print(f"sent {ans}")

    except Exception as e:
        print(e)
        print('failed to open image.')
        sock.close()
        time.sleep(10)
        continue
    sock.close()
    print("succeded to open image. client disconnected")
    time.sleep(10)
