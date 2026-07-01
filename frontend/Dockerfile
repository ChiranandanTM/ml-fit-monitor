# Build stage
FROM node:22-alpine as build

WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install --legacy-peer-deps

# Copy the rest of the code
COPY . .

# Build the React app using Vite
RUN npm run build

# Serve stage
FROM nginx:alpine

# Copy the built files from the build stage to Nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Run Nginx
CMD ["nginx", "-g", "daemon off;"]
