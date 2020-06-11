FROM alpine
RUN apk add nmap nano
CMD [ "sh", "-c", "exec ash -i" ]