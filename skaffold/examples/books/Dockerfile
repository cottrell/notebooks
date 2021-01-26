FROM alpine:latest
WORKDIR /app

RUN apk add --no-cache python3 && \
python3 -m ensurepip && \
rm -r /usr/lib/python*/ensurepip && \
pip3 install --upgrade pip setuptools

RUN if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
rm -r /root/.cache

COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod 755 /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

