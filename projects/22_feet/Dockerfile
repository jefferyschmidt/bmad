```Dockerfile
# Use a Node.js base image
FROM node:14

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy the application code
COPY . .

# Build the React.js application
RUN npm run build

# Set the environment variables
ENV NODE_ENV=production

# Expose the port the app will run on
EXPOSE 3000

# Start the Express.js server
CMD ["npm", "start"]
```