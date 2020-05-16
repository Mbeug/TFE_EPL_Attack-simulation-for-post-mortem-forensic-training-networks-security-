FROM gns3/ubuntu:xenial
RUN apt-get update && apt-get install apache2 php libapache2-mod-php php-mysql -y
CMD [ "sh", "-c", "/etc/init.d/apache2 start; exec bash -i" ]