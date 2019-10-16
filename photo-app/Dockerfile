FROM node:alpine as builder
WORKDIR '/app'
COPY package*.json yarn* ./
RUN yarn
COPY . .
RUN npm run build

FROM nginx
EXPOSE 3000
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist/photo-app /usr/share/nginx/html
