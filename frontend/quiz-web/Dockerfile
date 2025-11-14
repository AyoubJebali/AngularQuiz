# Stage 1: Build the Angular application
FROM node:20-alpine AS build

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
# Note: If you have npm install issues in restricted environments,
# you can pre-install node_modules locally and uncomment node_modules
# in .dockerignore, then the COPY . . below will include them
RUN npm ci --legacy-peer-deps || npm install --legacy-peer-deps

# Copy the rest of the application (including node_modules if npm install failed)
COPY . .

# Build the Angular app for production
RUN ./node_modules/.bin/ng build --configuration production

# Stage 2: Serve the application with nginx
FROM nginx:alpine

# Copy the built application from the build stage
COPY --from=build /app/dist/quiz-web/browser /usr/share/nginx/html

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
