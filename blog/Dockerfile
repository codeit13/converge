# app/blog/Dockerfile
FROM node:20-alpine as builder
WORKDIR /app
# Install Hugo globally via Yarn
RUN yarn global add hugo
COPY . .
# Build the Hugo site; by default Hugo outputs to the "public" folder.
RUN hugo

FROM nginx:alpine
COPY --from=builder /app/public /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
