FROM node:22-alpine

WORKDIR /code

COPY package*.json ./

RUN npm ci

COPY . .

EXPOSE 3000