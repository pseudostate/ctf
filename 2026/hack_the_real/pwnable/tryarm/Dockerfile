FROM ubuntu:22.04@sha256:b6b83d3c331794420340093eb706a6f152d9c1fa51b262d9bf34594887c2c7ac

RUN apt-get update && apt-get install -y socat adduser qemu-user-static

RUN adduser tryarm

WORKDIR /home/tryarm

COPY ./flag ./flag
COPY ./deploy/prob ./prob
COPY ./deploy/run.sh ./run.sh

USER root

RUN mkdir -p /lib/aarch64-linux-gnu
COPY ./deploy/ld-linux-aarch64.so.1 /lib/ld-linux-aarch64.so.1
COPY ./deploy/libc.so.6 /lib/aarch64-linux-gnu/libc.so.6
RUN chmod 444 ./flag 
RUN chmod 755 ./prob
RUN chmod 755 ./run.sh

USER tryarm

EXPOSE 9090
CMD ["socat","-d","-d","TCP-LISTEN:9090,reuseaddr,fork","EXEC:./run.sh,pty,stderr,setsid,ctty"]
