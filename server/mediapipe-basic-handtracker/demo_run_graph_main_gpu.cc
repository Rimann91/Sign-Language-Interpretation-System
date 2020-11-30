// Copyright 2019 The MediaPipe Authors.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
// An example of sending OpenCV webcam frames into a MediaPipe graph.
// This example requires a linux computer and a GPU with EGL support drivers.

////Mdified by Braden Bagby
////Modifications marked starting with ------------Modification BB------------------
///and ending with ------------Modification END BB------------------

#include <cstdlib>

#include "mediapipe/framework/calculator_framework.h"
#include "mediapipe/framework/formats/image_frame.h"
#include "mediapipe/framework/formats/image_frame_opencv.h"
#include "mediapipe/framework/port/commandlineflags.h"
#include "mediapipe/framework/port/file_helpers.h"
#include "mediapipe/framework/port/opencv_highgui_inc.h"
#include "mediapipe/framework/port/opencv_imgproc_inc.h"
#include "mediapipe/framework/port/opencv_video_inc.h"
#include "mediapipe/framework/port/parse_text_proto.h"
#include "mediapipe/framework/port/status.h"
#include "mediapipe/gpu/gl_calculator_helper.h"
#include "mediapipe/gpu/gpu_buffer.h"
#include "mediapipe/gpu/gpu_shared_data_internal.h"

//////------------Modification BB------------------
///Libraries for TCP Image Buffer
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <sys/wait.h>
#include <signal.h>
#include <iostream>
#include <thread>
#include <unistd.h>
#include <mutex>

//vars for TCP Image Buffer
#define PORT "4433"
unsigned char *imageBuffer = nullptr; //buffer to hold most current image
ssize_t imageSize = 0;
std::mutex imageBufferMutex; //mutex to block while writing and reading imageBuffer
bool ready = false;          //helper bool so mediapipe can wait until we have at least received one full image
 char *tempImageBuffer = new char[100000]();; //temp buffer that is large enough to store an entire image. used to not block mutex for each recv(). When done receiving, we copy data in here to real image buffer. 100000 should be good enought to hold all of the data
  
//functions for TCP Image Buffer
void *get_in_addr(struct sockaddr *sa);
static void print_buf(const char *title, const unsigned char *buf, size_t buf_len);
int imageBufferThread();

//////--------------------------------------------------------
///image buffer functions
int imageBufferThread()
{

    int socket_fd, connection_fd;
    struct addrinfo hints, *servinfo, *p;
    struct sockaddr_storage their_addr; // connector's address information
    socklen_t sin_size;
    int yes = 1;
    char s[INET6_ADDRSTRLEN];

    int rv;

    memset(&hints, 0, sizeof hints);
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_flags = AI_PASSIVE; // use my IP

    if ((rv = getaddrinfo(NULL, PORT, &hints, &servinfo)) != 0)
    {
        fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rv));
        return 1;
    }

    // loop through all the results and bind to the first we can
    for (p = servinfo; p != NULL; p = p->ai_next)
    {
        if ((socket_fd = socket(p->ai_family, p->ai_socktype,
                                p->ai_protocol)) == -1)
        {
            perror("server: socket");
            continue;
        }

        if (setsockopt(socket_fd, SOL_SOCKET, SO_REUSEADDR, &yes,
                       sizeof(int)) == -1)
        {
            perror("setsockopt");
            exit(1);
        }

        if (bind(socket_fd, p->ai_addr, p->ai_addrlen) == -1)
        {
            close(socket_fd);
            perror("server: bind");
            continue;
        }

        break;
    }

    freeaddrinfo(servinfo); // all done with this structure

    if (p == NULL)
    {
        fprintf(stderr, "server: failed to bind\n");
        exit(1);
    }

    if (listen(socket_fd, 1) == -1)
    {
        perror("listen");
        exit(1);
    }

    printf("Waiting for image buffer connection\n");

    while (true)
    {
        sin_size = sizeof their_addr;
        connection_fd = accept(socket_fd, (struct sockaddr *)&their_addr, &sin_size);
        if (socket_fd == -1)
        {
            perror("accept");
            continue;
        }
        inet_ntop(their_addr.ss_family,
                  get_in_addr((struct sockaddr *)&their_addr),
                  s, sizeof s);
        printf("server: got connection from %s\n", s);

        ////This while loop opens from connection, closes imageBufferMutex, fills imageBuffer, opensImageBufferMutex

        ssize_t len = 0;
        char buffer[1024]; //temp buffer for holding image data
        ssize_t totalLen = 0;
       
        while ((len = recv(connection_fd, buffer, 1024, 0)) > 0)
        {
            totalLen += len;

          
            memcpy(tempImageBuffer + totalLen - len, buffer, len); //update full buffer
            memset(buffer, 0, 1024);                               //clear buffer every time just to be safe its really not needed
        }

     

            ///MUTEX CLOSE
            imageBufferMutex.lock();

            //create and save to imageBuffer to be used by mediapipe
            imageSize = totalLen;
            imageBuffer = new unsigned char[imageSize]();
            memcpy(imageBuffer, tempImageBuffer, imageSize);

            /// MUTEX OPEN
            imageBufferMutex.unlock();
            ready = true;
        

        close(connection_fd);
    }

    return 0;
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

