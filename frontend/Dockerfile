# Stage 1: Build stage
FROM node:20-alpine AS builder
WORKDIR /src
COPY . .
RUN npm install
RUN npm run build

# Stage 2: Final stage - Copy build output to /built_dist
FROM node:20-alpine
WORKDIR /built_dist
COPY --from=builder /src/dist .
