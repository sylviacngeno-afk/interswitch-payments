# Stage 1: build
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm prune --omit=dev

# Stage 2: runtime
FROM node:20-alpine AS runtime
WORKDIR /app
ENV NODE_ENV=production PORT=3000

# Run as non-root user (Alpine syntax)
RUN addgroup -S portal && adduser -S -G portal portal

# Copy built application artifacts
COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/package.json ./package.json
COPY --from=build /app/server.js ./server.js
COPY --from=build /app/web ./web

USER portal
EXPOSE 3000

ENTRYPOINT ["node"]
CMD ["server.js"]
