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