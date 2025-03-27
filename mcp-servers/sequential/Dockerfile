# Builder Stage: Install dependencies and compile TypeScript
FROM node:22.12-alpine AS builder
WORKDIR /app

# Copy only necessary files for building
COPY package.json yarn.lock tsconfig.json ./
COPY index.ts ./
# If you have additional source files or directories, copy them here:
# COPY src/ ./src/

# Install dependencies and build the project
RUN yarn install
RUN yarn run build

# Release Stage: Use the built files and install only production dependencies
FROM node:22-alpine AS release
WORKDIR /app

# Copy only the built output and essential package files
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/yarn.lock ./yarn.lock

ENV NODE_ENV=production

# Install production dependencies without running lifecycle scripts
RUN yarn install --production --ignore-scripts

# Set the entry point to run your compiled application
ENTRYPOINT ["node", "dist/index.js"]
