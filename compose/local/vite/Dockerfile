FROM node:20.15-bullseye-slim

WORKDIR /app/vue_frontend

COPY ./vue_frontend/package.json /app/vue_frontend

COPY ./compose/local/vite/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint

RUN npm install && npm cache clean --force

ENV PATH ./node_modules/.bin/:$PATH

RUN echo $PATH

#CMD ["vite", "dev"]
ENTRYPOINT ["/entrypoint"]
