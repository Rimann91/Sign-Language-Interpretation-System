import cv2
import socket
import numpy
import time
from heapq import heappop, heappush, heapify

FRAME_DIVISIONS = 20
HEADER_SIZE = 40
FRAME_TIMEOUT = 0.1
UDP_IP="localhost"
UDP_PORT = 8888

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("server started....")

frame_heap=[]
timeout = 0
frame_size = 0
new_frame=True

while True:
    buffer = [b'' for x in range(FRAME_DIVISIONS)]
    #wait_buffer = []
    current_frame = 0
    current_frames = []
    new_frame = True

    while True:
        data, addr = sock.recvfrom(46120)

        if new_frame or (time.time()-timeout>FRAME_TIMEOUT):
            current_frame = int(data[10:20].decode('utf-8'))
            if len(frame_heap) > 0:
                buffer = heappop(frame_heap)[1:]
                timeout = time.time()
                current_frames.remove(current_frames)
            new_frame = False

        frame_size = int(data[:10].decode('utf-8'))
        frame_sequence = int(data[10:20].decode('utf-8'))
        slice_size = int(data[20:30].decode('utf-8'))
        slice_sequence = int(data[30:40].decode('utf-8'))
        #new_slice = False

        if frame_sequence == current_frame:
            #if data[HEADER_SIZE:] not in buffer:
            buffer[slice_sequence] = data[HEADER_SIZE:]
        
        else:
            #wait_buffer.insert(slice_sequence, data[HEADER_SIZE:])
            #frame_buffer[frame_sequence].insert(slice_sequence, data[HEADER_SIZE:])

            # if frame not already started
            if frame_sequence not in current_frames:
                d = [data[HEADER_SIZE:]]
                d.insert(0, frame_sequence)
                heappush(frame_heap, d)
                current_frames.append(frame_sequence)
            else:
                frame_heap[current_frames.index(frame_sequence)].insert(slice_sequence, [data[HEADER_SIZE:]])
        
        if len(b''.join(buffer)) == (frame_size):
            buffer = b''.join(buffer[:frame_size])
            frame = numpy.fromstring(buffer, dtype=numpy.uint8)
            buffer = numpy.fromstring(buffer, dtype=numpy.uint8)
            frame = frame.reshape(480,640,3)

            cv2.imshow("SERVER", frame)

            new_frame = True

            break


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

