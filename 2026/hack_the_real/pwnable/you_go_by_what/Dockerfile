FROM ubuntu:22.04@sha256:b6b83d3c331794420340093eb706a6f152d9c1fa51b262d9bf34594887c2c7ac

RUN apt update && apt-get install -y socat
RUN adduser --disabled-login --gecos '' -- "you_go_by"

WORKDIR /home/you_go_by
USER you_go_by

COPY ./deploy/prob ./prob
COPY ./deploy/log ./log
COPY ./flag ./flag

USER root
RUN chmod 444 ./flag
RUN chmod 755 ./prob
RUN chmod 755 ./log

USER you_go_by

EXPOSE 9090
CMD ["socat","TCP-LISTEN:9090,reuseaddr,fork","EXEC:./prob,pty,raw,echo=0,setsid,ctty,stderr"]