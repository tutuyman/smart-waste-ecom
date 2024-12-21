# Stage 1: Build Vue.js frontend
FROM node:18 AS frontend-build
WORKDIR /app
# Copy frontend code
COPY . ./
RUN npm install && npm run build

# Stage 2: Serve Vue.js frontend using 'serve'
FROM node:18 AS production
WORKDIR /app

# Install 'serve'
RUN npm install -g serve

# Copy Vue.js build output
COPY --from=frontend-build /app/dist /app

# Expose port 8080 for serving the frontend
EXPOSE 8080

# Start 'serve'
CMD ["serve", "-s", "/app", "-l", "8080"]
