FROM osrf/ros:humble-desktop-full

ENV DEBIAN_FRONTEND=noninteractive

ENV NVIDIA_DRIVER_CAPABILITIES=all
ENV QT_X11_NO_MITSHM=1

RUN apt-get update && apt-get install -y \
    ros-humble-controller-interface \
    ros-humble-realtime-tools \
    libglfw3-dev \
    ros-humble-ros2-control \
    ros-humble-ros2-controllers \
    ros-humble-controller-manager \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ROS2

CMD ["bash"]