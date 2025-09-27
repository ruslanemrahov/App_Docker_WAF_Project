FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Baku

RUN apt update && \ 
    apt full-upgrade -y && \
    apt install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install flask                    

COPY . /app/

EXPOSE 5000

CMD ["python3", "app.py"]
