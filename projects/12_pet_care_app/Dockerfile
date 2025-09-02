```Dockerfile
# Use the official Node.js image as the base
FROM node:14-alpine

# Set the working directory to /app
WORKDIR /app

# Copy the package.json and package-lock.json files to the container
COPY package*.json ./

# Install the dependencies
RUN npm ci

# Copy the entire project directory to the container
COPY . .

# Build the React Native app
RUN npm run build

# Set the command to start the Express.js server
CMD ["npm", "start"]
```