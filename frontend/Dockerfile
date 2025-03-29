# app/frontend/Dockerfile
FROM node:20-alpine as build
WORKDIR /app
COPY . .
RUN yarn install --frozen-lockfile && yarn run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
