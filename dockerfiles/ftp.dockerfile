FROM gns3/ubuntu:xenial
RUN apt-get update && apt-get install vsftpd -y
CMD [ "sh", "-c", "/etc/init.d/vsftpd start; exec bash -i" ]