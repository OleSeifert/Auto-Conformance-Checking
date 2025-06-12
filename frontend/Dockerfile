FROM node:18-alpine as build

# Set working directory
WORKDIR /app

# Copy dependency files and install
COPY package.json ./
COPY package-lock.json ./
RUN npm install

# Copy rest of the project files
COPY . ./

# Build the React app
RUN npm run build

# Serve with Nginx
FROM nginx:alpine

# Clear the default nginx HTML
RUN rm -rf /usr/share/nginx/html/*

# Copy built files to nginx directory
COPY --from=build /app/build /usr/share/nginx/html

# Expose default nginx port
EXPOSE 80

# Run Nginx in foreground
CMD ["nginx", "-g", "daemon off;"]