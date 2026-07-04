# STAGE 1: Build the React App
FROM node:26.4.0 AS build
WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the code and build for production
COPY . .
RUN npm run build

# STAGE 2: Serve with Nginx
FROM nginx:alpine
# Copy the compiled files from Stage 1 into the Nginx server
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80 (Nginx default)
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]