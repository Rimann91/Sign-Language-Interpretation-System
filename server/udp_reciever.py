import cv2
import socket
import numpy

UDP_IP="localhost"
UDP_PORT = 8888

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("server started....")

frame_buffer=[]
frame_size = 0
new_frame=True

while True:
    buffer=[]
    new_slice = True

    while True:
        data, addr = sock.recvfrom(46120)
        if data:
            pass

        if new_slice:
            frame_size = int(data[:10].decode('utf-8'))
            frame_sequence = int(data[10:20].decode('utf-8'))
            slice_size = int(data[20:30].decode('utf-8'))
            slice_sequence = int(data[30:40].decode('utf-8'))
            #new_slice = False

        typ = type(data)
        buffer.insert(slice_sequence,data[40:])
        
        if len(b''.join(buffer)) == (frame_size):
            buffer = b''.join(buffer[:frame_size])
            s = len(buffer)
            #frame_buffer.insert(slice_sequence, buffer[40:])
            frame = numpy.fromstring(buffer, dtype=numpy.uint8)
            frame = frame.reshape(480,640,3)

            cv2.imshow("SERVER", frame)

            break

    #current_frame_size = len(frame_buffer)

    #if len(frame_buffer) == 20:
    #    frame_buffer = b', '.join(frame_buffer)
    #    #s.decode()
    #    frame = numpy.fromstring(frame_buffer, dtype=numpy.uint8)
    #    frame = frame.reshape(480,640,3)
    #    cv2.imshow("SERVER", frame)
    #    frame = ''
    #    frame_buffer = b''
    #    new_frame = True

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

