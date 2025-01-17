# Step 1: Use Python 3.12 slim base image
FROM python:3.12-slim

# Step 2: Set environment variables to ensure Python output is unbuffered
ENV PYTHONUNBUFFERED 1

# Step 3: Set working directory in the container
WORKDIR /app

# Step 4: Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Step 5: Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Copy the rest of the project files into the container
COPY . /app/

# Step 7: Expose port for the Django app to be accessed
EXPOSE 8000

# Step 8: Command to run the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
