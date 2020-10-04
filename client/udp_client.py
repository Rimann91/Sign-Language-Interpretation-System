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
        #sock = socket.socket(soaaaaacket.AF_INET, socket.SOCK_DGRAM)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error:
        print('Failed to create socket')
        sys.exit()
    
    host = 'localhost'
    port = 8888

    fd = feed.video_feed()
    frame_sequence = 0

    print("client started... ")

    n=''

    while True:



        frame = fd.get_frame()
        err, err_msg, data = frame[0], frame[1], frame[2]

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if not err:
            #seg = segment(priority_count, data)p

            #gray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
            #color = cv2.cvtColor(data, cv2.COLOR_BGR)
            cv2.imshow("CLIENT", data)

            #dg_struct["data"] = gray 
            # convert data to streamable data
            d = data.flatten()
            s = d.tostring()
            #d = pickle.dumps(dg_struct)

            #print(seg.d)
            #print(sys.getsizeof(d))
            #print(sys.getsizeof(dg_struct))
            
            """cv2 video capture default frame size = (480,640,3)"""
            frame_size = len(s) 

            slice_sequence = 0

            for i in range(FRAME_DIVISIONS):
                #print(sys.getsizeof(s))
                #slc = s[i*46080:(i+1)*46080]
                slc = s[i*frame_size//FRAME_DIVISIONS:(i+1)*frame_size//FRAME_DIVISIONS]
                slice_size = len(slc)
                packet = bytes(
                    f'{frame_size:<10}'+
                    f'{frame_sequence:<10}'+
                    f'{slice_size:<10}'+
                    f'{slice_sequence:<10}','utf-8')+slc
                sz = sys.getsizeof(packet)
                sock.sendto(packet, (host,port))
                slice_sequence+=1
            #s.sendto(d, (host,port))
            frame_sequence+=1

        else: 
            print(err_msg)


    
    fd.end_feed()

