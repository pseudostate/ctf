# docker build -t bpf_prob . && docker run -d --name bpf_prob --cap-add NET_ADMIN --cap-add NET_RAW -p 8888:80 bpf_prob

FROM ubuntu:22.04@sha256:b6b83d3c331794420340093eb706a6f152d9c1fa51b262d9bf34594887c2c7ac

ENV DEBIAN_FRONTEND=noninteractive

USER root
WORKDIR /home/SIMPLE_BPF

COPY ./depoly/prob ./prob
COPY ./flag ./flag

RUN chmod 444 ./flag
RUN chmod 755 ./prob

# 기본 포트
EXPOSE 80

CMD ["./prob"]