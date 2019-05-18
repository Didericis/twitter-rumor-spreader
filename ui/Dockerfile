FROM node:10

RUN curl -o- -L https://yarnpkg.com/install.sh | bash

RUN mkdir -p /code

COPY package.json yarn.lock /tmp/
RUN cd /tmp && yarn
RUN cd /code && ln -s /tmp/node_modules

WORKDIR /code

COPY . .

EXPOSE 3000

ARG REACT_APP_API_PORT

RUN yarn build
RUN yarn global add serve
