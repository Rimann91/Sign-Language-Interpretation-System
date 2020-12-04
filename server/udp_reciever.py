#    Copyright 2020 Braden Bagby, Robert Stonner, Riley Hughes, David Gray, Zachary Langford

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.


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
MEDIAPIPE_PORT = 4433
MEDIAPIP_IP = "localhost"
FRAME_SEND_TIME = 0.033 #30 frames / second

class server():
    def __init__(self):
        print("init")


    def udp_recieve(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((UDP_IP, UDP_PORT))

        print("server started....")

        frame_heap=[]
        timeout = 0
        frame_size = 0
        new_frame=True
        frame_timer = time.time()

        while True:
            buffer = [b'' for x in range(FRAME_DIVISIONS)]
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

                if frame_sequence == current_frame:
                    buffer[slice_sequence] = data[HEADER_SIZE:]
                
                else:

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
                    frame = frame.reshape(480,640,3)

                    if (time.time() - frame_timer) > FRAME_SEND_TIME:
                        self.tcp_sendtomp(frame)
                        frame_timer = time.time()

                    new_frame = True

                    break


            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


    def tcp_sendtomp(self, frame):
       
        
        try:
            self.sock_mp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock_mp.connect((MEDIAPIP_IP, MEDIAPIPE_PORT))
        except socket.error as e:
            print(f"Failed to create TCP socket for mediapipe connection...  {e}")
        
        _,frame_jpg = cv2.imencode('.jpg', frame)
        #cv2.imshow("mediapipe image",frame) #we show the frame in mediapipe with hand detection
        try:
            self.sock_mp.sendall(frame_jpg)
            self.sock_mp.close()
        except socket.error as e:
            print("Failed sending jpg to mediapipe... {e}")
        
server = server()
server.udp_recieve()

main()