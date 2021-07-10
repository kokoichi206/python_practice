FROM python:3.6-slim-buster as runner

WORKDIR /root/opt

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean
RUN python -m pip install keras==2.3.1 && \
    python -m pip install tensorflow==2.0.0 && \
    python -m pip install flask==1.1.2 && \
    python -m pip install werkzeug==1.0.1 && \
    python -m pip install gunicorn==20.0.4 && \
    python -m pip install jinja2==2.11.1
RUN python -m pip install h5py==2.10.0
RUN python -m pip install numpy
RUN python -m pip install pillow==7.0.0

EXPOSE 8080
