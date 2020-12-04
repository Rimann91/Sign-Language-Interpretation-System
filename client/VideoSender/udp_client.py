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


'''
    UDP Client to stream openCV video stream to server

    Author: Riley Hughes
    Organization: Missouri State University - CSC450 - Dr. Razib Iqbal
'''
import socket # for network objects
import sys    # for exiting on error catch
import numpy  # manipulating cv2 video frame
import cv2    # 

import feed

def send_stream():

    FRAME_DIVISIONS = 20 # Minnimum 20
    HEADER_SIZE = 40

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error:
        print('Failed to create socket')
        sys.exit()
    
    host = 'localhost'
    port = 8888

    fd = feed.video_feed()

    print("client started... ")

    frame_sequence = 0
    while True:

        frame = fd.get_frame()
        err, err_msg, data = frame[0], frame[1], frame[2]

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if not err:

            cv2.imshow("CLIENT", data)

            # convert data to streamable data
            d = data.flatten()
            s = d.tostring()
            
            """cv2 video capture default frame size = (480,640,3)"""
            frame_size = len(s) 

            slice_sequence = 0

            for i in range(FRAME_DIVISIONS):
                slc = s[i*frame_size//FRAME_DIVISIONS:(i+1)*frame_size//FRAME_DIVISIONS]
                slice_size = len(slc)
                packet = bytes(
                    f'{frame_size:<10}'+
                    f'{frame_sequence:<10}'+
                    f'{slice_size:<10}'+
                    f'{slice_sequence:<10}','utf-8')+slc
                sock.sendto(packet, (host,port))
                slice_sequence+=1

            frame_sequence+=1

        else: 
            print(err_msg)

    fd.end_feed()

