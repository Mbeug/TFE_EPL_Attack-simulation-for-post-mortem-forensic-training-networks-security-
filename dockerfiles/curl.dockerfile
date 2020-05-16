FROM alpine
RUN apk add curl wget
CMD [ "sh", "-c", "exec ash -i" ]