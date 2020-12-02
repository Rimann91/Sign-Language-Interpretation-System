
////Mdified by Braden Bagby
////Modifications marked starting with ------------Modification BB------------------
///and ending with ------------Modification END BB------------------

#include <cmath>
#include <iostream>
#include <fstream>
#include <string>
#include <vector>

#include "mediapipe/framework/calculator_framework.h"
#include "mediapipe/framework/calculator_options.pb.h"
#include "mediapipe/framework/formats/landmark.pb.h"
#include "mediapipe/framework/formats/rect.pb.h"
#include "mediapipe/framework/port/ret_check.h"
#include "mediapipe/framework/port/status.h"

////------------Modification BB------------------
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <netdb.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <sys/socket.h>

#include <arpa/inet.h>

#define PORT "6009" // the port client will be connecting to
////------------Modification END BB------------------

namespace mediapipe
{

    namespace
    {
        constexpr char normRectTag[] = "NORM_RECT";
        constexpr char normalizedLandmarkListTag[] = "NORM_LANDMARKS";
    } // namespace

    class HandGestureRecognitionCalculator : public CalculatorBase
    {
    public:
        static ::mediapipe::Status GetContract(CalculatorContract *cc);
        ::mediapipe::Status Open(CalculatorContext *cc) override;

        ::mediapipe::Status Process(CalculatorContext *cc) override;

    private:
        float get_Euclidean_DistanceAB(float a_x, float a_y, float b_x, float b_y)
        {
            float dist = std::pow(a_x - b_x, 2) + pow(a_y - b_y, 2);
            return std::sqrt(dist);
        }

        bool isThumbNearFirstFinger(NormalizedLandmark point1, NormalizedLandmark point2)
        {
            float distance = this->get_Euclidean_DistanceAB(point1.x(), point1.y(), point2.x(), point2.y());
            return distance < 0.1;
        }
    };

    REGISTER_CALCULATOR(HandGestureRecognitionCalculator);

    ::mediapipe::Status HandGestureRecognitionCalculator::GetContract(
        CalculatorContract *cc)
    {
        RET_CHECK(cc->Inputs().HasTag(normalizedLandmarkListTag));
        cc->Inputs().Tag(normalizedLandmarkListTag).Set<mediapipe::NormalizedLandmarkList>();

        RET_CHECK(cc->Inputs().HasTag(normRectTag));
        cc->Inputs().Tag(normRectTag).Set<NormalizedRect>();

        return ::mediapipe::OkStatus();
    }

    ::mediapipe::Status HandGestureRecognitionCalculator::Open(
        CalculatorContext *cc)
    {
        cc->SetOffset(TimestampDiff(0));
        return ::mediapipe::OkStatus();
    }
    ////------------Modification BB------------------

    ///This function continues sending over tcp connection until all data is sent. it then sends the terminating character ';'
    bool send_all(int socket, const char *buffer, size_t length)
    {

        char *ptr = (char *)buffer;
        while (length > 0)
        {
            //keep sending until all data is sent
            int i = send(socket, ptr, length, 0);
            if (i < 1)
                return false;
            ptr += i;
            length -= i;
        }

        //send terminate char ';' so receiver can be sure they received all the data
        char *terminate = ";";
        send(socket, terminate, sizeof(terminate), 0);
        return true;
    }

    // get sockaddr, IPv4 or IPv6:
    void *get_in_addr(struct sockaddr *sa)
    {
        if (sa->sa_family == AF_INET)
        {
            return &(((struct sockaddr_in *)sa)->sin_addr);
        }

        return &(((struct sockaddr_in6 *)sa)->sin6_addr);
    }

    addrinfo *savedInfo = nullptr;

    //this function will open a TCP socket and send the output argument
    int sendData(std::string output)
    {
        int sockfd, numbytes;

        //if this is the first time, we must setup TCP socket addrinfo
        if (savedInfo == nullptr)
        {
            struct addrinfo hints, *servinfo, *p;
            int rv;
            char s[INET6_ADDRSTRLEN];

            memset(&hints, 0, sizeof hints);
            hints.ai_family = AF_UNSPEC;
            hints.ai_socktype = SOCK_STREAM;

            if ((rv = getaddrinfo("localhost", PORT, &hints, &servinfo)) != 0)
            {
                fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rv));
                return 1;
            }

            // loop through all the results and connect to the first we can
            for (p = servinfo; p != NULL; p = p->ai_next)
            {
                if ((sockfd = socket(p->ai_family, p->ai_socktype,
                                     p->ai_protocol)) == -1)
                {
                    perror("client: socket");
                    continue;
                }

                if (connect(sockfd, p->ai_addr, p->ai_addrlen) == -1)
                {
                    close(sockfd);
                    perror("client: connect");
                    continue;
                }

                break;
            }

            if (p == NULL)
            {
                fprintf(stderr, "client: failed to connect\n");
                return 2;
            }

            inet_ntop(p->ai_family, get_in_addr((struct sockaddr *)p->ai_addr),
                      s, sizeof s);

