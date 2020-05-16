FROM ubuntu
RUN apt-get update
RUN apt-get install -y git 
RUN apt-get install -y gcc make ruby-dev
RUN git clone https://github.com/iagox86/dnscat2.git 
RUN cd dnscat2/client/ && make
RUN cd /dnscat2/server/ && gem install bundler && bundle install
CMD [ "sh", "-c", "exec bash -i" ]