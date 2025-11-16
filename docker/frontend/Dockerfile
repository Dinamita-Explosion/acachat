FROM node:20-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

RUN npm run build:docker

FROM nginx:1.27-alpine

COPY docker/nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/www /usr/share/nginx/html

EXPOSE 80