            savedInfo = p;
        }
        else
        { //otherwise we have already setup addrinfo and we can just connect
            if ((sockfd = socket(savedInfo->ai_family, savedInfo->ai_socktype,
                                 savedInfo->ai_protocol)) == -1)
            {
                perror("client: socket");
                return 0;
            }

            if (connect(sockfd, savedInfo->ai_addr, savedInfo->ai_addrlen) == -1)
            {
                close(sockfd);
                perror("client: connect");
                return 0;
            }
        }

        //use send all function to actually send data over socket
        send_all(sockfd, output.c_str(), output.length());

        close(sockfd);

        return 0;
    }

    //------------Modification END BB------------------

    ::mediapipe::Status HandGestureRecognitionCalculator::Process(
        CalculatorContext *cc)
    {
        // hand closed (red) rectangle
        const auto rect = &(cc->Inputs().Tag(normRectTag).Get<NormalizedRect>());
        float width = rect->width();
        float height = rect->height();

        if (width < 0.01 || height < 0.01)
        {
            LOG(INFO) << "No Hand Detected";
            return ::mediapipe::OkStatus();
        }

        const auto &landmarkList = cc->Inputs()
                                       .Tag(normalizedLandmarkListTag)
                                       .Get<mediapipe::NormalizedLandmarkList>();
        RET_CHECK_GT(landmarkList.landmark_size(), 0) << "Input landmark vector is empty.";

        // finger states
        bool thumbIsOpen = false;
        bool firstFingerIsOpen = false;
        bool secondFingerIsOpen = false;
        bool thirdFingerIsOpen = false;
        bool fourthFingerIsOpen = false;
        //

        float pseudoFixKeyPoint = landmarkList.landmark(2).x();
        if (landmarkList.landmark(3).x() < pseudoFixKeyPoint && landmarkList.landmark(4).x() < pseudoFixKeyPoint)
        {
            thumbIsOpen = true;
        }

        pseudoFixKeyPoint = landmarkList.landmark(6).y();
        if (landmarkList.landmark(7).y() < pseudoFixKeyPoint && landmarkList.landmark(8).y() < pseudoFixKeyPoint)
        {
            firstFingerIsOpen = true;
        }

        pseudoFixKeyPoint = landmarkList.landmark(10).y();
        if (landmarkList.landmark(11).y() < pseudoFixKeyPoint && landmarkList.landmark(12).y() < pseudoFixKeyPoint)
        {
            secondFingerIsOpen = true;
        }

        pseudoFixKeyPoint = landmarkList.landmark(14).y();
        if (landmarkList.landmark(15).y() < pseudoFixKeyPoint && landmarkList.landmark(16).y() < pseudoFixKeyPoint)
        {
            thirdFingerIsOpen = true;
        }

        pseudoFixKeyPoint = landmarkList.landmark(18).y();
        if (landmarkList.landmark(19).y() < pseudoFixKeyPoint && landmarkList.landmark(20).y() < pseudoFixKeyPoint)
        {
            fourthFingerIsOpen = true;
        }

        // Hand gesture recognition
        if (thumbIsOpen && firstFingerIsOpen && secondFingerIsOpen && thirdFingerIsOpen && fourthFingerIsOpen)
        {
            LOG(INFO) << "FIVE";
        }
        else if (!thumbIsOpen && firstFingerIsOpen && secondFingerIsOpen && thirdFingerIsOpen && fourthFingerIsOpen)
        {
            LOG(INFO) << "FOUR";
        }
        else if (!thumbIsOpen && firstFingerIsOpen && secondFingerIsOpen && thirdFingerIsOpen && !fourthFingerIsOpen)
        {
            LOG(INFO) << "THREE";
        }
        else if (!thumbIsOpen && firstFingerIsOpen && !secondFingerIsOpen && !thirdFingerIsOpen && !fourthFingerIsOpen)
        {
            LOG(INFO) << "ONE";
        }
        else if (!thumbIsOpen && firstFingerIsOpen && secondFingerIsOpen && !thirdFingerIsOpen && !fourthFingerIsOpen)
        {
            LOG(INFO) << "TWO";
        }
        else if (!thumbIsOpen && !firstFingerIsOpen && !secondFingerIsOpen && !thirdFingerIsOpen && !fourthFingerIsOpen)
        {
            LOG(INFO) << "FIST";
        }
        else if (!firstFingerIsOpen && secondFingerIsOpen && thirdFingerIsOpen && fourthFingerIsOpen && this->isThumbNearFirstFinger(landmarkList.landmark(4), landmarkList.landmark(8)))
        {
            LOG(INFO) << "OK";
        }
        else
        {
            LOG(INFO) << "Finger States: " << thumbIsOpen << firstFingerIsOpen << secondFingerIsOpen << thirdFingerIsOpen << fourthFingerIsOpen;
            LOG(INFO) << "___";
        }

        //------------Modification BB------------------
        //OUTPUT OVER TCP

        //loop through each landmark and create a CSV string
        std::string landmarkString = "";
        for (int i = 0; i < landmarkList.landmark_size(); ++i)
        {
            const NormalizedLandmark &landmark = landmarkList.landmark(i);
            landmarkString = landmarkString + (i == 0 ? "" : ",") + std::to_string(static_cast<float>(landmark.x())) + "," + std::to_string(static_cast<float>(landmark.y())) + "," + std::to_string(static_cast<float>(landmark.z()));
        }

        //send to python process over TCP
        sendData(landmarkString);

        //------------Modification END BB------------------

        return ::mediapipe::OkStatus();
    } // namespace mediapipe

} // namespace mediapipe