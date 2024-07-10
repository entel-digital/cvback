FROM docker.io/node:20-bookworm-slim

WORKDIR /app

COPY ./vue_frontend/package.json /app

RUN npm install && npm install -g @quasar/cli
ENV PATH ./node_modules/.bin/:$PATH
