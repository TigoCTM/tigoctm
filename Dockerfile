FROM node:5.11.1

MAINTAINER MobyDevTeam

RUN apt-get update -qq
RUN apt-get install -y -qq \
    python-pygments \
    curl \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Hugo
ENV HUGO_VERSION 0.15
ENV HUGO_SOURCE hugo_${HUGO_VERSION}_linux_amd64
RUN curl -sL https://github.com/spf13/hugo/releases/download/v${HUGO_VERSION}/${HUGO_SOURCE}.tar.gz \
    > /usr/local/${HUGO_SOURCE}.tar.gz \
    && tar xzf /usr/local/${HUGO_SOURCE}.tar.gz -C /usr/local/ \
    && ln -s /usr/local/${HUGO_SOURCE}/${HUGO_SOURCE} /usr/local/bin/hugo \
    && rm /usr/local/${HUGO_SOURCE}.tar.gz

# ESLint And Gulp
RUN npm install -g --silent eslint gulp-cli webpack

ADD ./package.json /usr/src/app/
