FROM gliderlabs/alpine:3.1

WORKDIR /app
COPY . /app
ENV OPENSHIFT_REPO_DIR '/app'
ENV OPENSHIFT_PYTHON_DIR '/env'
EXPOSE 8080
RUN echo "### Installing Base Dependencies via apk..." && \
    apk --update add --virtual build-dependencies \
    python-dev \
    py-pip \
    build-base \
    curl \
    && echo "### Installing virtualenv via pip..." \
    && pip install virtualenv \
    && echo "### Creating a new virtualenv to /env..." \
    && virtualenv /env \
    && echo "### Downloading Hurtle CC SDK (hurtle_cc_sdk.tgz) via curl..." \
    && curl -s -k -o /tmp/sdk.tar.gz 'https://dl.dropboxusercontent.com/u/165239/mcn_cc_sdk.tgz' \
    && echo "### Installing Hurtle CC SDK (hurtle_cc_sdk.tgz) via pip..." \
    && /env/bin/pip install /tmp/sdk.tar.gz \
    #&& echo "### Downloading&Installing SM Library (sm-0.4-master.zip) via pip..." \
    #&& /env/bin/pip install 'https://github.com/AleDanish/sm-0.4/archive/master.zip' \
    && echo "### Downloading SM Library (sm-0.4.tgz) via curl..." \
    && curl -s -k -o /tmp/sm.tar.gz 'https://dl.dropboxusercontent.com/u/165239/sm-0.4.tgz' \
    && echo "### Installing SM Library (sm-0.4.tgz) via pip..." \
    && /env/bin/pip install /tmp/sm.tar.gz \
    && echo "### Installing SO Dependencies (requirements.txt) via pip..." \
    && /env/bin/pip install -r /app/requirements.txt \
    && echo "### Cleanup..." \
    && apk del build-dependencies \
    && apk add python \
    && rm -rf /var/cache/apk/* /root/.cache/* /tmp/*
CMD ["/env/bin/python", "./wsgi/application"]
