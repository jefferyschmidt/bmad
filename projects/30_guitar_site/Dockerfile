```Dockerfile
# Use the official Python image as the base image
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Build the Vue.js frontend
RUN npm install --prefix frontend
RUN npm run build --prefix frontend

# Expose the port that the FastAPI server will run on
EXPOSE 8000

# Set the command to start the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```