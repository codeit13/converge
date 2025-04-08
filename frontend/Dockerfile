# Stage 1: Build stage
FROM node:20-alpine AS builder
WORKDIR /src
COPY . .
RUN npm install
RUN npm run build

# Stage 2: Final stage - Copy build output to /build_dist
FROM node:20-alpine
WORKDIR /build_dist
COPY --from=builder /src/dist .
