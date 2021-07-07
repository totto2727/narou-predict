FROM python:3.9.6-buster

ARG INSTALL_ZSH="true"
ARG UPGRADE_PACKAGES="true"

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

#setup script
COPY ./scripts/*.sh /tmp/scripts/
RUN apt-get update \
    && export DEBIAN_FRONTEND=noninteractive \
    && /bin/bash /tmp/scripts/setup.sh \ 
    "${INSTALL_ZSH}" "${USERNAME}" "${USER_UID}" "${USER_GID}" "${UPGRADE_PACKAGES}"

#custom
#apt install
RUN apt-get install -y  --no-install-recommends \
    mecab \
    libmecab-dev \
    libmecab2 \
    mecab-ipadic \
    mecab-ipadic-utf8 

#apt optimize
RUN apt-get autoremove -y  \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/* /tmp/library-scripts \
    && rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/* 

#individual
RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git /ipadic-neologd \
    && /ipadic-neologd/bin/install-mecab-ipadic-neologd -n -a -y \
    && rm -r -f /ipadic-neologd

RUN pip install --no-cache-dir \ 
    mecab-python3 \
    requests

RUN ln -s /etc/mecabrc /usr/local/etc/mecabrc