# Use the official Node.js image as base
FROM node:20

# Set working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose port 5173 (or the port your Vue app runs on)
EXPOSE 5173

# Command to run the application
CMD ["npm", "run", "dev"]
