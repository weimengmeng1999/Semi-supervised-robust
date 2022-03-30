FROM nvcr.io/nvidia/pytorch:21.10-py3

ARG USER_ID
ARG GROUP_ID
ARG USER
ARG DEBIAN_FRONTEND=noninteractive

RUN addgroup --gid $GROUP_ID $USER
RUN adduser --disabled-password --gecos "" --uid $USER_ID --gid $GROUP_ID $USER

WORKDIR /nfs/home/$USER/Semi-supervised-robust
EXPOSE 8888

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y

# RUN apt-get install cifs-utils
# RUN mount -t cifs -o user=mwei,password=WMwm199910156@ //10.246.201.201/laparoscopy/robustmis /nfs/home/$USER/robustmis
