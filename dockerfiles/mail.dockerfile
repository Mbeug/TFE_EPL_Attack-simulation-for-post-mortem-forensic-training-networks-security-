FROM debian
RUN echo "postfix postfix/mailname string mail.local" | debconf-set-selections
RUN echo "postfix postfix/main_mailer_type string 'Internet Site'" | debconf-set-selections
RUN apt-get update && apt-get install --assume-yes postfix && apt -y install dovecot-core dovecot-imapd nano rsyslog
RUN echo 'listen = *, ::' >> /etc/dovecot/dovecot.conf 
RUN useradd -p $(openssl passwd -1 alice) --create-home -s /sbin/nologin bob
RUN useradd -p $(openssl passwd -1 alice) --create-home -s /sbin/nologin max

CMD [ "sh", "-c", "hostname -b mail.local; /etc/init.d/rsyslog start; /etc/init.d/postfix start; /etc/init.d/dovecot start; exec bash -i" ]