FROM node:19-alpine

COPY src /app
WORKDIR /app
RUN yarn

RUN apk update && \
    apk add --no-cache openssl && \
    openssl req -x509 -nodes -days 365 \
    -subj  "/C=CA/ST=QC/O=Company Inc/CN=example.com" \
    -newkey rsa:2048 -keyout /opt/selfsigned.key \
    -out /opt/selfsigned.crt;

ENTRYPOINT ["yarn", "start"]
