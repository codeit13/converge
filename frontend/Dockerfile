FROM node:20-alpine as builder

WORKDIR /src
COPY . .
RUN npm install
RUN npm run build

# Final stage: copy built files
FROM node:20-alpine
WORKDIR /dist
COPY --from=builder /src/dist .
