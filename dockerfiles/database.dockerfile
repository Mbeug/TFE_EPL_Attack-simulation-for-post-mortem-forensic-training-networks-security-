FROM gns3/ubuntu:xenial
RUN apt-get update
RUN apt-get install -y nano
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install mysql-server
RUN echo '[mysqld]' >> /etc/mysql/my.cnf
RUN echo 'bind-address = 0.0.0.0' >> /etc/mysql/my.cnf
CMD [ "sh", "-c", "/etc/init.d/mysql start; exec bash -i" ]