//helper function for printing imageBuffer as hex
static void print_buf(const char *title, const unsigned char *buf, size_t buf_len)
{
    size_t i = 0;
    fprintf(stdout, "%s\n", title);
    for (i = 0; i < buf_len; ++i)
        fprintf(stdout, "%02X%s", buf[i],
                (i + 1) % 16 == 0 ? "\r\n" : " ");
}
/////---------------------------------------------------------
////------------Modification END BB------------------

constexpr char kInputStream[] = "input_video";
constexpr char kOutputStream[] = "output_video";
constexpr char kWindowName[] = "MediaPipe";

DEFINE_string(
    calculator_graph_config_file, "",
    "Name of file containing text format CalculatorGraphConfig proto.");
DEFINE_string(input_video_path, "",
              "Full path of video to load. "
              "If not provided, attempt to use a webcam.");
DEFINE_string(output_video_path, "",
              "Full path of where to save result (.mp4 only). "
              "If not provided, show result in a window.");

::mediapipe::Status RunMPPGraph()
{
    std::string calculator_graph_config_contents;
    MP_RETURN_IF_ERROR(mediapipe::file::GetContents(
        FLAGS_calculator_graph_config_file, &calculator_graph_config_contents));
    LOG(INFO) << "Get calculator graph config contents: "
              << calculator_graph_config_contents;
    mediapipe::CalculatorGraphConfig config =
        mediapipe::ParseTextProtoOrDie<mediapipe::CalculatorGraphConfig>(
            calculator_graph_config_contents);

    LOG(INFO) << "Initialize the calculator graph.";
    mediapipe::CalculatorGraph graph;
    MP_RETURN_IF_ERROR(graph.Initialize(config));

    LOG(INFO) << "Initialize the GPU.";
    ASSIGN_OR_RETURN(auto gpu_resources, mediapipe::GpuResources::Create());
    MP_RETURN_IF_ERROR(graph.SetGpuResources(std::move(gpu_resources)));
    mediapipe::GlCalculatorHelper gpu_helper;
    gpu_helper.InitializeForTest(graph.GetGpuResources().get());

    LOG(INFO) << "Initialize the camera or load the video.";
    // cv::VideoCapture capture;
    /*const bool load_video = true;!FLAGS_input_video_path.empty();
  if (load_video) {
    capture.open(FLAGS_input_video_path);
  } else {
    capture.open(0);
  }
  RET_CHECK(capture.isOpened());
  cv::VideoWriter writer;
  const bool save_video = !FLAGS_output_video_path.empty();
  if (!save_video) {
    cv::namedWindow(kWindowName, /*flags=WINDOW_AUTOSIZE*/
    /* 1);
#if (CV_MAJOR_VERSION >= 3) && (CV_MINOR_VERSION >= 2)
    capture.set(cv::CAP_PROP_FRAME_WIDTH, 640);
    capture.set(cv::CAP_PROP_FRAME_HEIGHT, 480);
    capture.set(cv::CAP_PROP_FPS, 30);
#endif
  }*/

    LOG(INFO) << "Start running the calculator graph.";
    ASSIGN_OR_RETURN(mediapipe::OutputStreamPoller poller,
                     graph.AddOutputStreamPoller(kOutputStream));
    MP_RETURN_IF_ERROR(graph.StartRun({}));

    LOG(INFO) << "Start grabbing and processing frames.";
    bool grab_frames = true;
    while (grab_frames)
    {

        ////------------Modification BB------------------
        // Capture opencv camera or video frame.

        while (ready == false)
        {
            std::cout << "no starter image yet. sleep 5 seconds" << std::endl;
            sleep(5);
        }

        // MUTEX CLOSE
        imageBufferMutex.lock();

        //deep copy image data so we can conintue to update it in thread

        char *imageCopy = new char[imageSize]();
        memcpy(imageCopy, imageBuffer, imageSize);
        //MUTEX OPEN
        imageBufferMutex.unlock();

        std::vector<char> data(imageCopy, imageCopy + imageSize);
        cv::Mat camera_frame_raw = cv::imdecode(data, 1); //(480,640,CV_8UC1,imageCopy); //cv::imdecode(imageData);
        //capture >> camera_frame_raw;

        if (camera_frame_raw.empty())
            break; // End of video.
        cv::Mat camera_frame;
        cv::cvtColor(camera_frame_raw, camera_frame, cv::COLOR_BGR2RGB);
        //if (!load_video) {
        //  cv::flip(camera_frame, camera_frame, /*flipcode=HORIZONTAL*/ 1);
        // }

        ////------------Modification END BB------------------

        // Wrap Mat into an ImageFrame.
        auto input_frame = absl::make_unique<mediapipe::ImageFrame>(
            mediapipe::ImageFormat::SRGB, camera_frame.cols, camera_frame.rows,
            mediapipe::ImageFrame::kGlDefaultAlignmentBoundary);
        cv::Mat input_frame_mat = mediapipe::formats::MatView(input_frame.get());
        camera_frame.copyTo(input_frame_mat);

        // Prepare and add graph input packet.
        size_t frame_timestamp_us =
            (double)cv::getTickCount() / (double)cv::getTickFrequency() * 1e6;
        MP_RETURN_IF_ERROR(
            gpu_helper.RunInGlContext([&input_frame, &frame_timestamp_us, &graph,
                                       &gpu_helper]() -> ::mediapipe::Status {
                // Convert ImageFrame to GpuBuffer.
                auto texture = gpu_helper.CreateSourceTexture(*input_frame.get());
                auto gpu_frame = texture.GetFrame<mediapipe::GpuBuffer>();
                glFlush();
                texture.Release();
                // Send GPU image packet into the graph.
                MP_RETURN_IF_ERROR(graph.AddPacketToInputStream(
                    kInputStream, mediapipe::Adopt(gpu_frame.release())
                                      .At(mediapipe::Timestamp(frame_timestamp_us))));
                return ::mediapipe::OkStatus();
            }));

        // Get the graph result packet, or stop if that fails.
        mediapipe::Packet packet;
        if (!poller.Next(&packet))
            break;
        std::unique_ptr<mediapipe::ImageFrame> output_frame;

        // Convert GpuBuffer to ImageFrame.
        MP_RETURN_IF_ERROR(gpu_helper.RunInGlContext(
            [&packet, &output_frame, &gpu_helper]() -> ::mediapipe::Status {
                auto &gpu_frame = packet.Get<mediapipe::GpuBuffer>();
                auto texture = gpu_helper.CreateSourceTexture(gpu_frame);
                output_frame = absl::make_unique<mediapipe::ImageFrame>(
                    mediapipe::ImageFormatForGpuBufferFormat(gpu_frame.format()),
                    gpu_frame.width(), gpu_frame.height(),
                    mediapipe::ImageFrame::kGlDefaultAlignmentBoundary);
                gpu_helper.BindFramebuffer(texture);
                const auto info =
                    mediapipe::GlTextureInfoForGpuBufferFormat(gpu_frame.format(), 0);
                glReadPixels(0, 0, texture.width(), texture.height(), info.gl_format,
                             info.gl_type, output_frame->MutablePixelData());
                glFlush();
                texture.Release();
                return ::mediapipe::OkStatus();
            }));

        // Convert back to opencv for display or saving.
        cv::Mat output_frame_mat = mediapipe::formats::MatView(output_frame.get());
        cv::cvtColor(output_frame_mat, output_frame_mat, cv::COLOR_RGB2BGR);
        if (/*save_video*/ false)
        {
            /*  if (!writer.isOpened()) {
        LOG(INFO) << "Prepare video writer.";
        writer.open(FLAGS_output_video_path,
                    mediapipe::fourcc('a', 'v', 'c', '1'),  // .mp4
                    capture.get(cv::CAP_PROP_FPS), output_frame_mat.size());
        RET_CHECK(writer.isOpened());
      }
      writer.write(output_frame_mat);*/
        }
        else
        {
            cv::imshow(kWindowName, output_frame_mat);
            // Press any key to exit.
            const int pressed_key = cv::waitKey(5);
            if (pressed_key >= 0 && pressed_key != 255)
                grab_frames = false;
        }
    }

    LOG(INFO) << "Shutting down.";
    //  if (writer.isOpened()) writer.release();
    MP_RETURN_IF_ERROR(graph.CloseInputStream(kInputStream));
    return graph.WaitUntilDone();
}

int main(int argc, char **argv)
{
    google::InitGoogleLogging(argv[0]);
    gflags::ParseCommandLineFlags(&argc, &argv, true);

    std::thread imgBufferThread(imageBufferThread);

    ::mediapipe::Status run_status = RunMPPGraph();
    if (!run_status.ok())
    {
        LOG(ERROR) << "Failed to run the graph: " << run_status.message();
        return EXIT_FAILURE;
    }
    else
    {
        LOG(INFO) << "Success!";
    }
    imgBufferThread.join();
    return EXIT_SUCCESS;
}