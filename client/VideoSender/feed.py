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

class video_feed():

    def __init__(self):

        self.cap = cv2.VideoCapture(0)

    def get_frame(self):

        bln_error = False 
        error_message = ""

        # exit client if can't recieve camera feed
        if self.cap.isOpened():
            #capture frame by frame
            ret, frame = self.cap.read()

            if ret:
                #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                #cv2.imshow('feed_frame', frame)
                pass

            else:
                error_message = "Can't recieve frame (stream end?). Exiting..."
                bln_error = True 
                return (bln_error, error_message)

        else:
            error_message = "Cannot open camera"
            bln_error = True 
            return (bln_error, error_message)

        return (bln_error, error_message, frame)

    def end_feed(self):
        self.cap.release()
        cv2.destroyAllWindows()