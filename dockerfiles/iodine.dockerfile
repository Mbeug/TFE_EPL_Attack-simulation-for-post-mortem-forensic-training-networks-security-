FROM ubuntu
RUN apt update
RUN apt install -y iodine iputils-ping
CMD [ "sh", "-c", "exec bash -i" ]